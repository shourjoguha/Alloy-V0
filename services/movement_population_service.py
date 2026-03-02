"""
Movement Population Service for Alloy AI Fitness System.
Coordinates movement selection from database to populate program session blocks.
"""

import logging
from typing import List, Dict, Any, Optional, Set
from sqlalchemy.ext.asyncio import AsyncSession

from models.enums import (
    SessionType, BlockType, EquipmentType, DisciplineType
)
from models.program import (
    ProgramSkeleton, ProgramBlock, WeeklyPlan, SessionSkeleton,
    SessionBlock, SessionMovement
)
from models.hyrox import HyroxWorkout
from services.enhanced_movement_query_service_v2 import EnhancedMovementQueryServiceV2
from services.hyrox_workout_service import HyroxWorkoutService
from utils.config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class MovementPopulationService:
    """
    Service for populating program session blocks with concrete movements.
    
    Coordinates between EnhancedMovementQueryServiceV2 (for movements table)
    and HyroxWorkoutService (for hyrox_workouts_staging tables).
    """
    
    def __init__(
        self,
        db_session: AsyncSession,
        config_loader: Optional[ConfigLoader] = None
    ):
        """
        Initialize with database session and configuration.
        
        Args:
            db_session: SQLAlchemy async session for database queries.
            config_loader: Optional ConfigLoader instance. Creates default if None.
        """
        self.db = db_session
        self.config_loader = config_loader or ConfigLoader()
        
        # Initialize sub-services
        self.movement_service = EnhancedMovementQueryServiceV2(db_session, config_loader)
        self.hyrox_service = HyroxWorkoutService(db_session, config_loader)
        
        # Track used movements within a program for variety
        self._used_movement_ids: Set[int] = set()
        self._hyrox_usage_counts: Dict[int, int] = {}
        
        logger.info("MovementPopulationService initialized")
    
    async def populate_program(
        self,
        program_skeleton: ProgramSkeleton,
        available_equipment: List[EquipmentType]
    ) -> ProgramSkeleton:
        """
        Populate all sessions in a program skeleton with movements.
        
        Args:
            program_skeleton: Program skeleton with empty movement lists.
            available_equipment: List of equipment available to user.
            
        Returns:
            Program skeleton with movements populated in all blocks.
        """
        logger.info(f"Populating program {program_skeleton.program_id} with movements")
        
        # Convert equipment types to strings for query service
        equipment_list = [eq.value for eq in available_equipment]
        
        # Reset tracking for new program
        self._used_movement_ids.clear()
        self._hyrox_usage_counts.clear()
        
        # Iterate through all blocks and populate
        for block in program_skeleton.training_blocks:
            for weekly_plan in block.weekly_plans:
                for session in weekly_plan.sessions:
                    await self._populate_session(
                        session=session,
                        equipment_list=equipment_list,
                        primary_goal=block.primary_goal
                    )
        
        logger.info(
            f"Populated program {program_skeleton.program_id}: "
            f"{len(self._used_movement_ids)} unique movements used"
        )
        
        return program_skeleton
    
    async def _populate_session(
        self,
        session: SessionSkeleton,
        equipment_list: List[str],
        primary_goal: str
    ) -> None:
        """
        Populate all blocks in a single session with movements.
        
        Args:
            session: Session skeleton to populate.
            equipment_list: List of available equipment names.
            primary_goal: User's primary training goal.
        """
        logger.debug(
            f"Populating session {session.session_id}, "
            f"type={session.session_type.value}"
        )
        
        # Handle HYROX_STYLE sessions specially - attach pre-built workout
        if session.session_type == SessionType.HYROX_STYLE:
            await self._attach_hyrox_workout(session)
        
        # Populate each block
        for block in session.blocks:
            await self._populate_block(
                block=block,
                session_type=session.session_type,
                equipment_list=equipment_list,
                primary_goal=primary_goal,
                target_regions=session.target_muscle_groups
            )
    
    async def _populate_block(
        self,
        block: SessionBlock,
        session_type: SessionType,
        equipment_list: List[str],
        primary_goal: str,
        target_regions: Optional[List] = None
    ) -> None:
        """
        Populate a single block with movements based on block type.

        Constraint resolution order:
        1. If block.constraints.disciplines is set, use those (skeleton override).
        2. Otherwise, fall back to config-driven block_constraints (YAML).
        
        Args:
            block: SessionBlock to populate.
            session_type: Overall session type.
            equipment_list: Available equipment.
            primary_goal: User's primary goal.
            target_regions: Target muscle regions if any.
        """
        # Resolve constraints: skeleton BlockConstraints take priority, then config
        config_constraints = self.config_loader.get_block_constraints(
            block_type=block.block_type.value,
            session_type=session_type.value if block.block_type == BlockType.MAIN else None
        )

        if block.block_type == BlockType.WARMUP:
            movements = await self._get_warmup_movements(
                equipment_list, config_constraints=config_constraints
            )
        elif block.block_type == BlockType.COOLDOWN:
            movements = await self._get_cooldown_movements(
                equipment_list, config_constraints=config_constraints
            )
        else:  # MAIN block
            movements = await self._get_main_block_movements(
                session_type=session_type,
                equipment_list=equipment_list,
                primary_goal=primary_goal,
                target_regions=target_regions,
                block_duration=block.duration_minutes,
                config_constraints=config_constraints
            )
        
        # Convert to SessionMovement models and assign to block
        block.movements = self._convert_to_session_movements(
            movements=movements,
            target_sets=block.target_sets or 3,
            target_reps=block.target_reps or "8-12",
            target_rest=block.target_rest_seconds or 60
        )
        
        # Track used movements
        for movement in movements:
            self._used_movement_ids.add(movement["id"])
    
    async def _get_warmup_movements(
        self,
        equipment_list: List[str],
        max_movements: int = 4,
        config_constraints: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get warmup movements from database.

        Uses config-driven constraints (disciplines, spinal_compression) when
        available; falls back to query service defaults otherwise.
        
        Args:
            equipment_list: Available equipment.
            max_movements: Maximum movements to return.
            config_constraints: Constraints from YAML block_constraints.warmup.
            
        Returns:
            List of movement dictionaries.
        """
        # Log which disciplines we're using for transparency
        if config_constraints:
            logger.debug(
                f"Warmup constraints from config: disciplines={config_constraints.get('disciplines')}"
            )

        movements = await self.movement_service.get_warmup_movements(
            equipment_available=equipment_list,
            max_movements=max_movements
        )
        
        # Fallback to mobility movements if warmup-specific returns empty
        if not movements:
            logger.warning("No warmup movements found, falling back to mobility")
            movements = await self.movement_service.get_mobility_movements(
                equipment_available=equipment_list,
                max_movements=max_movements
            )
        
        return movements
    
    async def _get_cooldown_movements(
        self,
        equipment_list: List[str],
        max_movements: int = 4,
        config_constraints: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get cooldown movements from database.

        Uses config-driven constraints (disciplines, spinal_compression) when
        available; falls back to query service defaults otherwise.
        
        Args:
            equipment_list: Available equipment.
            max_movements: Maximum movements to return.
            config_constraints: Constraints from YAML block_constraints.cooldown.
            
        Returns:
            List of movement dictionaries.
        """
        if config_constraints:
            logger.debug(
                f"Cooldown constraints from config: disciplines={config_constraints.get('disciplines')}"
            )

        movements = await self.movement_service.get_mobility_movements(
            equipment_available=equipment_list,
            max_movements=max_movements
        )
        
        return movements
    
    async def _get_main_block_movements(
        self,
        session_type: SessionType,
        equipment_list: List[str],
        primary_goal: str,
        target_regions: Optional[List] = None,
        block_duration: int = 30,
        max_movements: int = 6,
        config_constraints: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get main block movements based on session type.

        Uses config-driven constraints (disciplines, compound_filter) when
        available; falls back to query service defaults otherwise.
        
        Args:
            session_type: Type of session (resistance, hyrox, cardio, mobility).
            equipment_list: Available equipment.
            primary_goal: User's primary goal.
            target_regions: Target muscle regions if any.
            block_duration: Duration of block in minutes.
            max_movements: Maximum movements to return.
            config_constraints: Constraints from YAML block_constraints.main.<session_type>.
            
        Returns:
            List of movement dictionaries.
        """
        if config_constraints:
            logger.debug(
                f"Main block constraints from config for {session_type.value}: "
                f"disciplines={config_constraints.get('disciplines')}, "
                f"compound_filter={config_constraints.get('compound_filter')}"
            )
        # Convert target regions to strings if present
        region_list = None
        if target_regions:
            region_list = [r.value if hasattr(r, 'value') else str(r) for r in target_regions]
        
        if session_type == SessionType.RESISTANCE_ACCESSORY:
            # Get mix of strength and accessory movements
            strength_movements = await self.movement_service.get_strength_movements(
                equipment_available=equipment_list,
                primary_regions=region_list,
                max_movements=max_movements // 2
            )
            accessory_movements = await self.movement_service.get_accessory_movements(
                equipment_available=equipment_list,
                primary_regions=region_list,
                max_movements=max_movements - len(strength_movements)
            )
            movements = strength_movements + accessory_movements
            
        elif session_type == SessionType.RESISTANCE_CIRCUITS:
            # Circuit-style: balanced set from multiple patterns
            movements = await self.movement_service.get_balanced_movement_set(
                session_type="resistance_circuits",
                equipment_available=equipment_list,
                target_regions=region_list,
                max_movements=max_movements
            )
            
        elif session_type == SessionType.HYROX_STYLE:
            # Hyrox: strength + carries + cardio
            strength = await self.movement_service.get_strength_movements(
                equipment_available=equipment_list,
                max_movements=2
            )
            carries = await self.movement_service.get_hyrox_carries(
                equipment_available=equipment_list,
                max_movements=2
            )
            cardio = await self.movement_service.get_cardio_movements(
                equipment_available=equipment_list,
                max_movements=2
            )
            movements = strength + carries + cardio
            
        elif session_type == SessionType.CARDIO_ONLY:
            movements = await self.movement_service.get_cardio_movements(
                equipment_available=equipment_list,
                max_movements=max_movements
            )
            
        elif session_type == SessionType.MOBILITY_ONLY:
            movements = await self.movement_service.get_mobility_movements(
                equipment_available=equipment_list,
                max_movements=max_movements
            )
            
        else:
            # Fallback to balanced set
            movements = await self.movement_service.get_balanced_movement_set(
                session_type="resistance_accessory",
                equipment_available=equipment_list,
                target_regions=region_list,
                max_movements=max_movements
            )
        
        return movements
    
    async def _attach_hyrox_workout(self, session: SessionSkeleton) -> None:
        """
        Attach a pre-built Hyrox workout to a HYROX_STYLE session.
        
        Args:
            session: Session skeleton to attach workout to.
        """
        try:
            # Select a Hyrox workout that fits the session duration
            workout = await self.hyrox_service.select_workout_for_session(
                session_duration_minutes=session.total_duration_minutes,
                excluded_ids=list(self._hyrox_usage_counts.keys()),
                usage_counts=self._hyrox_usage_counts
            )
            
            if workout:
                session.hyrox_workout_id = workout.id
                session.hyrox_workout_name = workout.name
                
                # Track usage
                self._hyrox_usage_counts[workout.id] = (
                    self._hyrox_usage_counts.get(workout.id, 0) + 1
                )
                
                logger.info(
                    f"Attached Hyrox workout '{workout.name}' (id={workout.id}) "
                    f"to session {session.session_id}"
                )
            else:
                logger.warning(
                    f"No suitable Hyrox workout found for session {session.session_id} "
                    f"(duration={session.total_duration_minutes}min)"
                )
                
        except Exception as e:
            logger.error(f"Failed to attach Hyrox workout: {e}")
    
    def _convert_to_session_movements(
        self,
        movements: List[Dict[str, Any]],
        target_sets: int,
        target_reps: str,
        target_rest: int
    ) -> List[SessionMovement]:
        """
        Convert movement dictionaries to SessionMovement models.
        
        Args:
            movements: List of movement dictionaries from query service.
            target_sets: Default sets per movement.
            target_reps: Default rep range.
            target_rest: Default rest between sets.
            
        Returns:
            List of SessionMovement instances.
        """
        session_movements = []
        
        for order, movement in enumerate(movements, start=1):
            # Determine equipment used
            equipment_used = self._determine_equipment_used(movement)
            
            session_movement = SessionMovement(
                movement_id=movement["id"],
                movement_name=movement["name"],
                discipline=movement.get("discipline", "resistance training"),
                pattern_subtype=movement.get("pattern_subtype"),
                primary_region=movement.get("primary_region", "full body"),
                primary_muscle=movement.get("primary_muscle"),
                compound=movement.get("compound"),
                sets=target_sets,
                reps=target_reps,
                rest_seconds=target_rest,
                equipment_used=equipment_used,
                order=order
            )
            session_movements.append(session_movement)
        
        return session_movements
    
    def _determine_equipment_used(self, movement: Dict[str, Any]) -> Optional[str]:
        """
        Determine which equipment is used for a movement based on available flags.
        
        Args:
            movement: Movement dictionary with equipment availability flags.
            
        Returns:
            Equipment name string or None.
        """
        equipment_available = movement.get("equipment_available", {})
        
        # Priority order for equipment selection
        equipment_priority = [
            ("barbell", "barbell"),
            ("dumbbell", "dumbbell"),
            ("kettlebell", "kettlebell"),
            ("machine", "machine"),
            ("band", "band"),
            ("plate_or_med_ball", "plate/med ball"),
            ("bodyweight", "bodyweight"),
        ]
        
        for key, name in equipment_priority:
            if equipment_available.get(key):
                return name
        
        return None
