from enum import Enum
from typing import Dict, List


class GoalType(str, Enum):
    """Primary goal types for the hierarchical sliders."""
    STRENGTH = "strength"
    ENDURANCE = "endurance"
    HYPERTROPHY = "hypertrophy"
    FAT_LOSS = "fat_loss"
    POWER = "power"
    MOBILITY = "mobility"


class SessionType(str, Enum):
    """Mutually exclusive main block session types."""
    RESISTANCE_ACCESSORY = "resistance_accessory"
    RESISTANCE_CIRCUITS = "resistance_circuits"
    HYROX_STYLE = "hyrox_style"
    MOBILITY_ONLY = "mobility_only"
    CARDIO_ONLY = "cardio_only"


class BlockType(str, Enum):
    """Session block types."""
    WARMUP = "warmup"
    MAIN = "main"
    COOLDOWN = "cooldown"


class EquipmentType(str, Enum):
    """Equipment types from existing database schema."""
    BODYWEIGHT = "bodyweight"
    DUMBBELL = "dumbbell"
    KETTLEBELL = "kettlebell"
    BARBELL = "barbell"
    MACHINE = "machine"
    BAND = "band"
    PLATE_MED_BALL = "plate_or_med_ball"


class PrimaryRegion(str, Enum):
    """Primary muscle regions from ACTUAL database schema."""
    ANTERIOR_LOWER = "anterior lower"      # Front of legs
    POSTERIOR_LOWER = "posterior lower"    # Back of legs
    SHOULDER = "shoulder"                  # Shoulders
    ANTERIOR_UPPER = "anterior upper"      # Front upper body
    POSTERIOR_UPPER = "posterior upper"    # Back upper body
    FULL_BODY = "full body"                # Full body
    LOWER_BODY = "lower body"              # Lower body (general)
    UPPER_BODY = "upper body"              # Upper body (general)
    CORE = "core"                          # Core


class SpinalCompression(str, Enum):
    """Spinal compression levels from existing database."""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class DisciplineType(str, Enum):
    """Discipline types from existing database."""
    RESISTANCE_TRAINING = "resistance training"  # For both strength & hypertrophy
    ENDURANCE = "endurance"
    POWER = "power"
    MOBILITY = "mobility"
    MIXED = "mixed"
    HYPERTROPHY = "hypertrophy"  # Keep for internal mapping, not in DB
    OLYMPIC = "olympic"
    CROSSFIT = "crossfit"
    ATHLETIC = "athletic"
    STRETCH = "stretch"
    CARDIO = "cardio"

    # Database-valid discipline values for validation
    DB_VALID_DISCIPLINES = {
        "resistance training",
        "endurance", 
        "power",
        "mobility",
        "mixed",
        "olympic",
        "crossfit",
        "athletic",
        "stretch",
        "cardio"
    }


class MetricType(str, Enum):
    """Metric types from existing database."""
    REPS = "reps"
    TIME = "time"
    DISTANCE = "distance"
    WEIGHT = "weight"


class PrimaryMuscle(str, Enum):
    """Primary muscle groups from existing database schema."""
    QUADRICEPS = "quadriceps"
    HAMSTRINGS = "hamstrings"
    GLUTES = "glutes"
    CALVES = "calves"
    CHEST = "chest"
    LATS = "lats"
    UPPER_BACK = "upper_back"
    REAR_DELTS = "rear_delts"
    FRONT_DELTS = "front_delts"
    SIDE_DELTS = "side_delts"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    FOREARMS = "forearms"
    CORE = "core"
    OBLIQUES = "obliques"
    LOWER_BACK = "lower_back"
    HIP_FLEXORS = "hip_flexors"
    ADDUCTORS = "adductors"
    ABDUCTORS = "abductors"
    FULL_BODY = "full_body"


class PatternType(str, Enum):
    """Movement pattern types from existing database schema."""
    SQUAT = "squat"
    HINGE = "hinge"
    LUNGE = "lunge"
    CARRY = "carry"
    ROTATION = "rotation"
    CORE = "core"
    MOBILITY = "mobility"
    HORIZONTAL_PUSH = "horizontal_push"
    HORIZONTAL_PULL = "horizontal_pull"
    VERTICAL_PUSH = "vertical_push"
    VERTICAL_PULL = "vertical_pull"


# Mapping function for our internal logic
REGION_MAPPING = {
    "anterior lower": "legs",
    "posterior lower": "legs", 
    "shoulder": "arms",
    "anterior upper": "upper_body",
    "posterior upper": "upper_body",
    "full body": "full_body",
    "lower body": "lower_body",
    "upper body": "upper_body",
    "core": "core"
}


