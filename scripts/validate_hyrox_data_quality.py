import json
import logging
import re
from typing import Dict, List, Any, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hyrox_validation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('hyrox_validator')

class ValidationLevel(Enum):
    CRITICAL = 'CRITICAL'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'

@dataclass
class ValidationResult:
    level: ValidationLevel
    category: str
    message: str
    workout_id: str = None
    field: str = None
    expected: Any = None
    actual: Any = None

class HyroxDataValidator:
    WORKOUT_TYPES = {
        'amrap': 'amrap',
        'emom': 'emom',
        'for time': 'for_time',
        'rounds for time': 'rounds_for_time',
        'for time, team': 'for_time_team',
        'for time, teams': 'for_time_teams',
        'for load': 'for_load',
        'chipper': 'chipper',
        'every minute on the minute': 'emom',
        'every x minutes': 'emom',
        'ladder': 'ladder',
        'ascending ladder': 'ladder',
        'descending ladder': 'ladder',
        'hyrox workout of week': 'unknown'
    }
    
    WORKOUT_GOALS = {
        'max rounds and reps': 'max_rounds_reps',
        'max rounds': 'max_rounds_reps',
        'max reps': 'max_reps',
        'max load': 'max_load',
        'finish quickly': 'finish_quickly',
        'time cap': 'time_cap',
        'max effort': 'max_effort',
        'pacing': 'pacing',
        'as written': 'as_written'
    }
    
    MOVEMENTS = [
        'wall ball shots', 'ski erg', 'lunges', 'burpees', 'v-ups',
        'run', 'row', 'sandbag lunges', 'hand release push-ups',
        'sled push', 'sled pull', 'farmer carry', 'burpee broad jumps',
        'sled drag', 'rope climb', 'box jump overs', 'box jumps',
        'jump rope', 'double unders', 'thrusters', 'toes to bar',
        'pull-ups', 'chest to bar', 'bar muscle-ups', 'ring dips',
        'kettlebell swings', 'kettlebell snatches', 'dumbbell snatches',
        'overhead lunges', 'air squats', 'front squats', 'back squats',
        'deadlifts', 'sumo deadlift high pull', 'power cleans',
        'push press', 'push jerk', 'snatch', 'clean and jerk',
        'wall walks', 'handstand push-ups', 'pike push-ups'
    ]
    
    def __init__(self, scraped_data: List[Dict], source_pages: Dict[str, str] = None):
        self.scraped_data = scraped_data
        self.source_pages = source_pages or {}
        self.results: List[ValidationResult] = []
        self.workout_urls = {w.get('wod_id'): w.get('url') for w in scraped_data}
    
    def validate_all(self) -> Tuple[int, int, int]:
        logger.info(f"Starting validation for {len(self.scraped_data)} workouts")
        
        total_errors = 0
        total_warnings = 0
        total_critical = 0
        
        for workout in self.scraped_data:
            workout_id = workout.get('wod_id')
            logger.info(f"Validating workout: {workout.get('name')} ({workout_id})")
            
            errors, warnings, critical = self._validate_workout(workout)
            total_errors += errors
            total_warnings += warnings
            total_critical += critical
        
        self._log_summary(total_errors, total_warnings, total_critical)
        return total_critical, total_errors, total_warnings
    
    def _validate_workout(self, workout: Dict) -> Tuple[int, int, int]:
        workout_id = workout.get('wod_id')
        errors = 0
        warnings = 0
        critical = 0
        
        errors += self._check_required_fields(workout)
        critical += self._check_duplicate_workout(workout)
        errors += self._validate_workout_details(workout)
        errors += self._validate_foreign_key_relationships(workout)
        warnings += self._validate_movements_parsed(workout)
        
        if workout_id in self.source_pages:
            errors += self._validate_against_source(workout, self.source_pages[workout_id])
        
        return errors, warnings, critical
    
    def _check_required_fields(self, workout: Dict) -> int:
        required_fields = ['wod_id', 'url', 'name', 'full_description']
        errors = 0
        
        for field in required_fields:
            if not workout.get(field):
                errors += 1
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    category='missing_field',
                    message=f"Required field '{field}' is missing or empty",
                    workout_id=workout.get('wod_id'),
                    field=field
                ))
                logger.error(f"Workout {workout.get('wod_id')}: Missing required field '{field}'")
        
        return errors
    
    def _check_duplicate_workout(self, workout: Dict) -> int:
        workout_id = workout.get('wod_id')
        duplicates = [w for w in self.scraped_data 
                    if w.get('wod_id') != workout_id and w.get('name') == workout.get('name')]
        
        if duplicates:
            dup_ids = [d.get('wod_id') for d in duplicates]
            self.results.append(ValidationResult(
                level=ValidationLevel.CRITICAL,
                category='duplicate',
                message=f"Duplicate workout found with same name",
                workout_id=workout_id,
                expected=f"Unique workout",
                actual=f"Duplicates: {dup_ids}"
            ))
            logger.critical(f"Workout {workout_id}: Duplicate found with IDs {dup_ids}")
            return 1
        return 0
    
    def _validate_workout_details(self, workout: Dict) -> int:
        errors = 0
        
        workout_type = workout.get('badge', '').lower()
        if workout_type and workout_type not in self.WORKOUT_TYPES:
            self.results.append(ValidationResult(
                level=ValidationLevel.ERROR,
                category='invalid_workout_type',
                message=f"Unknown workout type: {workout_type}",
                workout_id=workout.get('wod_id'),
                field='badge',
                expected=list(self.WORKOUT_TYPES.keys()),
                actual=workout_type
            ))
            errors += 1
            logger.error(f"Workout {workout.get('wod_id')}: Invalid workout type '{workout_type}'")
        
        time_spec = workout.get('time_specification', '')
        if time_spec and not self._is_valid_time_format(time_spec):
            self.results.append(ValidationResult(
                level=ValidationLevel.ERROR,
                category='malformed_time',
                message=f"Malformed time specification",
                workout_id=workout.get('wod_id'),
                field='time_specification',
                expected='Valid time format (e.g., "16 min", "20:00", "12:00 cap")',
                actual=time_spec
            ))
            errors += 1
            logger.error(f"Workout {workout.get('wod_id')}: Malformed time spec '{time_spec}'")
        
        description = workout.get('full_description', '')
        if description and len(description) < 10:
            self.results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                category='short_description',
                message=f"Description too short",
                workout_id=workout.get('wod_id'),
                field='full_description',
                expected='>= 10 characters',
                actual=len(description)
            ))
            logger.warning(f"Workout {workout.get('wod_id')}: Description too short ({len(description)} chars)")
        
        return errors
    
    def _validate_foreign_key_relationships(self, workout: Dict) -> int:
        errors = 0
        workout_id = workout.get('wod_id')
        
        lines = workout.get('parsed_lines', [])
        for line in lines:
            mini_circuit_id = line.get('mini_circuit_id')
            time_segment_id = line.get('time_segment_id')
            ladder_rung_id = line.get('ladder_rung_id')
            
            structure_refs = sum([
                1 if mini_circuit_id else 0,
                1 if time_segment_id else 0,
                1 if ladder_rung_id else 0
            ])
            
            if structure_refs > 1:
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    category='invalid_fk',
                    message=f"Line has multiple structure references",
                    workout_id=workout_id,
                    field='line_structure_fks',
                    expected='At most one structure FK',
                    actual=f"mini_circuit: {mini_circuit_id}, time_segment: {time_segment_id}, ladder_rung: {ladder_rung_id}"
                ))
                errors += 1
                logger.error(f"Workout {workout_id}: Line has multiple structure FKs")
        
        return errors
    
    def _validate_movements_parsed(self, workout: Dict) -> int:
        warnings = 0
        workout_id = workout.get('wod_id')
        
        lines = workout.get('parsed_lines', [])
        unknown_movements = set()
        
        for line in lines:
            movement = line.get('movement')
            if movement:
                movement_lower = movement.lower()
                matched = any(m.lower() in movement_lower for m in self.MOVEMENTS)
                if not matched and not line.get('is_rest'):
                    unknown_movements.add(movement)
        
        if unknown_movements:
            self.results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                category='unknown_movement',
                message=f"Unrecognized movement names found",
                workout_id=workout_id,
                field='movement_name',
                expected='Known movement',
                actual=list(unknown_movements)
            ))
            warnings += len(unknown_movements)
            logger.warning(f"Workout {workout_id}: Unknown movements: {unknown_movements}")
        
        return warnings
    
    def _validate_against_source(self, workout: Dict, source_content: str) -> int:
        errors = 0
        workout_id = workout.get('wod_id')
        
        if workout.get('name') not in source_content:
            self.results.append(ValidationResult(
                level=ValidationLevel.ERROR,
                category='source_mismatch',
                message=f"Workout name not found in source",
                workout_id=workout_id,
                field='name',
                expected=workout.get('name'),
                actual='Not found in source'
            ))
            errors += 1
            logger.error(f"Workout {workout_id}: Name not found in source")
        
        badge = workout.get('badge', '')
        if badge and badge not in source_content.lower():
            self.results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                category='source_mismatch',
                message=f"Workout type badge not found in source",
                workout_id=workout_id,
                field='badge',
                expected=badge,
                actual='Not found in source'
            ))
            errors += 1
            logger.warning(f"Workout {workout_id}: Badge '{badge}' not found in source")
        
        return errors
    
    def _is_valid_time_format(self, time_spec: str) -> bool:
        patterns = [
            r'^\d+\s+min$',
            r'^\d+\s+mins?$',
            r'^\d+:\d{2}$',
            r'^\d+:\d{2}\s+cap$',
            r'^\d+\s+min\s+cap$'
        ]
        return any(re.match(p, time_spec.lower()) for p in patterns)
    
    def _log_summary(self, errors: int, warnings: int, critical: int):
        logger.info("=" * 60)
        logger.info("VALIDATION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total workouts validated: {len(self.scraped_data)}")
        logger.info(f"Critical issues: {critical}")
        logger.info(f"Errors: {errors}")
        logger.info(f"Warnings: {warnings}")
        logger.info(f"Total issues: {critical + errors + warnings}")
        
        if critical == 0 and errors == 0:
            logger.info("✓ All validations passed!")
        else:
            logger.warning(f"✗ {critical + errors} issues need to be resolved")
        
        logger.info("=" * 60)
    
    def export_report(self, filename: str = 'hyrox_validation_report.json'):
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_workouts': len(self.scraped_data),
            'summary': {
                'critical': sum(1 for r in self.results if r.level == ValidationLevel.CRITICAL),
                'errors': sum(1 for r in self.results if r.level == ValidationLevel.ERROR),
                'warnings': sum(1 for r in self.results if r.level == ValidationLevel.WARNING)
            },
            'results': [
                {
                    'level': r.level.value,
                    'category': r.category,
                    'message': r.message,
                    'workout_id': r.workout_id,
                    'field': r.field,
                    'expected': str(r.expected) if r.expected else None,
                    'actual': str(r.actual) if r.actual else None
                }
                for r in self.results
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Validation report exported to {filename}")

def load_scraped_data(filename: str) -> List[Dict]:
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {filename}")
        return []

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        logger.error("Usage: python validate_hyrox_data_quality.py <scraped_data.json> [source_pages.json]")
        sys.exit(1)
    
    scraped_file = sys.argv[1]
    source_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    scraped_data = load_scraped_data(scraped_file)
    if not scraped_data:
        logger.error("No scraped data found")
        sys.exit(1)
    
    source_pages = {}
    if source_file:
        with open(source_file, 'r') as f:
            source_pages = json.load(f)
    
    validator = HyroxDataValidator(scraped_data, source_pages)
    critical, errors, warnings = validator.validate_all()
    validator.export_report()
    
    sys.exit(0 if critical == 0 and errors == 0 else 1)
