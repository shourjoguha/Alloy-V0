from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional
import logging
from datetime import datetime

from models.onboarding import (
    OnboardingRequest, OnboardingResponse, HierarchicalGoalSliders,
    GoalSlider, AvailabilityConfig, TimeAllocation
)
from models.program import ProgramGenerationRequest, ProgramGenerationResponse
from services.goal_normalizer import GoalNormalizer
from services.enhanced_program_service import EnhancedProgramService
from utils.config_loader import ConfigLoader

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/onboarding", tags=["onboarding"])

# Initialize services with Dependency Injection
config_loader = ConfigLoader(environment="production")
goal_normalizer = GoalNormalizer()
program_service = EnhancedProgramService(config_loader=config_loader)


@router.post("/validate-sliders", response_model=OnboardingResponse)
async def validate_goal_sliders(request: OnboardingRequest):
    """
    Validate hierarchical goal sliders and return normalized weights.
    
    This endpoint validates the user's goal configuration and applies
    mathematical normalization to ensure consistent slider behavior.
    """
    try:
        logger.info(f"Validating goal sliders for user: {request.user_id}")
        
        # Normalize goals using hierarchical algorithm
        normalized_goals = request.get_normalized_goals()
        
        # Validate goal consistency
        warnings = goal_normalizer.validate_goal_consistency({
            "primary_slider": request.goals.primary_slider.value,
            "hypertrophy_fat_loss": request.goals.hypertrophy_fat_loss.value,
            "power_mobility": request.goals.power_mobility.value
        })
        
        # Recommend program length based on goals
        recommended_length = goal_normalizer.recommend_program_length(normalized_goals)
        
        # Suggest time allocation if delegate_to_system is True
        time_suggestion = None
        if request.availability.time_allocation.delegate_to_system:
            time_suggestion = suggest_optimal_time_allocation(request, normalized_goals)
        
        response = OnboardingResponse(
            success=True,
            normalized_goals=normalized_goals,
            recommended_program_length=recommended_length,
            time_allocation_suggestion=time_suggestion,
            warnings=warnings if warnings else None
        )
        
        logger.info(f"Goal slider validation successful for user: {request.user_id}")
        return response
        
    except Exception as e:
        logger.error(f"Goal slider validation failed for user: {request.user_id}. Error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "GOAL_VALIDATION_FAILED",
                    "message": "Failed to validate goal sliders",
                    "details": str(e),
                    "trace_id": f"validate_{request.user_id}_{datetime.now().timestamp()}",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )


