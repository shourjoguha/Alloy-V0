"""
Hyrox Workout Service for Alloy AI Fitness System.
Provides search, detail retrieval, and intelligent selection of pre-built
Hyrox workouts from the hyrox_workouts_staging / hyrox_workout_lines_staging /
hyrox_mini_circuits_staging production tables.

Read-only — no writes. Data is populated by the scraping/migration pipeline.
"""

import math
import logging
from typing import List, Optional, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from models.hyrox import (
    HyroxWorkout,
    HyroxWorkoutLine,
    HyroxMiniCircuit,
    HyroxWorkoutDetail,
    HyroxSearchResponse,
)
from utils.config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class HyroxWorkoutService:
    """Service for querying and selecting Hyrox workouts."""

    def __init__(
        self,
        db_session: AsyncSession,
        config_loader: Optional[ConfigLoader] = None,
    ):
        """
        Initialize with database session and configuration.

        Args:
            db_session: SQLAlchemy async session for database queries.
            config_loader: Optional ConfigLoader instance. Creates default if None.
        """
        self.db = db_session
        self.config_loader = config_loader or ConfigLoader()
        self._selection_config = self.config_loader.get_hyrox_workout_selection_config()
        logger.info("HyroxWorkoutService initialized")

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    async def search_workouts(
        self,
        workout_type: Optional[str] = None,
        min_duration_minutes: Optional[int] = None,
        max_duration_minutes: Optional[int] = None,
        is_complex: Optional[bool] = None,
        has_mini_circuit: Optional[bool] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> HyroxSearchResponse:
        """
        Search hyrox_workouts_staging with optional filters. Paginated.

        Args:
            workout_type: Filter by hyrox_workout_type enum value.
            min_duration_minutes: Minimum total_time_minutes.
            max_duration_minutes: Maximum total_time_minutes.
            is_complex: Filter by is_complex flag.
            has_mini_circuit: Filter by has_mini_circuit flag.
            page: 1-indexed page number.
            per_page: Results per page (max 100).

        Returns:
            HyroxSearchResponse with workouts list and pagination metadata.
        """
        conditions: list[str] = []
        params: dict[str, Any] = {}

        if workout_type is not None:
            conditions.append("w.workout_type = :workout_type")
            params["workout_type"] = workout_type

        if min_duration_minutes is not None:
            conditions.append("w.total_time_minutes >= :min_dur")
            params["min_dur"] = min_duration_minutes

        if max_duration_minutes is not None:
            conditions.append("w.total_time_minutes <= :max_dur")
            params["max_dur"] = max_duration_minutes

        if is_complex is not None:
            conditions.append("w.is_complex = :is_complex")
            params["is_complex"] = is_complex

        if has_mini_circuit is not None:
            conditions.append("w.has_mini_circuit = :has_mini_circuit")
            params["has_mini_circuit"] = has_mini_circuit

        where_clause = " AND ".join(conditions) if conditions else "true"

        # Count query
        count_query = f"""
        SELECT COUNT(*)
        FROM hyrox_workouts_staging w
        WHERE {where_clause}
        """
        count_result = await self.db.execute(text(count_query), params)
        total = count_result.scalar() or 0

        # Data query
        offset = (page - 1) * per_page
        data_query = f"""
        SELECT w.*
        FROM hyrox_workouts_staging w
        WHERE {where_clause}
        ORDER BY w.name ASC
        LIMIT :limit OFFSET :offset
        """
        params["limit"] = per_page
        params["offset"] = offset

        result = await self.db.execute(text(data_query), params)
        rows = result.mappings().all()

        workouts = [self._row_to_workout(row) for row in rows]
        total_pages = math.ceil(total / per_page) if per_page > 0 else 0

        return HyroxSearchResponse(
            workouts=workouts,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
        )

    # ------------------------------------------------------------------
    # Detail
    # ------------------------------------------------------------------

    async def get_workout_detail(self, workout_id: int) -> Optional[HyroxWorkoutDetail]:
        """
        Fetch a complete Hyrox workout with lines and mini circuits.

        Args:
            workout_id: Primary key of hyrox_workouts_staging row.

        Returns:
            HyroxWorkoutDetail or None if not found.
        """
        # Workout
        workout_result = await self.db.execute(
            text("SELECT * FROM hyrox_workouts_staging WHERE id = :id"),
            {"id": workout_id},
        )
        workout_row = workout_result.mappings().first()
        if not workout_row:
            return None

        workout = self._row_to_workout(workout_row)

        # Lines (ordered)
        lines_result = await self.db.execute(
            text(
                "SELECT * FROM hyrox_workout_lines_staging "
                "WHERE workout_id = :wid ORDER BY line_number ASC"
            ),
            {"wid": workout_id},
        )
        lines = [self._row_to_line(r) for r in lines_result.mappings().all()]

        # Mini circuits (ordered)
        circuits_result = await self.db.execute(
            text(
                "SELECT * FROM hyrox_mini_circuits_staging "
                "WHERE workout_id = :wid ORDER BY circuit_number ASC"
            ),
            {"wid": workout_id},
        )
        mini_circuits = [
            self._row_to_mini_circuit(r) for r in circuits_result.mappings().all()
        ]

        return HyroxWorkoutDetail(
            workout=workout, lines=lines, mini_circuits=mini_circuits
        )

    # ------------------------------------------------------------------
    # Selection for program generation
    # ------------------------------------------------------------------

    async def select_workout_for_session(
        self,
        session_duration_minutes: int,
        excluded_ids: Optional[List[int]] = None,
        usage_counts: Optional[Dict[int, int]] = None,
        workout_type_preference: Optional[str] = None,
    ) -> Optional[HyroxWorkout]:
        """
        Select a Hyrox workout for a full HYROX_STYLE session.

        Selection criteria:
        1. total_time_minutes within session_duration ± time_tolerance
        2. workout_type in session_eligible_workout_types
        3. Exclude workouts that have hit max_repeats_per_program
        4. Random selection for variety

        Args:
            session_duration_minutes: Available time budget for the Hyrox workout.
            excluded_ids: Workout IDs that should be fully excluded.
            usage_counts: Map of workout_id → times already used in program.
            workout_type_preference: Optional preferred workout_type.

        Returns:
            HyroxWorkout or None if no suitable workout found.
        """
        if not self._selection_config.get("enabled", True):
            logger.info("Hyrox workout selection is disabled via config")
            return None

        return await self._select_workout(
            time_budget=session_duration_minutes,
            eligible_types=self._selection_config.get("session_eligible_workout_types", []),
            excluded_ids=excluded_ids,
            usage_counts=usage_counts,
            workout_type_preference=workout_type_preference,
        )

    async def select_workout_for_accessory_block(
        self,
        accessory_duration_minutes: int,
        excluded_ids: Optional[List[int]] = None,
        usage_counts: Optional[Dict[int, int]] = None,
    ) -> Optional[HyroxWorkout]:
        """
        Select a short Hyrox workout for the accessory portion of a resistance day.

        Uses a tighter time constraint: workout must fit within
        accessory_block_max_duration_minutes from config.

        Args:
            accessory_duration_minutes: Available time for the accessory block.
            excluded_ids: Workout IDs that should be fully excluded.
            usage_counts: Map of workout_id → times already used in program.

        Returns:
            HyroxWorkout or None if no suitable short workout found.
        """
        if not self._selection_config.get("enabled", True):
            return None

        max_dur = min(
            accessory_duration_minutes,
            self._selection_config.get("accessory_block_max_duration_minutes", 15),
        )

        return await self._select_workout(
            time_budget=max_dur,
            eligible_types=self._selection_config.get("accessory_eligible_workout_types", []),
            excluded_ids=excluded_ids,
            usage_counts=usage_counts,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _select_workout(
        self,
        time_budget: int,
        eligible_types: list[str],
        excluded_ids: Optional[List[int]] = None,
        usage_counts: Optional[Dict[int, int]] = None,
        workout_type_preference: Optional[str] = None,
    ) -> Optional[HyroxWorkout]:
        """
        Core selection query shared by session and accessory selectors.
        """
        tolerance = self._selection_config.get("time_tolerance_minutes", 5)
        max_repeats = self._selection_config.get("max_repeats_per_program", 2)

        conditions: list[str] = [
            "total_time_minutes IS NOT NULL",
            "total_time_minutes >= :min_time",
            "total_time_minutes <= :max_time",
        ]
        params: dict[str, Any] = {
            "min_time": max(1, time_budget - tolerance),
            "max_time": time_budget + tolerance,
        }

        # Eligible workout types
        if eligible_types:
            type_placeholders = ", ".join([f":etype_{i}" for i in range(len(eligible_types))])
            conditions.append(f"workout_type IN ({type_placeholders})")
            for i, t in enumerate(eligible_types):
                params[f"etype_{i}"] = t

        # Exclude fully blocked IDs
        if excluded_ids:
            id_placeholders = ", ".join([f":exid_{i}" for i in range(len(excluded_ids))])
            conditions.append(f"id NOT IN ({id_placeholders})")
            for i, eid in enumerate(excluded_ids):
                params[f"exid_{i}"] = eid

        # Exclude workouts that have hit max repeats
        if usage_counts:
            over_limit_ids = [wid for wid, count in usage_counts.items() if count >= max_repeats]
            if over_limit_ids:
                ol_placeholders = ", ".join([f":olid_{i}" for i in range(len(over_limit_ids))])
                conditions.append(f"id NOT IN ({ol_placeholders})")
                for i, ol_id in enumerate(over_limit_ids):
                    params[f"olid_{i}"] = ol_id

        # Optional type preference (boost, don't exclude others)
        order_clause = "RANDOM()"
        if workout_type_preference:
            order_clause = (
                f"CASE WHEN workout_type = :pref_type THEN 0 ELSE 1 END, RANDOM()"
            )
            params["pref_type"] = workout_type_preference

        where_clause = " AND ".join(conditions)

        query = f"""
        SELECT *
        FROM hyrox_workouts_staging
        WHERE {where_clause}
        ORDER BY {order_clause}
        LIMIT 1
        """

        result = await self.db.execute(text(query), params)
        row = result.mappings().first()

        if row:
            workout = self._row_to_workout(row)
            logger.info(
                f"Selected Hyrox workout: id={workout.id}, name={workout.name}, "
                f"type={workout.workout_type}, duration={workout.total_time_minutes}min"
            )
            return workout

        logger.info(
            f"No Hyrox workout found for time_budget={time_budget}min "
            f"(±{tolerance}min), types={eligible_types}"
        )
        return None

    # ------------------------------------------------------------------
    # Row mapping helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_workout(row: Any) -> HyroxWorkout:
        """Map a database row (mapping) to HyroxWorkout model."""
        return HyroxWorkout(
            id=row["id"],
            wod_id=row.get("wod_id"),
            name=row["name"],
            url=row["url"],
            badge=row.get("badge"),
            workout_type=row.get("workout_type", "unknown"),
            workout_goal=row.get("workout_goal"),
            time_specification=row.get("time_specification"),
            total_time_minutes=row.get("total_time_minutes"),
            time_cap_minutes=row.get("time_cap_minutes"),
            total_rounds=row.get("total_rounds"),
            has_buy_in=row.get("has_buy_in", False),
            has_cash_out=row.get("has_cash_out", False),
            is_complex=row.get("is_complex", False),
            has_mini_circuit=row.get("has_mini_circuit", False),
            full_description=row.get("full_description"),
            scraped_at=row.get("scraped_at"),
            source_page=row.get("source_page"),
            status=row.get("status", "pending_review"),
            notes=row.get("notes"),
        )

    @staticmethod
    def _row_to_line(row: Any) -> HyroxWorkoutLine:
        """Map a database row (mapping) to HyroxWorkoutLine model."""
        return HyroxWorkoutLine(
            id=row["id"],
            workout_id=row["workout_id"],
            line_number=row["line_number"],
            line_text=row["line_text"],
            is_rest=row.get("is_rest", False),
            is_buy_in=row.get("is_buy_in", False),
            is_cash_out=row.get("is_cash_out", False),
            movement_name=row.get("movement_name"),
            reps=row.get("reps"),
            distance_meters=row.get("distance_meters"),
            duration_seconds=row.get("duration_seconds"),
            weight_male=row.get("weight_male"),
            weight_female=row.get("weight_female"),
            calories=row.get("calories"),
            is_max_effort=row.get("is_max_effort", False),
            notes=row.get("notes"),
            mini_circuit_id=row.get("mini_circuit_id"),
            created_at=row.get("created_at"),
        )

    @staticmethod
    def _row_to_mini_circuit(row: Any) -> HyroxMiniCircuit:
        """Map a database row (mapping) to HyroxMiniCircuit model."""
        return HyroxMiniCircuit(
            id=row["id"],
            workout_id=row["workout_id"],
            circuit_number=row["circuit_number"],
            circuit_type=row.get("circuit_type", "unknown"),
            rounds=row.get("rounds"),
            start_time=row.get("start_time"),
            end_time=row.get("end_time"),
            duration_minutes=row.get("duration_minutes"),
            rest_after_minutes=row.get("rest_after_minutes"),
            notes=row.get("notes"),
            created_at=row.get("created_at"),
        )
