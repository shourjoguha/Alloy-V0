"""
Load scraped Hyrox workout data into staging tables
"""

import json
import re
import psycopg2
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse

DATABASE_URL = "postgresql://jacked:jackedpass@localhost:5434/Jacked-DB"

WORKOUT_TYPES = {
    'amrap': 'amrap',
    'emom': 'emom',
    'for time': 'for_time',
    'rounds for time': 'rounds_for_time',
    'rft': 'rounds_for_time',
    'buy-in': 'buy_in',
    'cash-out': 'cash_out',
    'time cap': 'time_cap',
    'ladder': 'ladder',
    'mini circuit': 'mini_circuit',
    'explicit time': 'explicit_time_guidance'
}

WORKOUT_GOALS = {
    'as many rounds as possible': 'max_rounds_reps',
    'as quickly as possible': 'finish_quickly',
    'finish as quickly as possible': 'finish_quickly',
    'complete all rounds': 'complete_rounds',
    'complete': 'complete_rounds',
    'build up to heaviest': 'max_load',
    'for load': 'max_load',
    'pace work': 'pace_work',
    'max effort': 'pace_work'
}


def extract_workout_type(text: str) -> str:
    text_lower = text.lower()
    for pattern, workout_type in WORKOUT_TYPES.items():
        if pattern in text_lower:
            return workout_type
    return 'unknown'


def extract_workout_goal(text: str) -> str:
    text_lower = text.lower()
    for pattern, goal in WORKOUT_GOALS.items():
        if pattern in text_lower:
            return goal
    return 'unknown'


def extract_total_minutes(text: str) -> Optional[int]:
    minutes_match = re.search(r'(\d+)\s*min(?:ute)?s?', text, re.IGNORECASE)
    if minutes_match:
        return int(minutes_match.group(1))
    time_match = re.search(r'(\d+):(\d+)', text)
    if time_match:
        hours = int(time_match.group(1))
        minutes = int(time_match.group(2))
        return hours * 60 + minutes
    return None


def extract_time_cap(text: str) -> Optional[int]:
    cap_patterns = [
        r'time\s*cap\s*[:\s]*(\d+)\s*min(?:ute)?s?',
        r'cap\s*[:\s]*(\d+)\s*min(?:ute)?s?',
    ]
    for pattern in cap_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None


def detect_complex_workout(text: str) -> bool:
    complex_indicators = [
        'mini circuit',
        'ladder',
        'time segment',
        'then',
        'after that',
        'followed by',
        'buy-in',
        'cash-out'
    ]
    text_lower = text.lower()
    return any(indicator in text_lower for indicator in complex_indicators)


def parse_movement_line(text: str) -> Dict:
    movements = [
        'wall ball shots', 'ski erg', 'lunges', 'burpees', 'v-ups',
        'run', 'row', 'sandbag lunges', 'hand release push-ups',
        'farmer\'s carry', 'sit-ups', 'push-ups', 'pull-ups',
        'kettlebell swings', 'box jumps', 'double unders', 'squat cleans',
        'deadlifts', 'thrusters', 'toes to bar', 'chest to bar',
        'muscle-ups', 'power cleans', 'snatches', 'back squats',
        'devil presses', 'air squats', 'burpee broad jumps', 'sled push', 'sled pull'
    ]
    
    text_lower = text.lower()
    movement = None
    for mov in movements:
        if mov in text_lower:
            movement = mov
            break
    
    reps_match = re.search(r'^(\d+)\s+(?!meter|cal|lb|kg)', text, re.IGNORECASE)
    reps = int(reps_match.group(1)) if reps_match else None
    
    distance_match = re.search(r'(\d+)\s*meters?\s*(run|row)?', text, re.IGNORECASE)
    distance = int(distance_match.group(1)) if distance_match else None
    
    duration_match = re.search(r'(\d+)\s*sec(?:ond)?s?', text, re.IGNORECASE)
    duration = int(duration_match.group(1)) if duration_match else None
    
    weight_match = re.search(r'(\d+)\s*(lb|kg)', text, re.IGNORECASE)
    weight = {'value': int(weight_match.group(1)), 'unit': weight_match.group(2).lower()} if weight_match else None
    
    calorie_match = re.search(r'(\d+)\s*cal(?:ories)?', text, re.IGNORECASE)
    calories = int(calorie_match.group(1)) if calorie_match else None
    
    return {
        'movement': movement,
        'reps': reps,
        'distance_m': distance,
        'duration_seconds': duration,
        'weight_value': weight['value'] if weight else None,
        'weight_unit': weight['unit'] if weight else None,
        'calories': calories
    }


