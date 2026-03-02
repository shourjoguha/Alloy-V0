"""
Configuration Loader Utility for Alloy AI Fitness System.
Provides centralized configuration loading with error handling and validation.
"""

import yaml
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ConfigValidationError(Exception):
    """Exception raised when configuration validation fails."""
    config_key: str
    message: str


# Type aliases for rest time configuration (Python 3.12 type keyword)
type RestTimeContext = str
type ExecutionFormat = str


class ConfigLoader:
    """Load and validate configuration from YAML files."""
    
    def __init__(self, config_path: Optional[Path] = None, environment: str = "production"):
        """
        Initialize config loader.
        
        Args:
            config_path: Path to config file. If None, uses default path.
            environment: Environment name (development, staging, production)
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "program_building_config.yaml"
        
        self.config_path = config_path
        self.environment = environment
        self.config: dict[str, object] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as file:
                self.config = yaml.safe_load(file)
            logger.info(f"Configuration loaded successfully from {self.config_path}")
        except FileNotFoundError as e:
            logger.error(f"Configuration file not found: {self.config_path}")
            raise ConfigValidationError(
                config_key="config_file",
                message=f"Configuration file not found: {self.config_path}"
            ) from e
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in configuration file: {e}")
            raise ConfigValidationError(
                config_key="config_file",
                message=f"Invalid YAML in configuration file: {e}"
            ) from e
    
    def get_day_type_mix(self, goal: str) -> dict[str, int]:
        """
        Get day type percentage distribution for a specific goal.
        
        Args:
            goal: Goal type (strength, hypertrophy, endurance, fat_loss, general_fitness)
            
        Returns:
            Dictionary mapping day types to percentages (must sum to 100)
        """
        try:
            return self.config["day_type_mix"][goal]
        except KeyError as e:
            logger.error(f"Day type mix not found for goal: {goal}")
            raise ConfigValidationError(
                config_key="day_type_mix",
                message=f"Day type mix not found for goal: {goal}"
            ) from e
    
    def get_rest_requirements(self, previous_day_type: str, next_day_type: str) -> int:
        """
        Get minimum rest hours required between session types using intensity-based approach.

        Args:
            previous_day_type: The day type of the previous session
            next_day_type: The day type of the next session

        Returns:
            Minimum rest hours required
        """
        rest_config = self.config.get("rest_requirements", {})

        # Check for hard overrides first
        for override in rest_config.get("overrides", []):
            if override["from"] == previous_day_type and override["to"] == next_day_type:
                logger.debug(
                    f"Using override for rest requirement: {previous_day_type} -> {next_day_type} = {override['hours']}h"
                )
                return override["hours"]

        # Get intensity levels for both session types
        session_intensity = rest_config.get("session_intensity", {})
        from_intensity = session_intensity.get(previous_day_type, "moderate_intensity")
        to_intensity = session_intensity.get(next_day_type, "moderate_intensity")

        # Get baseline hours for each intensity level
        baseline_hours = rest_config.get("baseline_hours", {})
        from_hours = baseline_hours.get(from_intensity, 12)
        to_hours = baseline_hours.get(to_intensity, 12)

        # Use the higher rest requirement
        result = max(from_hours, to_hours)

        logger.debug(
            f"Rest requirement calculation: {previous_day_type}({from_intensity}) -> {next_day_type}({to_intensity}), "
            f"max({from_hours}h, {to_hours}h) = {result}h"
        )

        return result

    def get_movement_rest_requirements(self, previous_movement: str, next_movement: str) -> int:
        """
        Get minimum rest hours required between movement types based on intensity.

        Args:
            previous_movement: The movement type of the previous session (compound, accessory, isolation)
            next_movement: The movement type of the next session (compound, accessory, isolation)

        Returns:
            Minimum rest hours required
        """
        rest_config = self.config.get("rest_requirements", {})

        # Get intensity levels for both movement types
        movement_intensity = rest_config.get("movement_intensity", {})
        from_intensity = movement_intensity.get(previous_movement, "moderate_intensity")
        to_intensity = movement_intensity.get(next_movement, "moderate_intensity")

        # Get baseline hours for each intensity level
        baseline_hours = rest_config.get("baseline_hours", {})
        from_hours = baseline_hours.get(from_intensity, 12)
        to_hours = baseline_hours.get(to_intensity, 12)

        # Use the higher rest requirement
        result = max(from_hours, to_hours)

        logger.debug(
            f"Movement rest requirement: {previous_movement}({from_intensity}) -> {next_movement}({to_intensity}), "
            f"max({from_hours}h, {to_hours}h) = {result}h"
        )

        return result
    
    def get_resistance_split(self, goal: str) -> dict[str, int]:
        """
        Get time allocation percentages for resistance training blocks.
        
        Args:
            goal: Goal type (strength, hypertrophy, endurance)
            
        Returns:
            Dictionary mapping block types to percentages
        """
        try:
            return self.config["resistance_split"][goal]
        except KeyError as e:
            logger.warning(f"Resistance split not found for goal: {goal}, using default")
            return {"compound_block": 50, "superset_block": 40, "accessory_block": 10}
    
    def get_pattern_exposure_thresholds(self) -> dict[str, int]:
        """Get pattern exposure thresholds for variety management."""
        return self.config.get("day_type_determination", {}).get("pattern_exposure_thresholds", {
            "min_exposure_before_rotation": 2,
            "max_consecutive_same_pattern": 4,
            "variety_window_days": 7
        })
    
    def get_goal_alignment_scores(self, goal: str) -> dict[str, int]:
        """
        Get alignment scores for different day types based on goal.
        
        Args:
            goal: Goal type (strength, hypertrophy, endurance, fat_loss, general_fitness)
            
        Returns:
            Dictionary mapping day types to alignment scores
        """
        try:
            return self.config["day_type_determination"]["goal_alignment_scores"][goal]
        except KeyError as e:
            logger.warning(f"Goal alignment scores not found for goal: {goal}")
            return {}
    
    def get_pattern_subtype_categories(self) -> dict[str, list]:
        """Get mapping of high-level categories to pattern subtypes."""
        return self.config.get("pattern_subtype_categories", {})
    
    def get_session_subtype_mapping(self, session_type: str) -> dict[str, list]:
        """
        Get pattern subtype mappings for a specific session type.
        
        Args:
            session_type: Session type (e.g., resistance_accessory, hyrox_style)
            
        Returns:
            Dictionary mapping block types to pattern subtype lists
        """
        return self.config.get("session_subtype_mapping", {}).get(session_type, {})
    
    def get_antagonist_pattern_pairs(self) -> list:
        """Get list of antagonist pattern pairs for superset creation."""
        return self.config.get("antagonist_pattern_pairs", [])
    
    def get_rest_time(
        self,
        execution_format: ExecutionFormat,
        goal: str,
        movement_type: str,
        block_type: str,
        day_type: str,
        equipment_load: str = "moderate"
    ) -> int:
        """
        Get rest time in seconds using baseline + multiplier approach.
        
        Args:
            execution_format: Format of exercise execution (standalone_sets, supersets, circuits, intervals)
            goal: User goal (strength, hypertrophy, endurance, fat_loss, general_fitness)
            movement_type: Type of movement (compound, accessory, isolation, superset, interval)
            block_type: Type of block (warmup, main, cooldown)
            day_type: Type of day (resistance, hyrox, cardio, mobility)
            equipment_load: Equipment load level (heavy, moderate, light)
            
        Returns:
            Rest time in seconds
            
        Raises:
            ConfigValidationError: If execution_format is invalid or configuration is missing
        """
        # Validate execution_format parameter
        valid_formats = {"standalone_sets", "supersets", "circuits", "intervals"}
        if execution_format not in valid_formats:
            raise ConfigValidationError(
                config_key="rest_time.execution_format",
                message=f"Invalid execution_format '{execution_format}'. Must be one of: {valid_formats}"
            )
        
        rest_config = self.config.get("rest_time", {})
        
        # Check for hard overrides first
        context = f"{goal}_{day_type}_{movement_type}_{block_type}_{execution_format}"
        for override in rest_config.get("overrides", []):
            if override["context"] == context:
                logger.debug(f"Using override for rest time context: {context}")
                return override["seconds"]
        
        # Get baseline
        try:
            baseline = rest_config["baseline"][execution_format]["seconds"]
        except KeyError as e:
            raise ConfigValidationError(
                config_key="rest_time.baseline",
                message=f"Baseline rest time not found for execution_format '{execution_format}': {e}"
            ) from e
        
        # Collect applicable multipliers
        multipliers = rest_config.get("multipliers", {})
        applicable_multipliers = [
            multipliers.get("goal", {}).get(goal, 1.0),
            multipliers.get("movement_type", {}).get(movement_type, 1.0),
            multipliers.get("block_type", {}).get(block_type, 1.0),
            multipliers.get("day_type", {}).get(day_type, 1.0),
            multipliers.get("equipment_load", {}).get(equipment_load, 1.0),
        ]
        
        # Calculate final multiplier
        final_multiplier = 1.0
        rules = rest_config.get("combination_rules", {})
        
        if rules.get("method") == "multiplicative":
            for m in applicable_multipliers:
                final_multiplier *= m
        
        # Clamp to range
        min_multiplier = rules.get("min_multiplier", 0.0)
        max_multiplier = rules.get("max_multiplier", 3.0)
        final_multiplier = max(min_multiplier, min(max_multiplier, final_multiplier))
        
        result = int(baseline * final_multiplier)
        logger.debug(
            f"Rest time calculation: baseline={baseline}s, multiplier={final_multiplier:.2f}, "
            f"context={context}, result={result}s"
        )
        
        return result
    
    def get_rep_set_ranges(
        self,
        goal: str,
        block_type: str,
        day_type: str
    ) -> dict[str, int]:
        """
        Get rep and set ranges using baseline + offset approach.

        Args:
            goal: User goal (strength, hypertrophy, endurance, fat_loss, general_fitness)
            block_type: Type of block (warmup, main, cooldown)
            day_type: Type of day (resistance, hyrox, cardio, mobility)

        Returns:
            Dictionary with rep_min, rep_max, set_min, set_max keys

        Raises:
            ConfigValidationError: If baseline configuration is missing or invalid
        """
        ranges_config = self.config.get("rep_set_ranges", {})

        # Check for hard overrides first
        context = f"{goal}_{block_type}_{day_type}"
        for override in ranges_config.get("overrides", []):
            if override["context"] == context:
                logger.debug(f"Using override for rep/set context: {context}")
                return {
                    "rep_min": override["rep_min"],
                    "rep_max": override["rep_max"],
                    "set_min": override["set_min"],
                    "set_max": override["set_max"],
                }

        # Get baseline for goal
        try:
            baseline = ranges_config["baseline"][goal]
        except KeyError as e:
            raise ConfigValidationError(
                config_key="rep_set_ranges.baseline",
                message=f"Baseline rep/set ranges not found for goal '{goal}': {e}"
            ) from e

        # Apply block_type adjustments
        block_adj = ranges_config.get("block_type_adjustments", {}).get(block_type, {})
        rep_min = baseline["rep_min"] + block_adj.get("rep_offset", 0)
        rep_max = baseline["rep_max"] + block_adj.get("rep_offset", 0)
        set_min = baseline["set_min"] + block_adj.get("set_offset", 0)
        set_max = baseline["set_max"] + block_adj.get("set_offset", 0)

        # Apply day_type adjustments
        day_adj = ranges_config.get("day_type_adjustments", {}).get(day_type, {})
        rep_min += day_adj.get("rep_offset", 0)
        rep_max += day_adj.get("rep_offset", 0)
        set_min += day_adj.get("set_offset", 0)
        set_max += day_adj.get("set_offset", 0)

        # Apply constraints
        constraints = ranges_config.get("constraints", {})
        rep_min = max(constraints.get("min_reps", 1), rep_min)
        rep_max = min(constraints.get("max_reps", 50), rep_max)
        set_min = max(constraints.get("min_sets", 1), set_min)
        set_max = min(constraints.get("max_sets", 10), set_max)

        # Ensure min <= max after constraints
        rep_min = min(rep_min, rep_max)
        set_min = min(set_min, set_max)

        logger.debug(
            f"Rep/set calculation: goal={goal}, block={block_type}, day={day_type}, "
            f"result=rep {rep_min}-{rep_max}, sets {set_min}-{set_max}"
        )

        return {
            "rep_min": rep_min,
            "rep_max": rep_max,
            "set_min": set_min,
            "set_max": set_max,
        }
    
    def get_equipment_mapping(self) -> dict[str, str]:
        """Get equipment name to database column mapping."""
        return self.config.get("equipment_mapping", {})
    
    def get_olympic_restrictions(self) -> dict[str, object]:
        """Get Olympic movement restrictions."""
        return self.config.get("olympic_restrictions", {})
    
    def get_selection_priority_rules(self) -> list:
        """Get day type selection priority rules."""
        return self.config.get("day_type_determination", {}).get("selection_priority", [])
    
    def get_training_day_spacing_patterns(self) -> dict[int, list[int]]:
        """
        Get optimal training day spacing patterns for different frequencies.

        Returns:
            Dictionary mapping days per week (1-7) to list of day numbers (1-7)
            for optimal placement
        """
        patterns = self.config.get("training_day_spacing_patterns", {})
        # Convert string keys to integers for easier usage
        return {int(k): v for k, v in patterns.items()}
    
    def get_session_region_priorities(self, session_type: str) -> list[str]:
        """
        Get primary region priorities for a specific session type.

        Args:
            session_type: Session type (e.g., resistance_accessory, resistance_circuits)

        Returns:
            List of region names in priority order (lower indices = higher priority)
        """
        return self.config.get("session_region_priorities", {}).get(session_type, ["full"])

    def get_region_options(self, body_area: str) -> list[str]:
        """
        Get available region options for a specific body area.

        Args:
            body_area: Body area (upper, lower)

        Returns:
            List of region names for the specified body area

        Raises:
            ConfigValidationError: If body_area is invalid or configuration is missing
        """
        valid_areas = {"upper", "lower"}
        if body_area not in valid_areas:
            raise ConfigValidationError(
                config_key="region_options.body_area",
                message=f"Invalid body_area '{body_area}'. Must be one of: {valid_areas}"
            )

        region_config = self.config.get("region_options", {})
        return region_config.get(body_area, [])
    
    def get_program_length_weeks_limits(self) -> dict[str, int]:
        """
        Get min/max limits for program length in weeks.

        Returns:
            Dictionary with min and max keys for program length limits
        """
        return self.config.get("validation", {}).get("request_validation", {}).get(
            "program_length_weeks", {"min": 8, "max": 12}
        )
    
    def get_days_per_week_limits(self) -> dict[str, int]:
        """
        Get min/max limits for days per week.

        Returns:
            Dictionary with min and max keys for days per week limits
        """
        return self.config.get("validation", {}).get("request_validation", {}).get(
            "days_per_week", {"min": 1, "max": 7}
        )
    
    def get_normalized_goals_limits(self) -> dict[str, float]:
        """
        Get min/max limits for normalized goal values.

        Returns:
            Dictionary with min_value and max_value keys for normalized goal limits
        """
        return self.config.get("validation", {}).get("request_validation", {}).get(
            "normalized_goals", {"min_value": 0.0, "max_value": 1.0}
        )
    
    def get_required_goal_keys(self) -> list[str]:
        """
        Get list of required goal keys for validation.

        Returns:
            List of required goal key names
        """
        return self.config.get("validation", {}).get("request_validation", {}).get(
            "required_goal_keys", [
                "primary_strength",
                "normalized_hypertrophy_fat_loss",
                "normalized_power_mobility",
                "strength_bias",
                "endurance_bias"
            ]
        )
    
    def get_movement_query_disciplines(self, query_type: str) -> list[str]:
        """
        Get list of disciplines for a specific movement query type.

        Args:
            query_type: Query type (warmup, cooldown, strength, accessory, hyrox_carries,
                        mobility, cardio, olympic)

        Returns:
            List of discipline names for the specified query type
        """
        return self.config.get("movement_query_disciplines", {}).get(query_type, [])
    
    def get_session_discipline_mapping(self, session_type: str) -> list[str]:
        """
        Get list of disciplines for a specific session type.

        Args:
            session_type: Session type (e.g., resistance_accessory, hyrox_style, mobility_only)

        Returns:
            List of discipline names for the specified session type
        """
        mapping = self.config.get("movement_query_disciplines", {}).get(
            "session_discipline_mapping", {}
        )
        return mapping.get(session_type, [])
    
    def get_default_pattern_subtypes(self, query_type: str) -> list[str]:
        """
        Get default pattern subtypes for a specific query type.

        These are fallback values used when config values are missing or empty.
        Eliminates need for hardcoded default values in Python code.

        Args:
            query_type: Query type (balanced, strength, accessory, carry, sled)

        Returns:
            List of default pattern subtype names for the specified query type
        """
        return self.config.get("default_pattern_subtypes", {}).get(query_type, [])
    
    def get_accessory_movement_priority(self) -> list[dict[str, object]]:
        """
        Get accessory movement priority configuration for ORDER BY clause generation.

        This configuration controls how accessory movements are ranked during selection.
        The priority values are used to build a CASE statement in the SQL ORDER BY clause.

        Returns:
            List of priority dictionaries with the following structure:
            [
                {
                    "priority": int,
                    "condition": str,
                    "condition_type": str,  # "pattern_subtype" or "compound_flag"
                    "subtypes": list[str],   # Optional: for pattern_subtype conditions
                    "value": bool,           # Optional: for compound_flag conditions
                    "description": str
                },
                ...
            ]
        """
        return self.config.get("accessory_movement_priority", [])
    
    def get_hyrox_workout_selection_config(self) -> dict[str, object]:
        """
        Get Hyrox workout selection configuration.

        Controls how pre-built Hyrox workouts are selected and placed into
        program sessions. Includes time tolerance, repeat limits, and
        accessory-block eligibility settings.

        Returns:
            Dictionary with selection parameters. Keys:
            - enabled: bool
            - time_tolerance_minutes: int
            - max_repeats_per_program: int
            - min_weeks_between_repeat: int
            - accessory_block_max_duration_minutes: int
            - accessory_eligible_workout_types: list[str]
            - session_eligible_workout_types: list[str]
        """
        defaults = {
            "enabled": True,
            "time_tolerance_minutes": 5,
            "max_repeats_per_program": 2,
            "min_weeks_between_repeat": 2,
            "accessory_block_max_duration_minutes": 15,
            "accessory_eligible_workout_types": ["amrap", "emom", "for_time"],
            "session_eligible_workout_types": [
                "amrap", "emom", "for_time", "rounds_for_time",
                "time_cap", "ladder", "mini_circuit", "explicit_time_guidance"
            ],
        }
        config = self.config.get("hyrox_workout_selection", {})
        # Merge with defaults so missing keys fall back
        return {**defaults, **config}

    def get_enum_values(self, enum_name: str) -> list[str]:
        """
        Get valid enum values for a movement property from config.

        This provides the single source of truth for enum validation.
        Values are validated against the movement_enum_values section in the config.

        Args:
            enum_name: Name of the enum (e.g., "primary_muscle", "discipline", "metric_type")

        Returns:
            List of valid enum values for the specified property
        """
        enum_config = self.config.get("movement_enum_values", {})
        values = enum_config.get(enum_name, [])
        
        if not values:
            logger.warning(f"No enum values found for '{enum_name}' in movement_enum_values config")
        
        return values
    
    def validate_enum_value(self, enum_name: str, value: str) -> bool:
        """
        Validate a value against enum config.

        This ensures that values used in database queries are valid enum values,
        preventing invalid data and providing type safety.

        Args:
            enum_name: Name of the enum (e.g., "primary_muscle", "discipline", "metric_type")
            value: Value to validate

        Returns:
            True if value is valid for the enum, False otherwise
        """
        valid_values = self.get_enum_values(enum_name)
        return value in valid_values
    
    def validate_enum_values(self, enum_name: str, values: list[str]) -> list[str]:
        """
        Validate multiple values against enum config and return only valid ones.

        This is useful for filtering user-provided lists to ensure only valid
        enum values are used in database queries.

        Args:
            enum_name: Name of the enum (e.g., "primary_muscle", "discipline", "metric_type")
            values: List of values to validate

        Returns:
            List of valid values (invalid values are filtered out and logged)
        """
        valid_values = self.get_enum_values(enum_name)
        valid_list = []
        
        for value in values:
            if value in valid_values:
                valid_list.append(value)
            else:
                logger.warning(f"Invalid value '{value}' for enum '{enum_name}', filtering out")
        
        return valid_list
