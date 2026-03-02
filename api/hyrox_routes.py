"""
Hyrox Workout API Routes for Alloy AI Fitness System.
Provides endpoints for searching, viewing, and recommending Hyrox workouts.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
import logging
import uuid
from datetime import datetime

from models.hyrox import (
    HyroxWorkoutType,
    HyroxWorkoutDetail,
    HyroxSearchResponse,
    HyroxRecommendRequest,
    HyroxWorkout,
)
from sqlalchemy.ext.asyncio import AsyncSession
from services.hyrox_workout_service import HyroxWorkoutService
from services.error_logger import log_validation_error
from config.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/hyrox", tags=["hyrox"])


# ---------------------------------------------------------------------------
# Dependency
# ---------------------------------------------------------------------------

async def get_hyrox_service(
    db: AsyncSession = Depends(get_db),
) -> HyroxWorkoutService:
    """Dependency injection for HyroxWorkoutService."""
    return HyroxWorkoutService(db_session=db)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/movements")
async def get_hyrox_movement_names(
    db: AsyncSession = Depends(get_db),
):
    """
    Return distinct movement names that appear in hyrox workout lines.
    Used to populate the 'Includes' filter in the Circuits search tab.
    """
    query = """
    SELECT DISTINCT movement_name
    FROM hyrox_workout_lines_staging
    WHERE movement_name IS NOT NULL AND movement_name != ''
    ORDER BY movement_name ASC
    """
    result = await db.execute(text(query))
    names = [str(row[0]) for row in result.fetchall()]
    return {"movement_names": names}


@router.get("/workouts", response_model=HyroxSearchResponse)
async def search_hyrox_workouts(
    workout_type: Optional[str] = Query(None, description="Filter by workout type (amrap, emom, for_time, etc.)"),
    min_duration: Optional[int] = Query(None, ge=1, description="Minimum duration in minutes"),
    max_duration: Optional[int] = Query(None, le=120, description="Maximum duration in minutes"),
    is_complex: Optional[bool] = Query(None, description="Filter by complexity"),
    has_mini_circuit: Optional[bool] = Query(None, description="Filter by has_mini_circuit"),
    includes: Optional[list[str]] = Query(None, description="Filter circuits that include specific movements"),
    excludes: Optional[list[str]] = Query(None, description="Exclude circuits that contain any of these movements"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    service: HyroxWorkoutService = Depends(get_hyrox_service),
):
    """
    Search and list Hyrox workouts with optional filters.

    Supports filtering by workout type, duration range, complexity, and mini circuit presence.
    Results are paginated.
    """
    trace_id = f"hyrox_search_{uuid.uuid4().hex[:12]}"

    try:
        logger.info(f"[{trace_id}] Searching Hyrox workouts: type={workout_type}, "
                     f"duration={min_duration}-{max_duration}min, complex={is_complex}")

        result = await service.search_workouts(
            workout_type=workout_type,
            min_duration_minutes=min_duration,
            max_duration_minutes=max_duration,
            is_complex=is_complex,
            has_mini_circuit=has_mini_circuit,
            includes=includes,
            excludes=excludes,
            page=page,
            per_page=per_page,
        )

        logger.info(f"[{trace_id}] Found {result.total} Hyrox workouts")
        return result

    except Exception as e:
        logger.error(f"[{trace_id}] Hyrox search failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "HYROX_SEARCH_FAILED",
                    "message": "Failed to search Hyrox workouts",
                    "details": str(e),
                    "trace_id": trace_id,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            },
        )


@router.get("/workouts/{workout_id}", response_model=HyroxWorkoutDetail)
async def get_hyrox_workout_detail(
    workout_id: int,
    service: HyroxWorkoutService = Depends(get_hyrox_service),
):
    """
    Get full Hyrox workout detail including movement lines and mini circuits.

    Returns the workout metadata, all movement lines (ordered by line_number),
    and mini circuits (ordered by circuit_number).
    """
    trace_id = f"hyrox_detail_{uuid.uuid4().hex[:12]}"

    try:
        logger.info(f"[{trace_id}] Fetching Hyrox workout detail: id={workout_id}")

        detail = await service.get_workout_detail(workout_id)

        if detail is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": {
                        "code": "HYROX_WORKOUT_NOT_FOUND",
                        "message": f"Hyrox workout with id {workout_id} not found",
                        "details": None,
                        "trace_id": trace_id,
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                },
            )

        logger.info(
            f"[{trace_id}] Returning workout '{detail.workout.name}' "
            f"with {len(detail.lines)} lines, {len(detail.mini_circuits)} circuits"
        )
        return detail

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[{trace_id}] Hyrox detail fetch failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "HYROX_DETAIL_FAILED",
                    "message": "Failed to fetch Hyrox workout detail",
                    "details": str(e),
                    "trace_id": trace_id,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            },
        )


@router.post("/workouts/recommend", response_model=Optional[HyroxWorkout])
async def recommend_hyrox_workout(
    request: HyroxRecommendRequest,
    service: HyroxWorkoutService = Depends(get_hyrox_service),
):
    """
    Recommend a Hyrox workout for a program session.

    Given session constraints (time budget, excluded IDs, usage counts),
    returns a suitable workout that fits the time budget and respects
    repeat limits. Returns null if no suitable workout is found.
    """
    trace_id = f"hyrox_recommend_{uuid.uuid4().hex[:12]}"

    try:
        logger.info(
            f"[{trace_id}] Recommending Hyrox workout: "
            f"duration={request.session_duration_minutes}min, "
            f"excluded={len(request.excluded_ids)} IDs, "
            f"type_pref={request.workout_type_preference}"
        )

        workout = await service.select_workout_for_session(
            session_duration_minutes=request.session_duration_minutes,
            excluded_ids=request.excluded_ids if request.excluded_ids else None,
            usage_counts=request.usage_counts,
            workout_type_preference=(
                request.workout_type_preference.value
                if request.workout_type_preference
                else None
            ),
        )

        if workout:
            logger.info(
                f"[{trace_id}] Recommended: '{workout.name}' "
                f"({workout.total_time_minutes}min, {workout.workout_type})"
            )
        else:
            logger.info(f"[{trace_id}] No suitable Hyrox workout found")

        return workout

    except Exception as e:
        logger.error(f"[{trace_id}] Hyrox recommendation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "HYROX_RECOMMEND_FAILED",
                    "message": "Failed to recommend Hyrox workout",
                    "details": str(e),
                    "trace_id": trace_id,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            },
        )


@router.get("/health")
async def hyrox_health_check():
    """Health check for the Hyrox workout service."""
    return {
        "status": "healthy",
        "service": "hyrox",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
    }
