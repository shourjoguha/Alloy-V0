"""
Load scraped Hyrox workout data into staging tables
Reads JSON output from scraper and populates staging tables.
"""

import json
import psycopg2
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Default configuration
DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = "5434"
DEFAULT_DB_NAME = "Jacked-DB"
DEFAULT_DB_USER = "jacked"
DEFAULT_DB_PASS = "jackedpass"

def get_db_connection():
    """Get database connection using env vars or defaults"""
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", DEFAULT_DB_HOST),
        port=os.environ.get("DB_PORT", DEFAULT_DB_PORT),
        database=os.environ.get("DB_NAME", DEFAULT_DB_NAME),
        user=os.environ.get("DB_USER", DEFAULT_DB_USER),
        password=os.environ.get("DB_PASS", DEFAULT_DB_PASS)
    )

def load_json_data(file_path: str) -> Dict:
    """Load JSON data from file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_time_string(time_str: Optional[str]) -> Optional[str]:
    """Convert time string (e.g., '10:00') to HH:MM:SS format for Postgres TIME type"""
    if not time_str:
        return None
    try:
        # Check if it's already in a recognizable format
        parts = time_str.split(':')
        if len(parts) == 2:
            # Assume MM:SS, prepend 00: for hours
            return f"00:{time_str}"
        elif len(parts) == 3:
            # Assume HH:MM:SS
            return time_str
        return None
    except Exception:
        return None

def load_workouts_to_staging(json_data: Dict) -> None:
    """Load workouts from JSON data to staging tables"""
    conn = get_db_connection()
    conn.autocommit = False
    cursor = conn.cursor()
    
    workouts = json_data.get('workouts', [])
    session_id = json_data.get('metadata', {}).get('session_id', 'unknown')
    
    print(f"Loading {len(workouts)} workouts from session {session_id}...")
    
    try:
        for workout in workouts:
            # 1. Insert Workout
            cursor.execute("""
                INSERT INTO hyrox_workouts_staging (
                    wod_id, name, url, badge, workout_type, workout_goal,
                    time_specification, total_time_minutes, time_cap_minutes,
                    has_buy_in, has_cash_out, is_complex, full_description,
                    scraped_at, source_page, status, notes,
                    total_rounds, has_mini_circuit
                ) VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s
                ) RETURNING id
            """, (
                workout.get('wod_id'),
                workout.get('name'),
                workout.get('url'),
                workout.get('badge'),
                workout.get('workout_type', 'unknown'),
                workout.get('workout_goal', 'unknown'),
                workout.get('time_specification'),
                workout.get('total_time_minutes'),
                workout.get('time_cap_minutes'),
                workout.get('has_buy_in', False),
                workout.get('has_cash_out', False),
                workout.get('is_complex', False),
                workout.get('full_description'),
                workout.get('scraped_at') or datetime.now(),
                workout.get('source_page', 'hyrox_workouts'),
                'pending_review',
                workout.get('notes'),
                workout.get('total_rounds'),
                bool(workout.get('mini_circuits'))  # has_mini_circuit
            ))
            
            workout_id = cursor.fetchone()[0]
            
            # Map for line associations
            # line_number -> {'mini_circuit_id': id}
            line_associations = {}
            
            # 2. Insert Mini Circuits
            for circuit in workout.get('mini_circuits', []):
                cursor.execute("""
                    INSERT INTO hyrox_mini_circuits_staging (
                        workout_id, circuit_number, circuit_type, rounds, notes,
                        start_time, end_time
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
                """, (
                    workout_id,
                    circuit.get('circuit_number'),
                    'mini_circuit', # defaulting type
                    circuit.get('rounds'),
                    circuit.get('description'),
                    parse_time_string(circuit.get('start_time')),
                    parse_time_string(circuit.get('end_time'))
                ))
                circuit_id = cursor.fetchone()[0]
                
                # Associate lines
                for move in circuit.get('movements', []):
                    ln = move.get('raw_line_number')
                    if ln is not None:
                        if ln not in line_associations: line_associations[ln] = {}
                        line_associations[ln]['mini_circuit_id'] = circuit_id

            # 3. Insert Workout Lines
            for line in workout.get('description_lines', []):
                line_number = line.get('raw_line_number', 0)
                assoc = line_associations.get(line_number, {})
                
                # Handle weights (prefer kg, fallback to lb converted)
                w_m = line.get('weight_male_kg')
                if w_m is None and line.get('weight_male_lb'):
                    w_m = float(line.get('weight_male_lb')) * 0.453592
                    
                w_f = line.get('weight_female_kg')
                if w_f is None and line.get('weight_female_lb'):
                    w_f = float(line.get('weight_female_lb')) * 0.453592

                cursor.execute("""
                    INSERT INTO hyrox_workout_lines_staging (
                        workout_id, line_number, line_text,
                        is_rest, is_buy_in, is_cash_out, is_max_effort,
                        movement_name, reps, distance_meters,
                        duration_seconds, weight_male, weight_female, calories,
                        mini_circuit_id
                    ) VALUES (
                        %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s,
                        %s, %s, %s, %s,
                        %s
                    )
                """, (
                    workout_id,
                    line_number,
                    line.get('text'),
                    line.get('is_rest', False),
                    line.get('is_buy_in', False),
                    line.get('is_cash_out', False),
                    line.get('is_max_effort', False),
                    line.get('movement_name'),
                    line.get('reps'),
                    line.get('distance_meters'),
                    line.get('duration_seconds'),
                    w_m,
                    w_f,
                    line.get('calories'),
                    assoc.get('mini_circuit_id')
                ))

        conn.commit()
        print(f"Successfully loaded {len(workouts)} workouts into staging tables.")
        
    except Exception as e:
        conn.rollback()
        print(f"Error loading data: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_hyrox_json_to_staging.py <path_to_json_file>")
        sys.exit(1)
        
    json_file = sys.argv[1]
    if not os.path.exists(json_file):
        print(f"File not found: {json_file}")
        sys.exit(1)
        
    data = load_json_data(json_file)
    load_workouts_to_staging(data)
