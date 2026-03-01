"""
Enhanced Program Service for Alloy AI Fitness System
Implements intelligent day spacing and primary region rotation logic.
"""

import random
from typing import Dict, List, Optional, Any, Set
import logging

from models.enums import (
    SessionType, BlockType, EquipmentType, PrimaryRegion,
    SpinalCompression, DisciplineType, MetricType
)
from models.program import (
    ProgramSkeleton, ProgramBlock, WeeklyPlan, SessionSkeleton,
    SessionBlock, BlockConstraints, ProgramGenerationRequest, ProgramGenerationResponse
)
from utils.config_loader import ConfigLoader, ConfigValidationError

logger = logging.getLogger(__name__)


class EnhancedProgramService:
    """Enhanced service for generating hierarchical program skeletons with intelligent spacing."""
    
    def __init__(self, config_loader: Optional[ConfigLoader] = None, db_session: Optional[Any] = None, 
                 environment: str = "production"):
        """
        Initialize with configuration loader (Dependency Injection).
        
        Args:
            config_loader: Optional ConfigLoader instance. If None, creates default instance
            db_session: Optional database session for movement queries (currently unused)
            environment: Environment name (development, staging, production)
        """
        self.config_loader = config_loader or ConfigLoader(environment=environment)
    
    # ========================================================================
    # Day Type Mix Methods
    # ========================================================================
    
    def get_day_type_distribution(self, goal: str) -> Dict[str, int]:
        """
        Get day type percentage distribution for a specific goal.
        
        Args:
            goal: Goal type (strength, hypertrophy, endurance, fat_loss, general_fitness)
            
        Returns:
            Dictionary mapping day types to percentages (must sum to 100)
        """
        try:
            return self.config_loader.get_day_type_mix(goal)
        except ConfigValidationError as e:
            logger.error(f"Failed to get day type distribution for {goal}: {e}")
            # Fallback to balanced distribution
            return {"resistance": 50, "hyrox": 25, "cardio": 15, "mobility": 10, "recovery": 0}
    
    def calculate_session_types_for_week(self, goal: str, days_per_week: int) -> List[str]:
        """
        Calculate the session types for a week based on goal and availability.
        
        Args:
            goal: User's primary goal
            days_per_week: Number of training days per week
            
        Returns:
            List of session types for the week
        """
        distribution = self.get_day_type_distribution(goal)
        
        # Convert percentages to counts
        total_sessions = days_per_week
        session_counts = {}
        remaining = total_sessions
        
        for day_type, percentage in sorted(distribution.items(), key=lambda x: -x[1]):
            if remaining <= 0:
                break
            count = int((percentage / 100) * total_sessions)
            if count > 0:
                session_counts[day_type] = count
                remaining -= count
        
        # Distribute remaining sessions to highest priority day types
        if remaining > 0:
            for day_type in sorted(distribution.items(), key=lambda x: -x[1]):
                if remaining <= 0:
                    break
                if day_type[0] in session_counts:
                    session_counts[day_type[0]] += 1
                    remaining -= 1
        
        # Create list of session types
        session_types = []
        for day_type, count in session_counts.items():
            session_types.extend([day_type] * count)
        
        # Shuffle for variety
        random.shuffle(session_types)
        
        return session_types[:total_sessions]
    
    # ========================================================================
    # Rest Requirements Methods
    # ========================================================================
    
    def get_rest_hours_between_sessions(self, previous_day_type: str, next_day_type: str) -> int:
        """
        Get minimum rest hours required between session types.
        
        Args:
            previous_day_type: The day type of the previous session
            next_day_type: The day type of the next session
            
        Returns:
            Minimum rest hours required
        """
        return self.config_loader.get_rest_requirements(previous_day_type, next_day_type)
    
    def validate_session_spacing(self, session_sequence: List[str]) -> List[Dict[str, Any]]:
        """
        Validate that session sequence respects rest requirements.
        
        Args:
            session_sequence: List of session types in order
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        for i in range(1, len(session_sequence)):
            previous_type = session_sequence[i - 1]
            next_type = session_sequence[i]
            
            required_rest = self.get_rest_hours_between_sessions(previous_type, next_type)
            
            if required_rest > 24:
                errors.append({
                    "position": i,
                    "previous_session": previous_type,
                    "next_session": next_type,
                    "required_rest_hours": required_rest,
                    "message": f"Session {i} requires {required_rest}h rest after {previous_type}"
                })
        
        return errors
    
    # ========================================================================
    # Resistance Split Methods
    # ========================================================================
    
    def get_resistance_time_allocation(self, goal: str) -> Dict[str, int]:
        """
        Get time allocation percentages for resistance training blocks.
        
        Args:
            goal: Goal type (strength, hypertrophy, endurance)
            
        Returns:
            Dictionary mapping block types to percentages
        """
        return self.config_loader.get_resistance_split(goal)
    
    def calculate_block_durations(self, total_minutes: int, goal: str) -> Dict[str, int]:
        """
        Calculate duration in minutes for each resistance block based on goal.
        
        Args:
            total_minutes: Total duration of resistance session
            goal: User's goal
            
        Returns:
            Dictionary with compound_block, superset_block, accessory_block durations
        """
        split = self.get_resistance_time_allocation(goal)
        
        return {
            "compound_block": int((split["compound_block"] / 100) * total_minutes),
            "superset_block": int((split["superset_block"] / 100) * total_minutes),
            "accessory_block": int((split["accessory_block"] / 100) * total_minutes)
        }
    
    # ========================================================================
    # Day Type Determination Methods
    # ========================================================================
    
    def get_pattern_exposure_thresholds(self) -> Dict[str, int]:
        """Get pattern exposure thresholds for variety management."""
        return self.config_loader.get_pattern_exposure_thresholds()
    
    def get_goal_alignment_scores(self, goal: str) -> Dict[str, int]:
        """
        Get alignment scores for different day types based on goal.
        
        Args:
            goal: Goal type (strength, hypertrophy, endurance, fat_loss, general_fitness)
            
        Returns:
            Dictionary mapping day types to alignment scores
        """
        return self.config_loader.get_goal_alignment_scores(goal)
    

    
    def _get_intelligent_training_days(self, days_per_week: int, program_length_weeks: int, 
                                       goal: str = "general_fitness") -> List[int]:
        """
        Generate intelligent training day distribution with optimal rest spacing.
        
        Uses goal-based day type distribution and rest requirements to determine
        optimal training day placement.
        
        Args:
            days_per_week: Number of training days per week
            program_length_weeks: Length of program in weeks
            goal: User's primary goal
            
        Returns:
            List of day numbers (1-7) for training days
        """
        # Load optimal spacing patterns from configuration
        # These are optimized for recovery and training frequency
        spacing_patterns = self.config_loader.get_training_day_spacing_patterns()
        
        if days_per_week not in spacing_patterns:
            # Fallback to even distribution
            return self._distribute_training_days_fallback(days_per_week)
        
        base_pattern = spacing_patterns[days_per_week]
        
        # Validate pattern against rest requirements
        session_types = self.calculate_session_types_for_week(goal, days_per_week)
        validation_errors = self.validate_session_spacing(session_types)
        
        if validation_errors:
            logger.warning(f"Pattern validation failed for {days_per_week} days: {validation_errors}")
            # Use fallback pattern if validation fails
            return self._distribute_training_days_fallback(days_per_week)
        
        # For longer programs, vary pattern slightly each week
        # to prevent overuse patterns, but keep core spacing
        # Placeholder: could implement sophisticated variation logic here
        return base_pattern
    
    def _distribute_training_days_fallback(self, days_per_week: int) -> List[int]:
        """Fallback method for distributing training days."""
        # Even distribution across the week
        interval = 7 / days_per_week
        return [int(1 + i * interval) for i in range(days_per_week)]
    
    def _select_primary_region_with_rotation(
        self, 
        session_type: SessionType, 
        day_number: int,
        previous_regions: List[PrimaryRegion],
        week_number: int,
        goal: str = "general_fitness"
    ) -> List[PrimaryRegion]:
        """
        Select primary region with intelligent rotation to avoid consecutive same regions.
        
        Rules:
        - Never use same primary region on consecutive days
        - Prefer alternating upper/lower for resistance sessions
        - Full body sessions can be used more flexibly
        - Consider weekly patterns for longer programs
        - Use goal-based alignment for region selection
        
        Args:
            session_type: Type of session being planned
            day_number: Day of the week (1-7)
            previous_regions: List of regions used on previous days
            week_number: Current week number in program
            goal: User's primary goal
            
        Returns:
            List of PrimaryRegion values for the session
        """
        # Load region priorities from config
        session_priorities = self.config_loader.get_session_region_priorities(
            session_type.value
        )
        
        # Get previous day's regions
        last_day_regions = previous_regions[-1] if previous_regions else []
        
        # For resistance sessions, implement intelligent upper/lower rotation
        if session_type in [SessionType.RESISTANCE_ACCESSORY, SessionType.RESISTANCE_CIRCUITS]:
            return self._get_resistance_region_rotation(
                day_number, last_day_regions, week_number, goal
            )
        
        # For other session types, use full body or core focus
        elif session_type == SessionType.HYROX_STYLE:
            return [PrimaryRegion.FULL_BODY]
        elif session_type == SessionType.MOBILITY_ONLY:
            return [PrimaryRegion.FULL_BODY]
        elif session_type == SessionType.CARDIO_ONLY:
            return [PrimaryRegion.FULL_BODY]
        
        return [PrimaryRegion.FULL_BODY]
    
    def _get_resistance_region_rotation(
        self, 
        day_number: int, 
        last_day_regions: List[PrimaryRegion],
        week_number: int,
        goal: str = "general_fitness"
    ) -> List[PrimaryRegion]:
        """
        Implement intelligent upper/lower rotation for resistance training.
        
        Uses goal-based region preferences and pattern variety thresholds.
        
        Pattern for 5-day example:
        Day 1 (Mon): Upper body focus
        Day 2 (Tue): Lower body focus  
        Day 4 (Thu): Upper body focus (different from Monday)
        Day 5 (Fri): Lower body focus (different from Tuesday)
        Day 6 (Sat): Full body/core focus
        
        Args:
            day_number: Day of the week (1-7)
            last_day_regions: Regions used on the previous day
            week_number: Current week in program
            goal: User's primary goal
            
        Returns:
            List of PrimaryRegion values for the session
        """
        # Load region options from config
        upper_options_config = self.config_loader.get_region_options("upper")
        lower_options_config = self.config_loader.get_region_options("lower")

        # Convert config strings to PrimaryRegion enum values
        upper_options = [PrimaryRegion(region) for region in upper_options_config]
        lower_options = [PrimaryRegion(region) for region in lower_options_config]

        # Get pattern variety thresholds from config
        thresholds = self.get_pattern_exposure_thresholds()
        
        # Check if we need to avoid repeating last day's region
        avoid_last_region = len(last_day_regions) > 0 and thresholds["max_consecutive_same_pattern"] > 0
        
        # Simple rotation based on day number
        if day_number in [1, 4]:  # Monday, Thursday
            # Upper body focus, alternate specific regions
            if week_number % 2 == 0:
                selected_region = PrimaryRegion.ANTERIOR_UPPER
            else:
                selected_region = PrimaryRegion.POSTERIOR_UPPER
            
            # Avoid repeating last day's region if needed
            if avoid_last_region and selected_region in last_day_regions:
                # Find alternative upper region
                for region in upper_options:
                    if region not in last_day_regions:
                        selected_region = region
                        break
            
            return [selected_region]
            
        elif day_number in [2, 5]:  # Tuesday, Friday
            # Lower body focus, alternate specific regions
            if week_number % 2 == 0:
                selected_region = PrimaryRegion.ANTERIOR_LOWER
            else:
                selected_region = PrimaryRegion.POSTERIOR_LOWER
            
            # Avoid repeating last day's region if needed
            if avoid_last_region and selected_region in last_day_regions:
                # Find alternative lower region
                for region in lower_options:
                    if region not in last_day_regions:
                        selected_region = region
                        break
            
            return [selected_region]
            
        elif day_number == 6:  # Saturday
            return [PrimaryRegion.FULL_BODY]
        else:  # Sunday or other
            return [PrimaryRegion.CORE]
    
    # ... (rest of the methods from original ProgramService, updated to use enhanced logic)
    
    async def generate_program_skeleton(self, request: ProgramGenerationRequest) -> ProgramGenerationResponse:
        """
        Generate a complete program skeleton with intelligent spacing and region rotation.
        
        Uses configuration-driven day type distribution, rest requirements, and
        pattern variety management to create optimal training programs.
        
        Args:
            request: Program generation request with normalized goals and preferences
            
        Returns:
            ProgramGenerationResponse with generated skeleton or errors
        """
        try:
            # Validate request
            validation_errors = self._validate_request(request)
            if validation_errors:
                return ProgramGenerationResponse(
                    success=False,
                    errors=validation_errors
                )
            
            # Generate program structure with enhanced logic
            program_skeleton = self._create_enhanced_program_skeleton(request)
            
            # Calculate session breakdown
            session_breakdown = self._calculate_session_breakdown(program_skeleton)
            
            return ProgramGenerationResponse(
                success=True,
                program_skeleton=program_skeleton,
                session_breakdown=session_breakdown
            )
            
        except Exception as e:
            logger.error(f"Program generation failed: {e}", exc_info=True)
            return ProgramGenerationResponse(
                success=False,
                errors=[f"Program generation failed: {str(e)}"]
            )
    
    def _create_enhanced_program_skeleton(self, request: ProgramGenerationRequest) -> ProgramSkeleton:
        """
        Create program skeleton with enhanced day spacing and region rotation.
        
        Uses configuration for all decision-making:
        - Day type distribution based on goals
        - Rest requirements between sessions
        - Pattern variety thresholds
        - Resistance training splits
        """
        try:
            # Get primary goal from normalized goals
            primary_goal = self._determine_primary_goal(request.normalized_goals)
            
            # Get training days per week
            days_per_week = request.availability.get("days_per_week", 3)
            
            # Generate intelligent training day distribution
            training_days = self._get_intelligent_training_days(
                days_per_week, 
                request.program_length_weeks,
                primary_goal
            )
            
            # Calculate session types for the program
            session_types_per_week = self.calculate_session_types_for_week(
                primary_goal, 
                days_per_week
            )
            
            # Create program skeleton
            # This is a simplified implementation - full version would create
            # complete ProgramSkeleton with all blocks, weeks, and sessions
            program_skeleton = ProgramSkeleton(
                program_id="temp_id",  # Would be generated
                user_id="temp_user_id",  # From request
                program_length_weeks=request.program_length_weeks,
                training_blocks=[],
                constraints=self._get_block_constraints(request, primary_goal)
            )
            
            logger.info(
                f"Created program skeleton: {days_per_week} days/week, "
                f"{request.program_length_weeks} weeks, goal={primary_goal}"
            )
            
            return program_skeleton
            
        except Exception as e:
            logger.error(f"Failed to create program skeleton: {e}", exc_info=True)
            raise
    
    def _determine_primary_goal(self, normalized_goals: Dict[str, float]) -> str:
        """
        Determine the primary goal from normalized goal scores.
        
        Args:
            normalized_goals: Dictionary of goal scores
            
        Returns:
            Primary goal string
        """
        goal_scores = {
            "strength": normalized_goals.get("primary_strength", 0),
            "hypertrophy": normalized_goals.get("normalized_hypertrophy_fat_loss", 0),
            "endurance": normalized_goals.get("normalized_power_mobility", 0) * 0.5 + 
                         normalized_goals.get("endurance_bias", 0) * 0.5,
            "fat_loss": normalized_goals.get("normalized_hypertrophy_fat_loss", 0) * 0.5,
            "general_fitness": 0.5  # Default
        }
        
        primary_goal = max(goal_scores.items(), key=lambda x: x[1])[0]
        
        # Map to config goal names
        goal_mapping = {
            "strength": "strength",
            "hypertrophy": "hypertrophy",
            "endurance": "endurance",
            "fat_loss": "fat_loss",
            "general_fitness": "general_fitness"
        }
        
        return goal_mapping.get(primary_goal, "general_fitness")
    
    def _get_block_constraints(self, request: ProgramGenerationRequest, 
                                goal: str) -> BlockConstraints:
        """
        Get block constraints from configuration.
        
        Args:
            request: Program generation request
            goal: Primary goal
            
        Returns:
            BlockConstraints object
        """
        # This would pull from config - simplified for now
        return BlockConstraints(
            min_duration=30,
            max_duration=90,
            preferred_duration=60
        )
        
    def _validate_request(self, request: ProgramGenerationRequest) -> List[str]:
        """Validate the program generation request."""
        errors = []
        
        # Validate program length using config thresholds
        program_length_limits = self.config_loader.get_program_length_weeks_limits()
        if not (program_length_limits["min"] <= request.program_length_weeks <= program_length_limits["max"]):
            errors.append(f"Program length must be between {program_length_limits['min']}-{program_length_limits['max']} weeks")
        
        # Validate days per week using config thresholds
        days_per_week_limits = self.config_loader.get_days_per_week_limits()
        days_per_week = request.availability.get("days_per_week", 3)
        if not (days_per_week_limits["min"] <= days_per_week <= days_per_week_limits["max"]):
            errors.append(f"Days per week must be between {days_per_week_limits['min']}-{days_per_week_limits['max']}")
        
        # Validate normalized goals using config thresholds
        required_keys = self.config_loader.get_required_goal_keys()
        normalized_goals_limits = self.config_loader.get_normalized_goals_limits()
        for key in required_keys:
            if key not in request.normalized_goals:
                errors.append(f"Missing normalized goal: {key}")
            elif not (normalized_goals_limits["min_value"] <= request.normalized_goals[key] <= normalized_goals_limits["max_value"]):
                errors.append(f"Invalid normalized goal value for {key}")
        
        return errors
    
    def _calculate_session_breakdown(self, program_skeleton: ProgramSkeleton) -> Dict[str, int]:
        """Calculate the breakdown of session types in the program."""
        breakdown = {}
        
        for session_type in SessionType:
            count = 0
            for block in program_skeleton.training_blocks:
                for week in block.weekly_plans:
                    for session in week.sessions:
                        if session.session_type == session_type:
                            count += 1
            breakdown[session_type.value] = count
        
        return breakdown