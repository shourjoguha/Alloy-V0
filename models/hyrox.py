"""
Hyrox Workout Models for Alloy AI Fitness System.
Pydantic models mirroring the hyrox_workouts_staging, hyrox_workout_lines_staging,
and hyrox_mini_circuits_staging production tables.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, time
from enum import Enum


class HyroxWorkoutType(str, Enum):
    """Workout structure types from hyrox_workout_type enum."""
    AMRAP = "amrap"
    EMOM = "emom"
    FOR_TIME = "for_time"
    ROUNDS_FOR_TIME = "rounds_for_time"
    FOR_LOAD = "for_load"
    BUY_IN = "buy_in"
    CASH_OUT = "cash_out"
    TIME_CAP = "time_cap"
    LADDER = "ladder"
    MINI_CIRCUIT = "mini_circuit"
    EXPLICIT_TIME_GUIDANCE = "explicit_time_guidance"
    UNKNOWN = "unknown"


class HyroxWorkoutGoal(str, Enum):
    """Workout goal types from hyrox_workout_goal enum (display only, not for selection)."""
    MAX_ROUNDS_REPS = "max_rounds_reps"
    FINISH_QUICKLY = "finish_quickly"
    COMPLETE_ROUNDS = "complete_rounds"
    MAX_LOAD = "max_load"
    PACE_WORK = "pace_work"
    ENDURANCE = "endurance"
    STRENGTH = "strength"
    MIXED = "mixed"
    UNKNOWN = "unknown"


class HyroxStatus(str, Enum):
    """Workflow status for scraped workouts."""
    PENDING_REVIEW = "pending_review"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    REJECTED = "rejected"


# ---------------------------------------------------------------------------
# Table models
# ---------------------------------------------------------------------------

class HyroxWorkoutLine(BaseModel):
    """Single movement line within a Hyrox workout (mirrors hyrox_workout_lines_staging)."""

    id: int = Field(..., description="Line ID")
    workout_id: int = Field(..., description="Parent workout ID")
    line_number: int = Field(..., description="Sequence number in workout")
    line_text: str = Field(..., description="Original description line text")
    is_rest: bool = Field(False, description="Whether this is a rest period")
    is_buy_in: bool = Field(False, description="Part of buy-in section")
    is_cash_out: bool = Field(False, description="Part of cash-out section")
    movement_name: Optional[str] = Field(None, description="Normalized movement name")
    reps: Optional[int] = Field(None, description="Number of repetitions")
    distance_meters: Optional[float] = Field(None, description="Distance in meters")
    duration_seconds: Optional[int] = Field(None, description="Duration in seconds")
    weight_male: Optional[float] = Field(None, description="Male weight (lb)")
    weight_female: Optional[float] = Field(None, description="Female weight (lb)")
    calories: Optional[int] = Field(None, description="Calorie target")
    is_max_effort: bool = Field(False, description="Max effort movement")
    notes: Optional[str] = Field(None, description="Parsing notes")
    mini_circuit_id: Optional[int] = Field(None, description="FK to hyrox_mini_circuits_staging")
    created_at: Optional[datetime] = Field(None, description="Record creation time")


class HyroxMiniCircuit(BaseModel):
    """Sub-circuit within a Hyrox workout (mirrors hyrox_mini_circuits_staging).

    Workouts with has_mini_circuit=True contain one or more circuits.
    Each circuit groups a subset of workout lines and defines round/time structure.
    """

    id: int = Field(..., description="Mini circuit ID")
    workout_id: int = Field(..., description="Parent workout ID")
    circuit_number: int = Field(..., description="Order within the workout (1-indexed)")
    circuit_type: HyroxWorkoutType = Field(..., description="Circuit structure type")
    rounds: Optional[int] = Field(None, description="Number of rounds for this circuit")
    start_time: Optional[time] = Field(None, description="Start time (for timed segments)")
    end_time: Optional[time] = Field(None, description="End time (for timed segments)")
    duration_minutes: Optional[int] = Field(None, description="Duration in minutes")
    rest_after_minutes: Optional[int] = Field(None, description="Rest after circuit (minutes)")
    notes: Optional[str] = Field(None, description="Circuit description/notes")
    created_at: Optional[datetime] = Field(None, description="Record creation time")


class HyroxWorkout(BaseModel):
    """Hyrox workout metadata (mirrors hyrox_workouts_staging table)."""

    id: int = Field(..., description="Workout ID")
    wod_id: Optional[str] = Field(None, description="URL slug identifier")
    name: str = Field(..., description="Workout name")
    url: str = Field(..., description="Full URL to workout")
    badge: Optional[str] = Field(None, description="Badge text")
    workout_type: HyroxWorkoutType = Field(
        HyroxWorkoutType.UNKNOWN, description="Workout structure type"
    )
    workout_goal: Optional[HyroxWorkoutGoal] = Field(
        None, description="Workout goal (display only)"
    )
    time_specification: Optional[str] = Field(None, description="Time spec text")
    total_time_minutes: Optional[int] = Field(None, description="Total workout duration")
    time_cap_minutes: Optional[int] = Field(None, description="Time cap if any")
    total_rounds: Optional[int] = Field(None, description="Total rounds for round-based workouts")
    has_buy_in: bool = Field(False, description="Has buy-in section")
    has_cash_out: bool = Field(False, description="Has cash-out section")
    is_complex: bool = Field(False, description="Has mini circuits/ladders/segments")
    has_mini_circuit: bool = Field(False, description="Contains sub-circuits")
    full_description: Optional[str] = Field(None, description="Full workout text")
    scraped_at: Optional[datetime] = Field(None, description="Scrape timestamp")
    source_page: Optional[str] = Field(None, description="Source page identifier")
    status: HyroxStatus = Field(
        HyroxStatus.PENDING_REVIEW, description="Review status"
    )
    notes: Optional[str] = Field(None, description="Manual notes")


class HyroxWorkoutDetail(BaseModel):
    """Full Hyrox workout with lines and mini circuits for UI rendering."""

    workout: HyroxWorkout = Field(..., description="Workout metadata")
    lines: List[HyroxWorkoutLine] = Field(
        default_factory=list, description="Movement lines ordered by line_number"
    )
    mini_circuits: List[HyroxMiniCircuit] = Field(
        default_factory=list, description="Sub-circuits ordered by circuit_number"
    )


# ---------------------------------------------------------------------------
# Search / Recommend request/response models
# ---------------------------------------------------------------------------

class HyroxSearchRequest(BaseModel):
    """Query parameters for searching Hyrox workouts."""

    workout_type: Optional[HyroxWorkoutType] = Field(
        None, description="Filter by workout structure type"
    )
    min_duration_minutes: Optional[int] = Field(
        None, ge=1, description="Minimum total time"
    )
    max_duration_minutes: Optional[int] = Field(
        None, le=120, description="Maximum total time"
    )
    is_complex: Optional[bool] = Field(
        None, description="Filter by complexity flag"
    )
    has_mini_circuit: Optional[bool] = Field(
        None, description="Filter by has_mini_circuit flag"
    )
    page: int = Field(1, ge=1, description="Page number")
    per_page: int = Field(20, ge=1, le=100, description="Items per page")


class HyroxSearchResponse(BaseModel):
    """Paginated search results."""

    workouts: List[HyroxWorkout] = Field(
        default_factory=list, description="Matching workouts"
    )
    total: int = Field(0, description="Total matching count")
    page: int = Field(1, description="Current page")
    per_page: int = Field(20, description="Items per page")
    total_pages: int = Field(0, description="Total pages")


class HyroxRecommendRequest(BaseModel):
    """Request body for workout recommendation."""

    session_duration_minutes: int = Field(
        ..., ge=5, le=120, description="Available time for the Hyrox portion"
    )
    excluded_ids: List[int] = Field(
        default_factory=list, description="Workout IDs already used in the program"
    )
    usage_counts: Optional[dict[int, int]] = Field(
        None, description="Map of workout_id -> times used in current program"
    )
    workout_type_preference: Optional[HyroxWorkoutType] = Field(
        None, description="Optional preference for workout type"
    )
