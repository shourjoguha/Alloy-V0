from pydantic import BaseModel, Field, validator, root_validator
from typing import Dict, List, Optional, Union
from datetime import datetime
import math

from models.enums import (
    GoalType, SessionType, BlockType, EquipmentType, 
    PrimaryRegion, SpinalCompression, DisciplineType, MetricType
)


class GoalSlider(BaseModel):
    """Individual goal slider configuration."""
    value: float = Field(..., ge=0.0, le=1.0, description="Slider value from 0.0 to 1.0")
    label: str = Field(..., description="Human-readable label for the slider")
    
    @validator('value')
    def validate_slider_value(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError("Slider value must be between 0.0 and 1.0")
        return v


class HierarchicalGoalSliders(BaseModel):
    """Hierarchical goal slider configuration with normalization."""
    
    # Primary slider - Strength vs Endurance
    primary_slider: GoalSlider = Field(
        default=GoalSlider(value=0.5, label="Strength vs Endurance"),
        description="Primary goal: 0.0 = pure endurance, 1.0 = pure strength"
    )
    
    # Secondary sliders
    hypertrophy_fat_loss: GoalSlider = Field(
        default=GoalSlider(value=0.5, label="Hypertrophy vs Fat Loss"),
        description="Secondary goal: 0.0 = fat loss focus, 1.0 = hypertrophy focus"
    )
    
    power_mobility: GoalSlider = Field(
        default=GoalSlider(value=0.5, label="Power vs Mobility"),
        description="Secondary goal: 0.0 = mobility focus, 1.0 = power focus"
    )
    
    # Normalized values (computed)
    normalized_hypertrophy_fat_loss: Optional[float] = Field(None, description="Normalized hypertrophy/fat loss weight")
    normalized_power_mobility: Optional[float] = Field(None, description="Normalized power/mobility weight")
    
    def normalize_sliders(self) -> Dict[str, float]:
        """Apply sigmoid normalization to secondary sliders based on primary."""
        primary_value = self.primary_slider.value
        
        # Sigmoid parameters from config
        k_strength = 6.0  # steepness for strength bias
        k_endurance = 6.0   # steepness for endurance bias
        
        # Calculate influence based on primary slider
        # When primary is high (strength focus), hypertrophy gets boost, fat loss gets reduction
        strength_influence = 1 / (1 + math.exp(-k_strength * (primary_value - 0.5)))
        endurance_influence = 1 - strength_influence
        
        # Normalize hypertrophy/fat loss slider
        base_hfl = self.hypertrophy_fat_loss.value
        hfl_adjustment = (strength_influence * 0.3) + (endurance_influence * -0.2)
        normalized_hfl = max(0.05, min(0.95, base_hfl + hfl_adjustment))
        
        # Normalize power/mobility slider
        base_pm = self.power_mobility.value
        pm_adjustment = (strength_influence * 0.4) + (endurance_influence * -0.3)
        normalized_pm = max(0.05, min(0.95, base_pm + pm_adjustment))
        
        return {
            "primary_strength": primary_value,
            "normalized_hypertrophy_fat_loss": normalized_hfl,
            "normalized_power_mobility": normalized_pm,
            "strength_bias": strength_influence,
            "endurance_bias": endurance_influence
        }


class TimeAllocation(BaseModel):
    """Time allocation configuration for sessions."""
    
    default_time_per_day: int = Field(
        default=60, ge=15, le=180, description="Default session time in minutes"
    )
    apply_to_all_days: bool = Field(
        default=True, description="Whether to apply default time to all days"
    )
    custom_times_per_day: Optional[Dict[str, int]] = Field(
        default=None, description="Custom times for specific days (day_name: minutes)"
    )
    delegate_to_system: bool = Field(
        default=False, description="Let system optimize time allocation"
    )
    
    @validator('custom_times_per_day')
    def validate_custom_times(cls, v):
        if v is not None:
            valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            for day, time in v.items():
                if day.lower() not in valid_days:
                    raise ValueError(f"Invalid day: {day}")
                if not 15 <= time <= 180:
                    raise ValueError(f"Time for {day} must be between 15-180 minutes")
        return v


class AvailabilityConfig(BaseModel):
    """User availability configuration."""
    
    days_per_week: int = Field(
        default=3, ge=1, le=7, description="Number of days available per week"
    )
    preferred_days: Optional[List[str]] = Field(
        default=None, description="Preferred workout days (optional)"
    )
    time_allocation: TimeAllocation = Field(
        default_factory=TimeAllocation, description="Time allocation settings"
    )
    
    @validator('preferred_days')
    def validate_preferred_days(cls, v):
        if v is not None:
            valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            for day in v:
                if day.lower() not in valid_days:
                    raise ValueError(f"Invalid day: {day}")
        return v


class OnboardingRequest(BaseModel):
    """Complete onboarding request."""
    
    user_id: str = Field(..., description="User identifier")
    goals: HierarchicalGoalSliders = Field(
        default_factory=HierarchicalGoalSliders, description="Hierarchical goal configuration"
    )
    availability: AvailabilityConfig = Field(
        default_factory=AvailabilityConfig, description="Availability and time configuration"
    )
    available_equipment: List[EquipmentType] = Field(
        default_factory=list, description="Equipment available to user"
    )
    experience_level: str = Field(
        default="intermediate", description="User fitness experience level"
    )
    program_length_weeks: int = Field(
        default=10, ge=8, le=12, description="Desired program length in weeks"
    )
    
    def get_normalized_goals(self) -> Dict[str, float]:
        """Get normalized goal weights for program generation."""
        return self.goals.normalize_sliders()
    
    def get_total_weekly_time(self) -> int:
        """Calculate total available time per week."""
        if self.availability.time_allocation.delegate_to_system:
            # System will optimize, return default for now
            return self.availability.days_per_week * 60
        
        if self.availability.time_allocation.apply_to_all_days:
            return self.availability.days_per_week * self.availability.time_allocation.default_time_per_day
        
        if self.availability.time_allocation.custom_times_per_day:
            return sum(self.availability.time_allocation.custom_times_per_day.values())
        
        return self.availability.days_per_week * self.availability.time_allocation.default_time_per_day


class OnboardingResponse(BaseModel):
    """Response from onboarding validation."""
    
    success: bool = Field(..., description="Whether onboarding configuration is valid")
    normalized_goals: Optional[Dict[str, float]] = Field(
        default=None, description="Normalized goal weights"
    )
    recommended_program_length: Optional[int] = Field(
        default=None, description="Recommended program length in weeks"
    )
    time_allocation_suggestion: Optional[Dict[str, int]] = Field(
        default=None, description="Suggested time allocation per day"
    )
    errors: Optional[List[str]] = Field(
        default=None, description="Validation errors if any"
    )
    warnings: Optional[List[str]] = Field(
        default=None, description="Configuration warnings"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "normalized_goals": {
                    "primary_strength": 0.7,
                    "normalized_hypertrophy_fat_loss": 0.65,
                    "normalized_power_mobility": 0.72,
                    "strength_bias": 0.75,
                    "endurance_bias": 0.25
                },
                "recommended_program_length": 12,
                "time_allocation_suggestion": {
                    "monday": 75,
                    "wednesday": 75,
                    "friday": 90
                }
            }
        }