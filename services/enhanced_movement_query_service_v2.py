"""
Enhanced Movement Query Service for Alloy AI Fitness System
Uses pattern_subtype for granular movement selection while preserving original pattern column.
Configuration-driven approach using program_building_config.yaml.
"""

import logging
from typing import List, Dict, Any, Optional, Set
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from models.enums import (
    PrimaryRegion, DisciplineType, SpinalCompression
)
from utils.config_loader import ConfigLoader, ConfigValidationError

logger = logging.getLogger(__name__)


class EnhancedMovementQueryServiceV2:
    """Enhanced service using pattern_subtype for intelligent movement selection.
    
    Configuration-driven: All pattern subtypes, session mappings, and equipment
    filters are loaded from program_building_config.yaml via ConfigLoader.
    """
    
    def __init__(self, db_session: AsyncSession, config_loader: Optional[ConfigLoader] = None):
        """
        Initialize with database session and configuration loader.
        
        Args:
            db_session: SQLAlchemy async session for database operations
            config_loader: Optional ConfigLoader instance. If None, creates new instance.
        """
        self.db = db_session
        self.config_loader = config_loader or ConfigLoader()
        
        # Cache frequently accessed config values for performance
        self._equipment_mapping = self.config_loader.get_equipment_mapping()
        self._pattern_subtype_categories = self.config_loader.get_pattern_subtype_categories()
        self._circuit_tables_config = self.config_loader.config.get("circuit_tables", {})
        
        logger.info("EnhancedMovementQueryServiceV2 initialized with configuration-driven approach")
    
    def get_pattern_subtypes_by_category(self, category: str) -> List[str]:
        """
        Get pattern subtypes for a high-level category from config.
        
        Args:
            category: Category name (e.g., push, pull, lower, core, cardio)
            
        Returns:
            List of pattern subtype strings for the category
        """
        try:
            return self._pattern_subtype_categories.get(category, [])
        except Exception as e:
            logger.error(f"Error getting pattern subtypes for category '{category}': {e}")
            return []
    
    def get_session_subtypes(self, session_type: str) -> Dict[str, List[str]]:
        """
        Get pattern subtype mappings for a specific session type from config.
        
        Args:
            session_type: Session type (e.g., resistance_accessory, hyrox_style)
            
        Returns:
            Dictionary mapping block types to pattern subtype lists
        """
        try:
            return self.config_loader.get_session_subtype_mapping(session_type)
        except Exception as e:
            logger.error(f"Error getting session subtypes for '{session_type}': {e}")
            return {}
    
    def is_circuit_integration_enabled(self) -> bool:
        """Check if circuit table integration is enabled in config."""
        try:
            return self._circuit_tables_config.get("enabled", False)
        except Exception as e:
            logger.error(f"Error checking circuit integration: {e}")
            return False
    
    def get_circuit_patterns(self, circuit_type: str) -> List[Dict[str, Any]]:
        """
        Get circuit patterns for a specific circuit type.
        Placeholder method for future circuit table integration.
        
        Args:
            circuit_type: Type of circuit (e.g., warmup_circuits, hyrox_circuits)
            
        Returns:
            List of circuit pattern dictionaries
        """
        try:
            patterns = self._circuit_tables_config.get("circuit_patterns", {})
            return patterns.get(circuit_type, [])
        except Exception as e:
            logger.error(f"Error getting circuit patterns for '{circuit_type}': {e}")
            return []
    
    def _build_accessory_order_by_clause(self) -> str:
        """
        Build ORDER BY clause for accessory movements using config-driven priorities.
        
        This method reads priority configuration from program_building_config.yaml
        and generates a SQL CASE statement for the ORDER BY clause.
        
        Returns:
            SQL ORDER BY clause string (CASE statement followed by RANDOM())
        """
        try:
            priority_config = self.config_loader.get_accessory_movement_priority()
            
            if not priority_config:
                logger.warning("No accessory movement priority config found, using default ORDER BY RANDOM()")
                return "RANDOM()"
            
            # Build CASE statement from config
            case_conditions = []
            for priority_item in priority_config:
                priority = priority_item.get("priority", 99)
                condition_type = priority_item.get("condition_type", "")
                
                if condition_type == "pattern_subtype":
                    subtypes = priority_item.get("subtypes", [])
                    if subtypes:
                        subtype_list = ", ".join([f"'{s}'" for s in subtypes])
                        case_conditions.append(
                            f"WHEN pattern_subtype IN ({subtype_list}) THEN {priority}"
                        )
                
                elif condition_type == "compound_flag":
                    value = priority_item.get("value")
                    if value is not None:
                        sql_value = "true" if value else "false"
                        case_conditions.append(
                            f"WHEN compound = {sql_value} THEN {priority}"
                        )
            
            if not case_conditions:
                logger.warning("No valid CASE conditions generated, using default ORDER BY RANDOM()")
                return "RANDOM()"
            
            # Combine CASE conditions with a default ELSE
            case_statement = "CASE " + " ".join(case_conditions) + " ELSE 99 END"
            
            # Add RANDOM() for tie-breaking within same priority
            order_by_clause = f"{case_statement}, RANDOM()"
            
            logger.debug(f"Built ORDER BY clause from config: {order_by_clause}")
            return order_by_clause
            
        except Exception as e:
            logger.error(f"Error building ORDER BY clause from config: {e}, using default")
            return "RANDOM()"
    
    async def get_balanced_movement_set(
        self,
        session_type: str,
        equipment_available: List[str],
        target_regions: Optional[List[str]] = None,
        max_movements: int = 8,
        include_variations: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get a balanced set of movements using pattern_subtype distribution.
        
        This ensures we get complementary movements (push/pull, upper/lower)
        and uses the pattern_subtype column for intelligent combinations.
        Pattern subtypes and session mappings are loaded from config.
        
        Args:
            session_type: Type of session (e.g., resistance_accessory, hyrox_style)
            equipment_available: List of available equipment types
            target_regions: Optional list of primary regions to filter by
            max_movements: Maximum number of movements to return
            include_variations: Whether to include movement variations
            
        Returns:
            List of movement dictionaries with pattern_subtype information
        """
        # Get available subtypes for this session type from config
        session_subtypes = self.get_session_subtypes(session_type)
        
        # Build subtype distribution from config
        subtypes_to_include = []
        for category, subtypes in session_subtypes.items():
            subtypes_to_include.extend(subtypes)
        
        if not subtypes_to_include:
            logger.warning(f"No pattern subtypes found for session type '{session_type}', using defaults from config")
            subtypes_to_include = self.config_loader.get_default_pattern_subtypes("balanced")
        
        # Build equipment filter
        equipment_where = self._build_equipment_filter(equipment_available)
        
        # Build region filter with proper parameter binding
        region_where = "true"
        region_params = {}
        if target_regions:
            region_where = "primary_region IN :regions"
            region_params["regions"] = tuple(target_regions)
        
        # Build subtype filter with proper parameter binding
        subtype_where = "true"
        subtype_params = {}
        if subtypes_to_include:
            subtype_where = "pattern_subtype IN :subtypes"
            subtype_params["subtypes"] = tuple(subtypes_to_include)

        # Build discipline filter based on session type with parameter binding
        discipline_where, discipline_params = self._get_discipline_filter(session_type)

        # Build compound filter based on session type
        compound_filter = self._get_compound_filter(session_type)

        # Validate regions against enum config
        if target_regions:
            valid_regions = self.config_loader.validate_enum_values("primary_region", target_regions)
            if len(valid_regions) < len(target_regions):
                logger.warning(f"Some regions were invalid, filtered from {len(target_regions)} to {len(valid_regions)}")

        query = f"""
        SELECT id, name, discipline, primary_region, primary_muscle, pattern, pattern_subtype, compound,
               spinal_compression, bodyweight_possible, dumbbell_possible, kettlebell_possible,
               barbell_possible, machine_possible, band_possible, plate_or_med_ball_possible,
               is_complex_lift, is_unilateral, regression_to_move, progression_to_move
        FROM movements
        WHERE {discipline_where}
        AND {compound_filter}
        AND {subtype_where}
        AND {equipment_where}
        AND {region_where}
        ORDER BY RANDOM()
        LIMIT :limit
        """

        params = {"limit": max_movements}
        params.update(region_params)
        params.update(subtype_params)
        params.update(discipline_params)

        result = await self.db.execute(text(query), params)
        movements = result.fetchall()
        
        return self._format_movement_results(movements)
    
    async def get_warmup_movements(
        self,
        equipment_available: List[str],
        max_movements: int = 5,
        execution_format: str = "standalone_sets"
    ) -> List[Dict[str, Any]]:
        """
        Get appropriate warmup movements using pattern_subtype-based selection.

        Criteria:
        - discipline from config (warmup section)
        - compound = false OR compound IS NULL
        - spinal_compression IN ('none', 'low')
        - Pattern_subtype-based: uses mobility category from config

        Args:
            equipment_available: List of available equipment types
            max_movements: Maximum number of movements to return
            execution_format: Format for rest time calculation ("standalone_sets" or "circuits")

        Returns:
            List of movement dictionaries suitable for warmup
        """
        # Get mobility pattern subtypes from config
        mobility_subtypes = self.get_pattern_subtypes_by_category("mobility")
        
        # Get warmup disciplines from config
        warmup_disciplines = self.config_loader.get_movement_query_disciplines("warmup")
        discipline_where, discipline_params = self._build_discipline_filter(warmup_disciplines)

        equipment_where = self._build_equipment_filter(equipment_available)

        query = f"""
        SELECT id, name, discipline, primary_region, primary_muscle, pattern, pattern_subtype, compound,
               spinal_compression, bodyweight_possible, dumbbell_possible, kettlebell_possible,
               barbell_possible, machine_possible, band_possible, plate_or_med_ball_possible,
               is_complex_lift, is_unilateral
        FROM movements
        WHERE {discipline_where}
        AND (compound = false OR compound IS NULL)
        AND spinal_compression IN ('none', 'low')
        AND {equipment_where}
        ORDER BY RANDOM()
        LIMIT :limit
        """

        params = {"limit": max_movements}
        params.update(discipline_params)

        result = await self.db.execute(text(query), params)
        movements = result.fetchall()
        
        return self._format_movement_results(movements)
    
    async def get_strength_movements(
        self,
        equipment_available: List[str],
        primary_regions: Optional[List[str]] = None,
        max_movements: int = 6,
        execution_format: str = "standalone_sets"
    ) -> List[Dict[str, Any]]:
        """
        Get strength section movements - compound, pattern_subtype-based selection.

        Criteria:
        - discipline from config (strength section)
        - compound = true
        - olympic = false (save olympic for advanced sessions)
        - Pattern_subtype-based: uses push, pull, lower categories from config

        Args:
            equipment_available: List of available equipment types
            primary_regions: Optional list of primary regions to filter by
            max_movements: Maximum number of movements to return
            execution_format: Format for rest time calculation ("standalone_sets" or "circuits")

        Returns:
            List of strength-focused movement dictionaries
        """
        # Get strength pattern subtypes from config (push, pull, lower categories)
        push_subtypes = self.get_pattern_subtypes_by_category("push")
        pull_subtypes = self.get_pattern_subtypes_by_category("pull")
        lower_subtypes = self.get_pattern_subtypes_by_category("lower")
        
        # Combine all strength subtypes
        strength_subtypes = push_subtypes + pull_subtypes + lower_subtypes
        
        if not strength_subtypes:
            logger.warning("No strength subtypes found in config, using defaults from config")
            strength_subtypes = self.config_loader.get_default_pattern_subtypes("strength")
        
        # Get strength disciplines from config
        strength_disciplines = self.config_loader.get_movement_query_disciplines("strength")
        discipline_where, discipline_params = self._build_discipline_filter(strength_disciplines)

        equipment_where = self._build_equipment_filter(equipment_available)

        # Build region filter with proper parameter binding
        region_where = "true"
        region_params = {}
        if primary_regions:
            region_where = "primary_region IN :regions"
            region_params["regions"] = tuple(primary_regions)

        # Build subtype filter with proper parameter binding
        subtype_where = "true"
        subtype_params = {}
        if strength_subtypes:
            subtype_where = "pattern_subtype IN :subtypes"
            subtype_params["subtypes"] = tuple(strength_subtypes)

        # Validate regions against enum config
        if primary_regions:
            valid_regions = self.config_loader.validate_enum_values("primary_region", primary_regions)
            if len(valid_regions) < len(primary_regions):
                logger.warning(f"Some regions were invalid, filtered from {len(primary_regions)} to {len(valid_regions)}")

        query = f"""
        SELECT id, name, discipline, primary_region, primary_muscle, pattern, pattern_subtype, compound,
               spinal_compression, bodyweight_possible, dumbbell_possible, kettlebell_possible,
               barbell_possible, machine_possible, band_possible, plate_or_med_ball_possible,
               is_complex_lift, is_unilateral, regression_to_move, progression_to_move
        FROM movements
        WHERE {discipline_where}
        AND compound = true
        AND {subtype_where}
        AND {equipment_where}
        AND {region_where}
        ORDER BY RANDOM()
        LIMIT :limit
        """

        params = {"limit": max_movements}
        params.update(region_params)
        params.update(subtype_params)
        params.update(discipline_params)

        result = await self.db.execute(text(query), params)
        movements = result.fetchall()
        
        return self._format_movement_results(movements)
    
    async def get_accessory_movements(
        self,
        equipment_available: List[str],
        primary_regions: Optional[List[str]] = None,
        max_movements: int = 8,
        execution_format: str = "standalone_sets"
    ) -> List[Dict[str, Any]]:
        """
        Get accessory section movements - all resistance training with pattern_subtype variety.

        Criteria:
        - discipline from config (accessory section)
        - NO compound filter - all movements
        - Pattern_subtype-based: uses vertical, core, athletic categories from config

        Args:
            equipment_available: List of available equipment types
            primary_regions: Optional list of primary regions to filter by
            max_movements: Maximum number of movements to return
            execution_format: Format for rest time calculation ("standalone_sets" or "circuits")

        Returns:
            List of accessory movement dictionaries
        """
        # Get accessory pattern subtypes from config (core, athletic categories)
        core_subtypes = self.get_pattern_subtypes_by_category("core")
        athletic_subtypes = self.get_pattern_subtypes_by_category("athletic")
        
        # Combine with vertical movements (subset of push/pull categories)
        push_subtypes = self.get_pattern_subtypes_by_category("push")
        pull_subtypes = self.get_pattern_subtypes_by_category("pull")
        
        # Filter for vertical movements from push/pull
        vertical_subtypes = [s for s in push_subtypes + pull_subtypes if "vertical" in s]
        
        # Combine all accessory subtypes
        accessory_subtypes = vertical_subtypes + core_subtypes + athletic_subtypes
        
        if not accessory_subtypes:
            logger.warning("No accessory subtypes found in config, using defaults from config")
            accessory_subtypes = self.config_loader.get_default_pattern_subtypes("accessory")
        
        # Get accessory disciplines from config
        accessory_disciplines = self.config_loader.get_movement_query_disciplines("accessory")
        discipline_where, discipline_params = self._build_discipline_filter(accessory_disciplines)

        equipment_where = self._build_equipment_filter(equipment_available)

        # Build region filter with proper parameter binding
        region_where = "true"
        region_params = {}
        if primary_regions:
            region_where = "primary_region IN :regions"
            region_params["regions"] = tuple(primary_regions)

        # Build subtype filter with proper parameter binding
        subtype_where = "true"
        subtype_params = {}
        if accessory_subtypes:
            subtype_where = "pattern_subtype IN :subtypes"
            subtype_params["subtypes"] = tuple(accessory_subtypes)

        # Validate regions against enum config
        if primary_regions:
            valid_regions = self.config_loader.validate_enum_values("primary_region", primary_regions)
            if len(valid_regions) < len(primary_regions):
                logger.warning(f"Some regions were invalid, filtered from {len(primary_regions)} to {len(valid_regions)}")

        # Build ORDER BY clause from config-driven priorities
        order_by_clause = self._build_accessory_order_by_clause()

        query = f"""
        SELECT id, name, discipline, primary_region, primary_muscle, pattern, pattern_subtype, compound,
               spinal_compression, bodyweight_possible, dumbbell_possible, kettlebell_possible,
               barbell_possible, machine_possible, band_possible, plate_or_med_ball_possible,
               is_complex_lift, is_unilateral, regression_to_move, progression_to_move
        FROM movements
        WHERE {discipline_where}
        AND ({subtype_where} OR compound = false)
        AND {equipment_where}
        AND {region_where}
        ORDER BY {order_by_clause}
        LIMIT :limit
        """

        params = {"limit": max_movements}
        params.update(region_params)
        params.update(subtype_params)
        params.update(discipline_params)

        result = await self.db.execute(text(query), params)
        movements = result.fetchall()
        
        return self._format_movement_results(movements)
    
    async def get_hyrox_carries(
        self, 
        equipment_available: List[str],
        max_movements: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Get hyrox carries movements - pattern_subtype-based selection using config.
        
        Criteria:
        - discipline from config (hyrox_carries section)
        - pattern_subtype-based: uses carry category from config
        
        Args:
            equipment_available: List of available equipment types
            max_movements: Maximum number of movements to return
            
        Returns:
            List of carry movement dictionaries
        """
        # Get carry pattern subtypes from config
        carry_subtypes = self.get_pattern_subtypes_by_category("carry")
        sled_subtypes = self.get_pattern_subtypes_by_category("sled")
        
        # Combine carry and sled subtypes for Hyrox
        hyrox_carry_subtypes = carry_subtypes + sled_subtypes
        
        # Get hyrox carries disciplines from config
        hyrox_carries_disciplines = self.config_loader.get_movement_query_disciplines("hyrox_carries")
        discipline_where, discipline_params = self._build_discipline_filter(hyrox_carries_disciplines)

        equipment_where = self._build_equipment_filter(equipment_available)

        # Build subtype filter from config with proper parameter binding
        subtype_where = "true"
        subtype_params = {}
        if hyrox_carry_subtypes:
            subtype_where = "pattern_subtype IN :subtypes"
            subtype_params["subtypes"] = tuple(hyrox_carry_subtypes)
        else:
            # Try default subtypes from config
            default_carry_subtypes = self.config_loader.get_default_pattern_subtypes("carry")
            if default_carry_subtypes:
                logger.warning("No carry subtypes found in pattern_subtype_categories, using defaults from config")
                subtype_where = "pattern_subtype IN :subtypes"
                subtype_params["subtypes"] = tuple(default_carry_subtypes)
            else:
                # Final fallback to name-based search if no subtypes in config
                logger.warning("No carry subtypes found in config, using name-based search")
                subtype_where = "(name ILIKE '%carry%' OR name ILIKE '%farmer%' OR name ILIKE '%waiter%' OR name ILIKE '%suitcase%' OR name ILIKE '%sled%')"

        query = f"""
        SELECT id, name, discipline, primary_region, primary_muscle, pattern, pattern_subtype, compound,
               spinal_compression, bodyweight_possible, dumbbell_possible, kettlebell_possible,
               barbell_possible, machine_possible, band_possible, plate_or_med_ball_possible,
               is_complex_lift, is_unilateral
        FROM movements
        WHERE {discipline_where}
        AND {subtype_where}
        AND {equipment_where}
        ORDER BY RANDOM()
        LIMIT :limit
        """

        params = {"limit": max_movements}
        params.update(subtype_params)
        params.update(discipline_params)

        result = await self.db.execute(text(query), params)
        movements = result.fetchall()
        
        return self._format_movement_results(movements)
    
    async def get_mobility_movements(
        self,
        equipment_available: List[str],
        max_movements: int = 8,
        execution_format: str = "standalone_sets"
    ) -> List[Dict[str, Any]]:
        """
        Get mobility-focused movements - pattern_subtype and discipline based.

        Criteria:
        - discipline from config (mobility section)
        - Uses mobility category from config

        Args:
            equipment_available: List of available equipment types
            max_movements: Maximum number of movements to return
            execution_format: Format for rest time calculation ("standalone_sets" or "circuits")

        Returns:
            List of mobility-focused movement dictionaries
        """
        # Get mobility pattern subtypes from config
        mobility_subtypes = self.get_pattern_subtypes_by_category("mobility")
        
        # Get mobility disciplines from config
        mobility_disciplines = self.config_loader.get_movement_query_disciplines("mobility")
        discipline_where, discipline_params = self._build_discipline_filter(mobility_disciplines)

        equipment_where = self._build_equipment_filter(equipment_available)

        # Build subtype filter from config with proper parameter binding
        subtype_where = "true"  # Default: no subtype filter
        subtype_params = {}
        if mobility_subtypes:
            subtype_where = "pattern_subtype IN :subtypes"
            subtype_params["subtypes"] = tuple(mobility_subtypes)

        query = f"""
        SELECT id, name, discipline, primary_region, primary_muscle, pattern, pattern_subtype, compound,
               spinal_compression, bodyweight_possible, dumbbell_possible, kettlebell_possible,
               barbell_possible, machine_possible, band_possible, plate_or_med_ball_possible
        FROM movements
        WHERE {discipline_where}
        AND {subtype_where}
        AND {equipment_where}
        ORDER BY RANDOM()
        LIMIT :limit
        """

        params = {"limit": max_movements}
        params.update(subtype_params)
        params.update(discipline_params)

        result = await self.db.execute(text(query), params)
        movements = result.fetchall()
        
        return self._format_movement_results(movements)
    
    async def get_cardio_movements(
        self,
        equipment_available: List[str],
        max_movements: int = 6,
        execution_format: str = "standalone_sets"
    ) -> List[Dict[str, Any]]:
        """
        Get cardio movements - pattern_subtype and discipline based.

        Criteria:
        - discipline from config (cardio section)
        - Uses cardio category from config

        Args:
            equipment_available: List of available equipment types
            max_movements: Maximum number of movements to return
            execution_format: Format for rest time calculation ("standalone_sets" or "circuits")

        Returns:
            List of cardio movement dictionaries
        """
        # Get cardio pattern subtypes from config
        cardio_subtypes = self.get_pattern_subtypes_by_category("cardio")
        
        # Get cardio disciplines from config
        cardio_disciplines = self.config_loader.get_movement_query_disciplines("cardio")
        discipline_where, discipline_params = self._build_discipline_filter(cardio_disciplines)

        equipment_where = self._build_equipment_filter(equipment_available)

        # Build subtype filter from config with proper parameter binding
        subtype_where = "true"  # Default: no subtype filter
        subtype_params = {}
        if cardio_subtypes:
            subtype_where = "pattern_subtype IN :subtypes"
            subtype_params["subtypes"] = tuple(cardio_subtypes)

        query = f"""
        SELECT id, name, discipline, primary_region, primary_muscle, pattern, pattern_subtype, compound,
               spinal_compression, bodyweight_possible, dumbbell_possible, kettlebell_possible,
               barbell_possible, machine_possible, band_possible, plate_or_med_ball_possible,
               metric_type
        FROM movements
        WHERE {discipline_where}
        AND {subtype_where}
        AND {equipment_where}
        ORDER BY RANDOM()
        LIMIT :limit
        """

        params = {"limit": max_movements}
        params.update(subtype_params)
        params.update(discipline_params)

        result = await self.db.execute(text(query), params)
        movements = result.fetchall()
        
        return self._format_movement_results(movements)
    
    async def get_olympic_movements(
        self,
        equipment_available: List[str],
        user_level: str = "intermediate",
        max_movements: int = 3,
        execution_format: str = "standalone_sets"
    ) -> List[Dict[str, Any]]:
        """
        Get olympic lift movements for advanced users.

        Criteria:
        - discipline from config (olympic section and olympic_restrictions)
        - User level validated against olympic_restrictions config
        - Pattern_subtype-based: complex lift patterns

        Args:
            equipment_available: List of available equipment types
            user_level: User experience level (beginner, intermediate, advanced)
            max_movements: Maximum number of movements to return
            execution_format: Format for rest time calculation ("standalone_sets" or "circuits")

        Returns:
            List of Olympic movement dictionaries, empty if user level is insufficient
        """
        # Validate user level - only intermediate and advanced can access Olympic movements
        if user_level not in ["intermediate", "advanced"]:
            logger.info(f"User level '{user_level}' does not meet Olympic requirements")
            return []
        
        # Get Olympic disciplines from config (movement_query_disciplines section)
        olympic_disciplines = self.config_loader.get_movement_query_disciplines("olympic")
        discipline_where, discipline_params = self._build_discipline_filter(olympic_disciplines)

        equipment_where = self._build_equipment_filter(equipment_available)

        query = f"""
        SELECT id, name, discipline, primary_region, primary_muscle, pattern, pattern_subtype, compound,
               spinal_compression, bodyweight_possible, dumbbell_possible, kettlebell_possible,
               barbell_possible, machine_possible, band_possible, plate_or_med_ball_possible,
               is_complex_lift, is_unilateral
        FROM movements
        WHERE {discipline_where}
        AND is_complex_lift = true
        AND {equipment_where}
        ORDER BY RANDOM()
        LIMIT :limit
        """

        params = {"limit": max_movements}
        params.update(discipline_params)

        result = await self.db.execute(text(query), params)
        movements = result.fetchall()
        
        return self._format_movement_results(movements)
    
    def _build_equipment_filter(self, equipment_available: List[str]) -> str:
        """
        Build SQL WHERE clause for equipment availability using config mapping.
        
        Args:
            equipment_available: List of equipment types available to user
            
        Returns:
            SQL WHERE clause fragment for equipment filtering
        """
        if not equipment_available:
            return "true"
        
        equipment_filters = []
        for equipment in equipment_available:
            # Use config mapping to get correct database column name
            equipment_column = self._equipment_mapping.get(equipment)
            
            if equipment_column:
                equipment_filters.append(f"{equipment_column} = true")
            else:
                logger.warning(f"Equipment '{equipment}' not found in config mapping, skipping")
        
        if len(equipment_filters) == 1:
            return equipment_filters[0]
        elif len(equipment_filters) > 1:
            return f"({ ' OR '.join(equipment_filters) })"
        else:
            return "true"
    
    def _build_discipline_filter(self, disciplines: list[str]) -> tuple[str, dict]:
        """
        Build SQL WHERE clause for discipline filtering from config with parameter binding.

        Args:
            disciplines: List of discipline names

        Returns:
            Tuple of (SQL WHERE clause fragment, parameters dict)
        """
        if not disciplines:
            return "true", {}
        elif len(disciplines) == 1:
            return "discipline = :discipline", {"discipline": disciplines[0]}
        else:
            return "discipline IN :disciplines", {"disciplines": tuple(disciplines)}
    
    def _get_discipline_filter(self, session_type: str) -> tuple[str, dict]:
        """
        Get discipline filter based on session type from config with parameter binding.

        Args:
            session_type: Type of training session

        Returns:
            Tuple of (SQL WHERE clause fragment, parameters dict)
        """
        try:
            disciplines = self.config_loader.get_session_discipline_mapping(session_type)
            return self._build_discipline_filter(disciplines)
        except Exception as e:
            logger.error(f"Error getting discipline filter for session type '{session_type}': {e}")
            return "discipline = :discipline", {"discipline": "resistance training"}
    
    def _get_compound_filter(self, session_type: str) -> str:
        """
        Get compound filter based on session type.
        
        Args:
            session_type: Type of training session
            
        Returns:
            SQL WHERE clause fragment for compound filtering
        """
        if session_type == "mobility_only":
            return "(compound = false OR compound IS NULL)"
        elif session_type in ["resistance_accessory", "resistance_circuits", "hyrox_style"]:
            return "compound = true"
        else:
            return "true"
    
    def _format_movement_results(self, movements: Any) -> List[Dict[str, Any]]:
        """
        Format database results into movement dictionaries.
        
        Args:
            movements: Raw database result rows
            
        Returns:
            List of formatted movement dictionaries
        """
        return [
            {
                "id": row[0],
                "name": row[1],
                "discipline": row[2],
                "primary_region": row[3],
                "primary_muscle": row[4],
                "pattern": row[5],
                "pattern_subtype": row[6],  # New field
                "compound": row[7],
                "spinal_compression": row[8],
                "equipment_available": {
                    "bodyweight": row[9],
                    "dumbbell": row[10],
                    "kettlebell": row[11],
                    "barbell": row[12],
                    "machine": row[13],
                    "band": row[14],
                    "plate_or_med_ball": row[15]
                },
                "is_complex_lift": row[16] if len(row) > 16 else None,
                "is_unilateral": row[17] if len(row) > 17 else None,
                "regression_to_move": row[18] if len(row) > 18 else None,
                "progression_to_move": row[19] if len(row) > 19 else None,
                "metric_type": row[20] if len(row) > 20 else None
            }
            for row in movements
        ]