def load_workouts_to_staging(workouts: List[Dict]) -> None:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()
    
    try:
        session_id = str(datetime.now().timestamp())
        
        for workout in workouts:
            wod_id = workout.get('wod_id')
            full_desc = workout.get('full_description', '')
            
            workout_type = extract_workout_type(full_desc)
            workout_goal = extract_workout_goal(full_desc)
            total_time = extract_total_minutes(full_desc)
            time_cap = extract_time_cap(full_desc)
            has_buy_in = 'buy-in' in full_desc.lower()
            has_cash_out = 'cash-out' in full_desc.lower()
            is_complex = detect_complex_workout(full_desc)
            
            cursor.execute("""
                INSERT INTO hyrox_workouts_staging (
                    wod_id, name, url, badge, workout_type, workout_goal,
                    time_specification, total_time_minutes, time_cap_minutes,
                    has_buy_in, has_cash_out, is_complex, background_image,
                    favorites_count, comments_count, full_description,
                    source_page
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                wod_id,
                workout.get('name'),
                workout.get('url'),
                workout.get('badge'),
                workout_type,
                workout_goal,
                None,
                total_time,
                time_cap,
                has_buy_in,
                has_cash_out,
                is_complex,
                workout.get('background_image'),
                workout.get('stats', {}).get('favorites', 0),
                workout.get('stats', {}).get('comments', 0),
                full_desc,
                'hyrox_workouts'
            ))
            
            workout_staging_id = cursor.fetchone()[0]
            
            for line in workout.get('description_lines', []):
                if not line.strip():
                    continue
                
                movement_data = parse_movement_line(line)
                
                cursor.execute("""
                    INSERT INTO hyrox_workout_lines_staging (
                        workout_id, line_text, line_number,
                        is_rest, movement_name, reps, distance_meters,
                        duration_seconds, weight_text, calories
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    workout_staging_id,
                    line,
                    0,
                    'rest' in line.lower(),
                    movement_data.get('movement'),
                    movement_data.get('reps'),
                    movement_data.get('distance_m'),
                    movement_data.get('duration_seconds'),
                    (str(movement_data.get('weight_value')) + (movement_data.get('weight_unit') or '')) if movement_data.get('weight_value') else None,
                    movement_data.get('calories')
                ))
            
            cursor.execute("""
                INSERT INTO hyrox_workout_tags_staging (
                    workout_id, tag_name
                ) VALUES (%s, %s)
            """, (workout_staging_id, 'hyrox'))
            
            if workout.get('badge'):
                cursor.execute("""
                    INSERT INTO hyrox_workout_tags_staging (
                        workout_id, tag_name
                    ) VALUES (%s, %s)
                """, (workout_staging_id, workout['badge']))
        
        cursor.execute("""
            INSERT INTO hyrox_scraping_log_staging (
                scrape_session_id, started_at, completed_at, total_workouts_found, workouts_scraped, workouts_saved, errors_count, has_errors, notes
            ) VALUES (%s, NOW(), NOW(), %s, %s, %s, %s, false, %s)
        """, (
            session_id,
            len(workouts),
            len(workouts),
            len(workouts),
            0,
            'Initial test scrape from wodwell.com'
        ))
        
        print(f"Successfully loaded {len(workouts)} workouts into staging tables")
        print(f"Session ID: {session_id}")
        
    except Exception as e:
        print(f"Error loading workouts: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    with open('/Users/shourjosmac/Documents/Alloy V0/hyrox_workouts_sample.json', 'r') as f:
        workouts = json.load(f)
    
    load_workouts_to_staging(workouts)