def map_db_region_to_internal(db_region: str) -> str:
    """Map database region to our internal muscle group logic."""
    return REGION_MAPPING.get(db_region, db_region)


def get_internal_muscle_group(db_region: str) -> str:
    """Get internal muscle group name from database region."""
    return REGION_MAPPING.get(db_region, db_region)


def validate_discipline_value(discipline: str) -> bool:
    """Validate that a discipline value exists in the database."""
    return discipline in DisciplineType.DB_VALID_DISCIPLINES


def get_db_discipline_values(disciplines: List[DisciplineType]) -> List[str]:
    """Convert enum disciplines to database string values."""
    return [discipline.value for discipline in disciplines]


class MovementConstraint:
    """Movement constraints for different block types."""
    
    WARMUP_CONSTRAINTS = {
        "compound": False,  # Only non-compound movements
        "spinal_compression": [SpinalCompression.NONE.value, SpinalCompression.LOW.value],
        "discipline": ["mobility", "stretch", "athletic"],  # DB string values
        "movement_name_patterns": ["jump", "leap", "hop", "mobility", "stretch"]
    }
    
    COOLDOWN_CONSTRAINTS = {
        "compound": False,
        "spinal_compression": [SpinalCompression.NONE.value, SpinalCompression.LOW.value],
        "discipline": ["mobility", "stretch"],  # DB string values
        "movement_name_patterns": ["stretch", "mobility", "foam_roll"]
    }
    
    MAIN_BLOCK_CONSTRAINTS = {
        SessionType.RESISTANCE_ACCESSORY: {
            "compound": True,
            "discipline": ["resistance training", "hypertrophy"],  # DB string values
            "compound_filter": True  # Only compound for strength section
        },
        SessionType.RESISTANCE_CIRCUITS: {
            "compound": True,
            "discipline": ["resistance training", "crossfit"],  # DB string values
            "compound_filter": None  # All movements for accessory section
        },
        SessionType.HYROX_STYLE: {
            "compound": True,
            "discipline": ["resistance training", "cardio", "athletic"],  # DB string values
            "compound_filter": None
        },
        SessionType.MOBILITY_ONLY: {
            "compound": False,
            "discipline": ["mobility", "stretch"],  # DB string values
            "compound_filter": False
        },
        SessionType.CARDIO_ONLY: {
            "compound": False,
            "discipline": [DisciplineType.CARDIO, DisciplineType.ATHLETIC],
            "compound_filter": False
        }
    }


# Session type to discipline mapping for database queries
SESSION_TO_DISCIPLINE_MAPPING = {
    SessionType.RESISTANCE_ACCESSORY: [DisciplineType.RESISTANCE_TRAINING, DisciplineType.HYPERTROPHY],
    SessionType.RESISTANCE_CIRCUITS: [DisciplineType.RESISTANCE_TRAINING, DisciplineType.CROSSFIT],
    SessionType.HYROX_STYLE: [DisciplineType.RESISTANCE_TRAINING, DisciplineType.CARDIO, DisciplineType.ATHLETIC],
    SessionType.MOBILITY_ONLY: [DisciplineType.MOBILITY, DisciplineType.STRETCH],
    SessionType.CARDIO_ONLY: [DisciplineType.CARDIO, DisciplineType.ATHLETIC]
}


# Plyometric detection logic
def is_plyometric_movement(movement_name: str, discipline: str) -> bool:
    """
    Detect plyometric movements based on real database patterns.
    """
    # From database analysis: athletic discipline + jump/leap/hop keywords
    if discipline == DisciplineType.ATHLETIC:
        name_lower = movement_name.lower()
        if any(keyword in name_lower for keyword in ["jump", "leap", "hop"]):
            return True
    return False


def is_mobility_appropriate(discipline: str) -> bool:
    """
    Determine if movement is appropriate for mobility-focused days.
    """
    return discipline in [DisciplineType.MOBILITY, DisciplineType.STRETCH, DisciplineType.ATHLETIC]


def is_olympic_appropriate(session_type: str, user_level: str) -> bool:
    """
    Olympic lifts should only be used in main blocks for strength work
    with appropriate user experience level.
    """
    return (session_type in [SessionType.RESISTANCE_ACCESSORY, SessionType.RESISTANCE_CIRCUITS] 
            and user_level in ["intermediate", "advanced"])