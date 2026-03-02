from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from enum import Enum

from models.enums import (
    SessionType, BlockType, EquipmentType, PrimaryRegion, 
    SpinalCompression, DisciplineType, MetricType
)


class SessionMovement(BaseModel):
    """A single movement within a session block."""
    
    movement_id: int = Field(..., description="Database ID of the movement")
    movement_name: str = Field(..., description="Name of the movement")
    discipline: str = Field(..., description="Movement discipline (e.g., 'resistance training')")
    pattern_subtype: Optional[str] = Field(None, description="Pattern subtype (e.g., 'squat', 'hinge')")
    primary_region: str = Field(..., description="Primary muscle region targeted")
    primary_muscle: Optional[str] = Field(None, description="Primary muscle targeted")
    compound: Optional[bool] = Field(None, description="Whether this is a compound movement")
    sets: int = Field(..., ge=1, le=10, description="Number of sets")
    reps: str = Field(..., description="Rep range or count (e.g., '8-12' or '10')")
    rest_seconds: int = Field(..., ge=0, le=300, description="Rest between sets in seconds")
    equipment_used: Optional[str] = Field(None, description="Equipment used for this movement")
    notes: Optional[str] = Field(None, description="Additional coaching notes")
    order: int = Field(1, ge=1, description="Order of movement within the block")


class BlockConstraints(BaseModel):
    """Movement constraints for a session block."""
    
    compound: Optional[bool] = Field(None, description="Whether compound movements are allowed")
    spinal_compression: Optional[List[SpinalCompression]] = Field(None, description="Allowed spinal compression levels")
    disciplines: Optional[List[DisciplineType]] = Field(None, description="Allowed discipline types")
    equipment_types: Optional[List[EquipmentType]] = Field(None, description="Required equipment types")
    muscle_regions: Optional[List[PrimaryRegion]] = Field(None, description="Target muscle regions")
    metric_types: Optional[List[MetricType]] = Field(None, description="Allowed metric types")
    min_duration: int = Field(5, ge=1, description="Minimum block duration in minutes")
    max_duration: int = Field(15, le=120, description="Maximum block duration in minutes")


class SessionBlock(BaseModel):
    """A single block within a session (warmup, main, cooldown)."""
    
    block_type: BlockType = Field(..., description="Type of session block")
    session_type: Optional[SessionType] = Field(None, description="Session type for main blocks")
    duration_minutes: int = Field(..., ge=5, le=120, description="Block duration in minutes")
    constraints: BlockConstraints = Field(..., description="Movement constraints for this block")
    target_sets: Optional[int] = Field(None, ge=1, le=10, description="Target number of sets")
    target_reps: Optional[str] = Field(None, description="Target rep range (e.g., '8-12')")
    target_rest_seconds: Optional[int] = Field(None, ge=0, le=300, description="Target rest between sets")
    notes: Optional[str] = Field(None, description="Additional notes for this block")
    movements: List[SessionMovement] = Field(
        default_factory=list, description="Populated movements for this block"
    )


class SessionSkeleton(BaseModel):
    """Complete session skeleton with all blocks."""
    
    session_id: str = Field(..., description="Unique session identifier")
    day_number: int = Field(..., ge=1, le=7, description="Day of week (1=Monday, 7=Sunday)")
    session_focus: str = Field(..., description="Primary focus of this session")
    total_duration_minutes: int = Field(..., ge=5, le=120, description="Total session duration")
    blocks: List[SessionBlock] = Field(..., description="Session blocks in order")
    target_muscle_groups: Optional[List[PrimaryRegion]] = Field(
        None, description="Primary muscle groups to target"
    )
    session_type: SessionType = Field(..., description="Main session type")
    difficulty_level: str = Field("intermediate", description="Session difficulty level")
    hyrox_workout_id: Optional[int] = Field(
        None, description="ID of attached Hyrox workout from hyrox_workouts table"
    )
    hyrox_workout_name: Optional[str] = Field(
        None, description="Name of attached Hyrox workout for display"
    )


class WeeklyPlan(BaseModel):
    """Weekly training plan with session skeletons."""
    
    week_number: int = Field(..., ge=1, description="Week number in program")
    sessions: List[SessionSkeleton] = Field(..., description="Sessions for this week")
    total_sessions: int = Field(..., ge=1, le=7, description="Number of sessions this week")
    weekly_focus: str = Field(..., description="Primary focus for this week")
    total_training_time: int = Field(..., ge=60, le=840, description="Total weekly training time in minutes")
    rest_days: List[int] = Field(..., description="Days of week that are rest days (1-7)")


