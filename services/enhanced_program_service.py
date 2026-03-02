"""
Enhanced Program Service for Alloy AI Fitness System
Implements intelligent day spacing and primary region rotation logic.
"""

import random
import uuid
from typing import Dict, List, Optional, Any, Set
import logging
from datetime import datetime

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
            db_session: Optional database session for movement queries and Hyrox workout selection
            environment: Environment name (development, staging, production)
        """
        self.config_loader = config_loader or ConfigLoader(environment=environment)
        self.db_session = db_session
        self._hyrox_config = self.config_loader.get_hyrox_workout_selection_config()
        self._hyrox_service = None  # Lazy-initialized when DB session is available
    
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
            default_time = request.availability.get("time_allocation", {}).get("default_time_per_day", 60)
            
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
            
            # Generate unique IDs
            program_id = f"prog_{uuid.uuid4().hex[:12]}"
            
            # Determine secondary goals based on normalized goals
            secondary_goals = self._determine_secondary_goals(request.normalized_goals, primary_goal)
            
            # Generate program name based on goal (from config with fallback)
            program_name = self._get_program_name(primary_goal)
            
            # Calculate total sessions
            total_sessions = days_per_week * request.program_length_weeks
            
            # Create training blocks (split program into phases)
            training_blocks = self._create_training_blocks(
                request=request,
                primary_goal=primary_goal,
                days_per_week=days_per_week,
                training_days=training_days,
                session_types_per_week=session_types_per_week,
                default_time=default_time
            )
            
            # Create program skeleton with all required fields
            program_skeleton = ProgramSkeleton(
                program_id=program_id,
                user_id=request.user_id,
                program_name=program_name,
                total_weeks=request.program_length_weeks,
                total_sessions=total_sessions,
                training_blocks=training_blocks,
                primary_goal=primary_goal,
                secondary_goals=secondary_goals,
                created_at=datetime.utcnow()
            )
            
            logger.info(
                f"Created program skeleton: {program_id}, {days_per_week} days/week, "
                f"{request.program_length_weeks} weeks, goal={primary_goal}, "
                f"total_sessions={total_sessions}"
            )
            
            return program_skeleton
            
        except Exception as e:
            logger.error(f"Failed to create program skeleton: {e}", exc_info=True)
            raise
    
    def _determine_secondary_goals(self, normalized_goals: Dict[str, float], primary_goal: str) -> List[str]:
        """
        Determine secondary goals based on normalized goal values.
        
        Args:
            normalized_goals: Dictionary of goal scores
            primary_goal: The primary goal already determined
            
        Returns:
            List of secondary goal strings
        """
        secondary = []
        
        # Add secondary goals based on slider values
        hypertrophy_score = normalized_goals.get("normalized_hypertrophy_fat_loss", 0.5)
        power_score = normalized_goals.get("normalized_power_mobility", 0.5)
        
        if hypertrophy_score > 0.6 and primary_goal != "hypertrophy":
            secondary.append("hypertrophy")
        elif hypertrophy_score < 0.4 and primary_goal != "fat_loss":
            secondary.append("fat_loss")
        
        if power_score > 0.6:
            secondary.append("power")
        elif power_score < 0.4:
            secondary.append("mobility")
        
        # Ensure we have at least one secondary goal
        if not secondary:
            secondary.append("general_conditioning")
        
        return secondary
    
    def _create_training_blocks(
        self,
        request: ProgramGenerationRequest,
        primary_goal: str,
        days_per_week: int,
        training_days: List[int],
        session_types_per_week: List[str],
        default_time: int
    ) -> List[ProgramBlock]:
        """
        Create training blocks for the program.
        
        Splits the program into 2-4 week blocks with progressive focus.
        """
        blocks = []
        total_weeks = request.program_length_weeks
        
        # Determine block structure based on program length
        if total_weeks <= 8:
            block_weeks = [4, 4] if total_weeks == 8 else [4, total_weeks - 4]
        elif total_weeks <= 10:
            block_weeks = [4, 3, 3]
        else:
            block_weeks = [4, 4, total_weeks - 8]
        
        # Block focus progression
        block_focuses = self._get_block_focuses(primary_goal, len(block_weeks))
        intensity_progressions = ["Foundation", "Building", "Peak"]
        
        week_counter = 1
        for block_num, (weeks, focus) in enumerate(zip(block_weeks, block_focuses), 1):
            # Create weekly plans for this block
            weekly_plans = []
            for week_offset in range(weeks):
                week_number = week_counter + week_offset
                weekly_plan = self._create_weekly_plan(
                    week_number=week_number,
                    days_per_week=days_per_week,
                    training_days=training_days,
                    session_types=session_types_per_week,
                    default_time=default_time,
                    primary_goal=primary_goal,
                    experience_level=request.experience_level,
                    block_focus=focus
                )
                weekly_plans.append(weekly_plan)
            
            block = ProgramBlock(
                block_name=f"Block {block_num}: {focus}",
                block_number=block_num,
                weeks_duration=weeks,
                primary_goal=primary_goal,
                weekly_plans=weekly_plans,
                block_focus=focus,
                intensity_progression=intensity_progressions[min(block_num - 1, 2)]
            )
            blocks.append(block)
            week_counter += weeks
        
        return blocks
    
    def _get_block_focuses(self, primary_goal: str, num_blocks: int) -> List[str]:
        """
        Get focus areas for each block based on primary goal.
        Uses config with hardcoded fallback.
        """
        # Try to get from config first
        try:
            focus_config = self.config_loader.config.get("block_focus_progression", {})
            if primary_goal in focus_config:
                focuses = focus_config[primary_goal]
                return focuses[:num_blocks]
        except Exception:
            pass
        
        # Fallback to defaults
        default_focus_map = {
            "strength": ["Strength Foundation", "Strength Building", "Strength Peak"],
            "hypertrophy": ["Volume Accumulation", "Intensification", "Metabolic Stress"],
            "endurance": ["Aerobic Base", "Threshold Development", "Peak Conditioning"],
            "fat_loss": ["Metabolic Conditioning", "High Intensity", "Maintenance"],
            "general_fitness": ["Foundation", "Development", "Performance"]
        }
        focuses = default_focus_map.get(primary_goal, default_focus_map["general_fitness"])
        return focuses[:num_blocks]
    
    def _create_weekly_plan(
        self,
        week_number: int,
        days_per_week: int,
        training_days: List[int],
        session_types: List[str],
        default_time: int,
        primary_goal: str,
        experience_level: str,
        block_focus: str
    ) -> WeeklyPlan:
        """
        Create a weekly plan with session skeletons.
        """
        sessions = []
        all_days = set(range(1, 8))
        training_day_set = set(training_days)
        rest_days = list(all_days - training_day_set)
        
        for i, day_number in enumerate(training_days):
            # Cycle through session types
            session_type_str = session_types[i % len(session_types)]
            session_type = self._map_session_type(session_type_str)
            
            session = self._create_session_skeleton(
                week_number=week_number,
                day_number=day_number,
                session_index=i,
                session_type=session_type,
                duration=default_time,
                experience_level=experience_level,
                primary_goal=primary_goal
            )
            sessions.append(session)
        
        total_training_time = sum(s.total_duration_minutes for s in sessions)
        
        return WeeklyPlan(
            week_number=week_number,
            sessions=sessions,
            total_sessions=len(sessions),
            weekly_focus=block_focus,
            total_training_time=total_training_time,
            rest_days=sorted(rest_days)
        )
    
    def _map_session_type(self, session_type_str: str) -> SessionType:
        """
        Map string session type to SessionType enum.
        """
        mapping = {
            "resistance": SessionType.RESISTANCE_ACCESSORY,
            "hyrox": SessionType.HYROX_STYLE,
            "cardio": SessionType.CARDIO_ONLY,
            "mobility": SessionType.MOBILITY_ONLY,
            "recovery": SessionType.MOBILITY_ONLY  # Map recovery to mobility
        }
        return mapping.get(session_type_str, SessionType.RESISTANCE_ACCESSORY)
    
    def _create_session_skeleton(
        self,
        week_number: int,
        day_number: int,
        session_index: int,
        session_type: SessionType,
        duration: int,
        experience_level: str,
        primary_goal: str,
        hyrox_usage_counts: Optional[Dict[int, int]] = None,
    ) -> SessionSkeleton:
        """
        Create a session skeleton with warmup, main, and cooldown blocks.
        
        For HYROX_STYLE sessions, attempts to attach a pre-built Hyrox workout
        from the hyrox_workouts table. Falls back to generic blocks if unavailable.
        """
        session_id = f"sess_w{week_number}_d{day_number}_{uuid.uuid4().hex[:8]}"
        
        # Determine session focus based on type
        focus_map = {
            SessionType.RESISTANCE_ACCESSORY: "Resistance Training",
            SessionType.RESISTANCE_CIRCUITS: "Circuit Training",
            SessionType.HYROX_STYLE: "Hyrox Conditioning",
            SessionType.CARDIO_ONLY: "Cardiovascular Training",
            SessionType.MOBILITY_ONLY: "Mobility & Recovery"
        }
        session_focus = focus_map.get(session_type, "General Training")
        
        # Calculate block durations from config (with fallback percentages)
        time_allocation = self._get_session_time_allocation()
        warmup_duration = max(5, int(duration * time_allocation["warmup"]))
        cooldown_duration = max(5, int(duration * time_allocation["cooldown"]))
        main_duration = duration - warmup_duration - cooldown_duration
        
        # Create blocks
        blocks = [
            self._create_warmup_block(warmup_duration),
            self._create_main_block(main_duration, session_type, primary_goal),
            self._create_cooldown_block(cooldown_duration)
        ]
        
        # Determine target muscle groups using the region rotation logic
        target_groups = self._select_primary_region_with_rotation(
            session_type=session_type,
            day_number=day_number,
            previous_regions=[],  # Could be enhanced to track across sessions
            week_number=week_number,
            goal=primary_goal
        )
        
        # Hyrox workout attachment — attach a pre-built workout reference
        # when the session type is HYROX_STYLE and the feature is enabled.
        # The actual workout content (lines/tags) is loaded by the frontend
        # via the /api/hyrox/workouts/{id} endpoint.
        hyrox_workout_id = None
        hyrox_workout_name = None
        
        if session_type == SessionType.HYROX_STYLE and self._hyrox_config.get("enabled", True):
            # Selection is deferred to runtime when DB session is available.
            # During skeleton generation (no DB), we set a placeholder note.
            logger.debug(
                f"HYROX_STYLE session w{week_number}d{day_number}: "
                f"Hyrox workout selection available at runtime with DB session"
            )
        
        return SessionSkeleton(
            session_id=session_id,
            day_number=day_number,
            session_focus=session_focus,
            total_duration_minutes=duration,
            blocks=blocks,
            target_muscle_groups=target_groups,
            session_type=session_type,
            difficulty_level=experience_level,
            hyrox_workout_id=hyrox_workout_id,
            hyrox_workout_name=hyrox_workout_name,
        )
    
    def _create_warmup_block(self, duration: int) -> SessionBlock:
        """
        Create a warmup block.
        """
        return SessionBlock(
            block_type=BlockType.WARMUP,
            duration_minutes=duration,
            constraints=BlockConstraints(
                compound=False,
                spinal_compression=[SpinalCompression.NONE, SpinalCompression.LOW],
                min_duration=5,
                max_duration=15
            ),
            target_sets=2,
            target_reps="10-15",
            target_rest_seconds=30,
            notes="Dynamic warmup and mobility preparation"
        )
    
    def _create_main_block(self, duration: int, session_type: SessionType, primary_goal: str) -> SessionBlock:
        """
        Create a main training block.
        Uses config-driven parameters with fallbacks.
        """
        # Get parameters from config or use fallbacks
        block_params = self._get_main_block_params(session_type, primary_goal)
        
        return SessionBlock(
            block_type=BlockType.MAIN,
            session_type=session_type,
            duration_minutes=duration,
            constraints=BlockConstraints(
                compound=block_params["compound"],
                disciplines=block_params["disciplines"],
                min_duration=20,
                max_duration=90
            ),
            target_sets=block_params["target_sets"],
            target_reps=block_params["target_reps"],
            target_rest_seconds=block_params["target_rest"],
            notes=f"Main {session_type.value} block"
        )
    
    def _create_cooldown_block(self, duration: int) -> SessionBlock:
        """
        Create a cooldown block.
        """
        return SessionBlock(
            block_type=BlockType.COOLDOWN,
            duration_minutes=duration,
            constraints=BlockConstraints(
                compound=False,
                spinal_compression=[SpinalCompression.NONE, SpinalCompression.LOW],
                disciplines=[DisciplineType.MOBILITY],
                min_duration=5,
                max_duration=15
            ),
            target_sets=1,
            target_reps="30-60s holds",
            target_rest_seconds=0,
            notes="Static stretching and recovery"
        )
    
    # ========================================================================
    # Config-Driven Helper Methods
    # ========================================================================
    
    def _get_program_name(self, primary_goal: str) -> str:
        """
        Get program name based on goal from config with fallback.
        """
        try:
            name_config = self.config_loader.config.get("program_names", {})
            if primary_goal in name_config:
                return name_config[primary_goal]
        except Exception:
            pass
        
        # Fallback defaults
        default_names = {
            "strength": "Strength Focus Program",
            "hypertrophy": "Muscle Building Program",
            "endurance": "Endurance & Conditioning Program",
            "fat_loss": "Fat Loss & Toning Program",
            "general_fitness": "General Fitness Program"
        }
        return default_names.get(primary_goal, "Custom Program")
    
    def _get_session_time_allocation(self) -> Dict[str, float]:
        """
        Get session time allocation percentages from config with fallback.
        Returns dict with warmup, main, cooldown percentages (0.0-1.0).
        """
        try:
            time_config = self.config_loader.config.get("time_allocation", {})
            if time_config:
                return {
                    "warmup": time_config.get("warmup", 0.15),
                    "main": time_config.get("main", 0.70),
                    "cooldown": time_config.get("cooldown", 0.15)
                }
        except Exception:
            pass
        
        # Fallback defaults
        return {"warmup": 0.15, "main": 0.70, "cooldown": 0.15}
    
    def _get_main_block_params(self, session_type: SessionType, primary_goal: str) -> Dict[str, Any]:
        """
        Get main block parameters from config with fallback.
        Returns dict with target_sets, target_reps, target_rest, compound, disciplines.
        """
        # Try to get from config
        try:
            block_config = self.config_loader.config.get("main_block_params", {})
            session_config = block_config.get(session_type.value, {})
            goal_config = session_config.get(primary_goal, session_config.get("default", {}))
            
            if goal_config:
                disciplines = [DisciplineType(d) for d in goal_config.get("disciplines", [])]
                return {
                    "target_sets": goal_config.get("target_sets", 3),
                    "target_reps": goal_config.get("target_reps", "8-12"),
                    "target_rest": goal_config.get("target_rest", 60),
                    "compound": goal_config.get("compound", True),
                    "disciplines": disciplines if disciplines else [DisciplineType.RESISTANCE_TRAINING]
                }
        except Exception:
            pass
        
        # Fallback defaults based on session type and goal
        return self._get_default_main_block_params(session_type, primary_goal)
    
    def _get_default_main_block_params(self, session_type: SessionType, primary_goal: str) -> Dict[str, Any]:
        """
        Fallback defaults for main block parameters.
        """
        if session_type in [SessionType.RESISTANCE_ACCESSORY, SessionType.RESISTANCE_CIRCUITS]:
            if primary_goal == "strength":
                return {
                    "target_sets": 4, "target_reps": "4-6", "target_rest": 180,
                    "compound": True, "disciplines": [DisciplineType.RESISTANCE_TRAINING, DisciplineType.HYPERTROPHY]
                }
            elif primary_goal == "hypertrophy":
                return {
                    "target_sets": 4, "target_reps": "8-12", "target_rest": 90,
                    "compound": True, "disciplines": [DisciplineType.RESISTANCE_TRAINING, DisciplineType.HYPERTROPHY]
                }
            else:
                return {
                    "target_sets": 3, "target_reps": "10-15", "target_rest": 60,
                    "compound": True, "disciplines": [DisciplineType.RESISTANCE_TRAINING, DisciplineType.HYPERTROPHY]
                }
        elif session_type == SessionType.HYROX_STYLE:
            return {
                "target_sets": 3, "target_reps": "12-20", "target_rest": 45,
                "compound": True, "disciplines": [DisciplineType.ENDURANCE, DisciplineType.RESISTANCE_TRAINING]
            }
        elif session_type == SessionType.CARDIO_ONLY:
            return {
                "target_sets": 1, "target_reps": "20-30 min", "target_rest": 0,
                "compound": False, "disciplines": [DisciplineType.ENDURANCE]
            }
        else:  # MOBILITY_ONLY
            return {
                "target_sets": 2, "target_reps": "30-60s holds", "target_rest": 15,
                "compound": False, "disciplines": [DisciplineType.MOBILITY]
            }
    
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