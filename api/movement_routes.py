"""
Movement Search API Routes for Alloy AI Fitness System.
Provides endpoints for searching and filtering movements from the movements table.
"""

from fastapi import APIRouter, Depends, Query
from typing import Optional, List
import logging
import math

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from config.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/movements", tags=["movements"])


# ---------------------------------------------------------------------------
# Response models (kept lightweight — no Pydantic ORM for raw SQL queries)
# ---------------------------------------------------------------------------

def _row_to_dict(row) -> dict:
    """Convert a SQLAlchemy Row to a plain dict."""
    return dict(row._mapping)


# ---------------------------------------------------------------------------
# GET /api/movements/search
# ---------------------------------------------------------------------------

@router.get("/search")
async def search_movements(
    q: Optional[str] = Query(None, description="Text search on movement name"),
    primary_region: Optional[List[str]] = Query(None, description="Filter by primary_region (multi-select)"),
    primary_muscle: Optional[List[str]] = Query(None, description="Filter by primary_muscle (multi-select)"),
    discipline: Optional[List[str]] = Query(None, description="Filter by discipline (multi-select)"),
    compound: Optional[bool] = Query(None, description="Filter by compound flag"),
    is_complex_lift: Optional[bool] = Query(None, description="Filter by is_complex_lift flag"),
    is_unilateral: Optional[bool] = Query(None, description="Filter by is_unilateral flag"),
    metric_type: Optional[List[str]] = Query(None, description="Filter by metric_type (multi-select)"),
    spinal_compression: Optional[List[str]] = Query(None, description="Filter by spinal_compression (multi-select)"),
    equipment: Optional[List[str]] = Query(None, description="Filter by equipment availability (bodyweight, dumbbell, kettlebell, barbell, machine, band, plate_or_med_ball)"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
):
    """
    Search and filter movements with optional parameters.
    All filters are optional; default returns all movements paginated.
    Enum filters accept multiple values (multi-select) and use IN clause.
    """
    conditions: list[str] = []
    params: dict = {}

    # Text search on name (case-insensitive ILIKE)
    if q:
        conditions.append("name ILIKE :q")
        params["q"] = f"%{q}%"

    # Multi-select enum filters (IN clause with tuple binding)
    _multi_filters = {
        "primary_region": primary_region,
        "primary_muscle": primary_muscle,
        "discipline": discipline,
        "metric_type": metric_type,
        "spinal_compression": spinal_compression,
    }
    for col, values in _multi_filters.items():
        if values:
            placeholders = ", ".join(f":{col}_{i}" for i in range(len(values)))
            conditions.append(f"{col} IN ({placeholders})")
            for i, v in enumerate(values):
                params[f"{col}_{i}"] = v

    # Boolean filters
    if compound is not None:
        conditions.append("compound = :compound")
        params["compound"] = compound

    if is_complex_lift is not None:
        conditions.append("is_complex_lift = :is_complex_lift")
        params["is_complex_lift"] = is_complex_lift

    if is_unilateral is not None:
        conditions.append("is_unilateral = :is_unilateral")
        params["is_unilateral"] = is_unilateral

    # Equipment filter — show movements where ANY selected equipment is possible (OR logic)
    if equipment:
        equipment_col_map = {
            "bodyweight": "bodyweight_possible",
            "dumbbell": "dumbbell_possible",
            "kettlebell": "kettlebell_possible",
            "barbell": "barbell_possible",
            "machine": "machine_possible",
            "band": "band_possible",
            "plate_or_med_ball": "plate_or_med_ball_possible",
        }
        eq_conditions = []
        for eq in equipment:
            col = equipment_col_map.get(eq)
            if col:
                eq_conditions.append(f"{col} = true")
        if eq_conditions:
            conditions.append(f"({' OR '.join(eq_conditions)})")

    where_clause = " AND ".join(conditions) if conditions else "true"
    offset = (page - 1) * per_page

    # Count query
    count_query = f"SELECT COUNT(*) FROM movements WHERE {where_clause}"
    count_result = await db.execute(text(count_query), params)
    total = count_result.scalar() or 0

    # Data query
    data_query = f"""
    SELECT id, name, primary_muscle, primary_region, compound, is_complex_lift,
           is_unilateral, metric_type, spinal_compression,
           bodyweight_possible, dumbbell_possible, kettlebell_possible,
           barbell_possible, machine_possible, band_possible, plate_or_med_ball_possible,
           discipline, pattern
    FROM movements
    WHERE {where_clause}
    ORDER BY name ASC
    LIMIT :limit OFFSET :offset
    """
    params["limit"] = per_page
    params["offset"] = offset

    result = await db.execute(text(data_query), params)
    rows = result.fetchall()

    return {
        "movements": [_row_to_dict(row) for row in rows],
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": math.ceil(total / per_page) if total > 0 else 0,
    }


# ---------------------------------------------------------------------------
# GET /api/movements/filters
# ---------------------------------------------------------------------------

@router.get("/filters")
async def get_movement_filters(
    db: AsyncSession = Depends(get_db),
):
    """
    Return distinct values for each filterable column.
    Used to dynamically populate filter dropdowns in the UI.
    """
    filter_queries = {
        "primary_region": "SELECT DISTINCT primary_region FROM movements WHERE primary_region IS NOT NULL ORDER BY primary_region",
        "primary_muscle": "SELECT DISTINCT primary_muscle FROM movements WHERE primary_muscle IS NOT NULL ORDER BY primary_muscle",
        "discipline": "SELECT DISTINCT discipline FROM movements WHERE discipline IS NOT NULL ORDER BY discipline",
        "metric_type": "SELECT DISTINCT metric_type FROM movements WHERE metric_type IS NOT NULL ORDER BY metric_type",
        "spinal_compression": "SELECT DISTINCT spinal_compression FROM movements WHERE spinal_compression IS NOT NULL ORDER BY spinal_compression",
    }

    filters: dict = {}
    for key, query in filter_queries.items():
        result = await db.execute(text(query))
        filters[key] = [str(row[0]) for row in result.fetchall()]

    # Equipment is a fixed list of boolean columns
    filters["equipment"] = [
        "bodyweight", "dumbbell", "kettlebell", "barbell",
        "machine", "band", "plate_or_med_ball",
    ]

    return filters


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@router.get("/health")
async def movements_health_check():
    """Health check for the movements service."""
    return {"status": "healthy", "service": "movements"}