class ProgramBlock(BaseModel):
    """A training block within the program (e.g., strength focus phase)."""
    
    block_name: str = Field(..., description="Name of training block")
    block_number: int = Field(..., ge=1, description="Block number in sequence")
    weeks_duration: int = Field(..., ge=1, le=6, description="Duration of block in weeks")
    primary_goal: str = Field(..., description="Primary training goal for this block")
    weekly_plans: List[WeeklyPlan] = Field(..., description="Weekly plans for this block")
    block_focus: str = Field(..., description="Specific focus for this training block")
    intensity_progression: str = Field(..., description="How intensity progresses through block")


class ProgramSkeleton(BaseModel):
    """Complete program skeleton with all training blocks."""
    
    program_id: str = Field(..., description="Unique program identifier")
    user_id: str = Field(..., description="User identifier")
    program_name: str = Field(..., description="Program name")
    total_weeks: int = Field(..., ge=8, le=12, description="Total program duration in weeks")
    total_sessions: int = Field(..., ge=8, le=84, description="Total number of sessions")
    training_blocks: List[ProgramBlock] = Field(..., description="Training blocks in sequence")
    primary_goal: str = Field(..., description="Primary training goal")
    secondary_goals: List[str] = Field(..., description="Secondary training goals")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Program creation timestamp")
    
    # Computed fields
    @property
    def total_training_time(self) -> int:
        """Calculate total training time across all sessions."""
        return sum(
            week.total_training_time 
            for block in self.training_blocks 
            for week in block.weekly_plans
        )
    
    @property
    def average_session_duration(self) -> float:
        """Calculate average session duration."""
        total_sessions = sum(
            len(week.sessions) 
            for block in self.training_blocks 
            for week in block.weekly_plans
        )
        return self.total_training_time / total_sessions if total_sessions > 0 else 0
    
    @property
    def weekly_training_frequency(self) -> float:
        """Calculate average weekly training frequency."""
        return self.total_sessions / self.total_weeks if self.total_weeks > 0 else 0


class ProgramGenerationRequest(BaseModel):
    """Request for program skeleton generation."""
    
    user_id: str = Field(..., description="User identifier")
    normalized_goals: Dict[str, float] = Field(..., description="Normalized goal weights from onboarding")
    availability: Dict[str, Any] = Field(..., description="User availability configuration")
    available_equipment: List[EquipmentType] = Field(..., description="Available equipment")
    program_length_weeks: int = Field(..., ge=8, le=12, description="Program length in weeks")
    experience_level: str = Field("intermediate", description="User experience level")
    
    @field_validator('normalized_goals')
    @classmethod
    def validate_normalized_goals(cls, v: Dict[str, float]) -> Dict[str, float]:
        required_keys = [
            "primary_strength", "normalized_hypertrophy_fat_loss",
            "normalized_power_mobility", "strength_bias", "endurance_bias",
        ]
        for key in required_keys:
            if key not in v:
                raise ValueError(f"Missing required normalized goal key: {key}")
            if not 0.0 <= v[key] <= 1.0:
                raise ValueError(f"Goal value for {key} must be between 0.0 and 1.0")
        return v


class ProgramGenerationResponse(BaseModel):
    """Response from program skeleton generation."""
    
    success: bool = Field(..., description="Whether generation was successful")
    program_skeleton: Optional[ProgramSkeleton] = Field(
        default=None, description="Generated program skeleton"
    )
    errors: Optional[List[str]] = Field(
        default=None, description="Generation errors if any"
    )
    warnings: Optional[List[str]] = Field(
        default=None, description="Generation warnings"
    )
    session_breakdown: Optional[Dict[str, int]] = Field(
        default=None, description="Count of each session type"
    )
    
    model_config = ConfigDict(json_schema_extra={
        "examples": [{
            "success": True,
            "program_skeleton": {
                "program_id": "prog_123",
                "user_id": "user_456",
                "program_name": "Strength Focus Program",
                "total_weeks": 12,
                "total_sessions": 36,
                "primary_goal": "strength",
                "secondary_goals": ["hypertrophy", "power"],
            },
            "session_breakdown": {
                "resistance_accessory": 20,
                "resistance_circuits": 8,
                "mobility_only": 8,
            },
        }]
    })