@router.post("/generate-program", response_model=ProgramGenerationResponse)
async def generate_program_skeleton(request: OnboardingRequest):
    """
    Generate a complete program skeleton based on onboarding configuration.
    
    This endpoint creates a hierarchical program structure with:
    - Training blocks with specific focuses
    - Weekly microcycles with session distribution
    - Daily session skeletons with warmup/main/cooldown blocks
    - Movement constraints and target parameters
    """
    try:
        logger.info(f"Generating program skeleton for user: {request.user_id}")
        
        # First validate and normalize goals
        normalized_goals = request.get_normalized_goals()
        
        # Create program generation request
        program_request = ProgramGenerationRequest(
            user_id=request.user_id,
            normalized_goals=normalized_goals,
            availability={
                "days_per_week": request.availability.days_per_week,
                "time_allocation": {
                    "default_time_per_day": request.availability.time_allocation.default_time_per_day,
                    "delegate_to_system": request.availability.time_allocation.delegate_to_system
                }
            },
            available_equipment=request.available_equipment,
            program_length_weeks=request.program_length_weeks,
            experience_level=request.experience_level
        )
        
        # Generate program skeleton
        program_response = program_service.generate_program_skeleton(program_request)
        
        if not program_response.success:
            logger.error(f"Program generation failed for user: {request.user_id}. Errors: {program_response.errors}")
            raise HTTPException(
                status_code=400,
                detail={
                    "error": {
                        "code": "PROGRAM_GENERATION_FAILED",
                        "message": "Failed to generate program skeleton",
                        "details": program_response.errors,
                        "trace_id": f"generate_{request.user_id}_{datetime.now().timestamp()}",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )
        
        logger.info(f"Program skeleton generated successfully for user: {request.user_id}")
        return program_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Program generation failed for user: {request.user_id}. Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred during program generation",
                    "details": str(e),
                    "trace_id": f"error_{request.user_id}_{datetime.now().timestamp()}",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )


def suggest_optimal_time_allocation(request: OnboardingRequest, normalized_goals: Dict[str, float]) -> Dict[str, int]:
    """
    Suggest optimal time allocation per day based on goals and availability.
    
    Uses workout type optimization to allocate different time budgets
    for resistance vs cardio vs mobility days.
    """
    days_per_week = request.availability.days_per_week
    
    # Base time allocation based on goals
    strength_bias = normalized_goals["strength_bias"]
    endurance_bias = normalized_goals["endurance_bias"]
    
    if strength_bias > endurance_bias:
        # Strength-focused program needs longer sessions
        base_time = 75  # minutes
        session_times = [75, 90, 60]  # Rotate between 75, 90, 60 minutes
    else:
        # Endurance-focused program can have varied durations
        base_time = 60  # minutes
        session_times = [45, 60, 75]  # Rotate between 45, 60, 75 minutes
    
    # Distribute across training days
    training_days = get_training_days(days_per_week)
    time_allocation = {}
    
    for i, day in enumerate(training_days):
        time_allocation[day] = session_times[i % len(session_times)]
    
    return time_allocation


def get_training_days(days_per_week: int) -> List[str]:
    """Get optimal training day names based on frequency."""
    all_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    
    if days_per_week == 1:
        return ["wednesday"]
    elif days_per_week == 2:
        return ["tuesday", "friday"]
    elif days_per_week == 3:
        return ["monday", "wednesday", "friday"]
    elif days_per_week == 4:
        return ["monday", "wednesday", "friday", "saturday"]
    elif days_per_week == 5:
        return ["monday", "tuesday", "thursday", "friday", "saturday"]
    elif days_per_week == 6:
        return ["monday", "tuesday", "wednesday", "friday", "saturday", "sunday"]
    else:
        return all_days


@router.get("/health")
async def health_check():
    """Health check endpoint for the onboarding service."""
    return {
        "status": "healthy",
        "service": "onboarding",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@router.get("/config/sliders")
async def get_slider_configuration():
    """Get current slider configuration and constraints."""
    return {
        "primary_slider": {
            "name": "Strength vs Endurance",
            "range": [0.0, 1.0],
            "description": "Primary training focus: 0.0 = pure endurance, 1.0 = pure strength"
        },
        "secondary_sliders": [
            {
                "name": "Hypertrophy vs Fat Loss",
                "range": [0.0, 1.0],
                "description": "Body composition focus: 0.0 = fat loss, 1.0 = hypertrophy"
            },
            {
                "name": "Power vs Mobility",
                "range": [0.0, 1.0],
                "description": "Performance focus: 0.0 = mobility, 1.0 = power"
            }
        ],
        "constraints": {
            "min_value": 0.0,
            "max_value": 1.0,
            "normalization_enabled": True,
            "hierarchical_influence": True
        }
    }


@router.get("/config/time-allocation")
async def get_time_allocation_configuration():
    """Get time allocation configuration options."""
    return {
        "default_session_time": 60,  # minutes
        "min_session_time": 15,      # minutes
        "max_session_time": 180,     # minutes
        "options": {
            "apply_to_all_days": "Use same time for all training days",
            "custom_per_day": "Set different times for each training day",
            "delegate_to_system": "Let system optimize time allocation"
        },
        "optimization_factors": [
            "Workout type (resistance vs cardio vs mobility)",
            "Session complexity and intensity",
            "Recovery requirements between sessions",
            "User experience level and goals"
        ]
    }