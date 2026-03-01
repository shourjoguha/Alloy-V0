#!/usr/bin/env python3
"""
Hyrox Workout Data Loader

Loads Hyrox workout data from JSON files into the 6-table staging schema:
- hyrox_workouts_staging
- hyrox_workout_lines_staging
- hyrox_mini_circuits_staging
- hyrox_time_segments_staging
- hyrox_ladder_rungs_staging
- hyrox_workout_tags_staging

Usage:
    python scripts/load_hyrox_workouts.py --input hyrox_workouts_sample.json
    python scripts/load_hyrox_workouts.py --input hyrox_workouts_sample.json --dry-run

Environment Variables:
    DATABASE_URL: PostgreSQL connection string (required)
"""

import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime, time as time_type
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_batch, DictCursor
from psycopg2.extensions import connection, cursor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('hyrox_loader.log')
    ]
)
logger = logging.getLogger(__name__)


class HyroxWorkoutLoader:
    """Load Hyrox workout data from JSON into staging tables."""

    def __init__(self, database_url: str, dry_run: bool = False):
        """
        Initialize the loader.

        Args:
            database_url: PostgreSQL connection string
            dry_run: If True, parse and validate but don't write to database
        """
        self.database_url = database_url
        self.dry_run = dry_run
        self.conn: Optional[connection] = None
        self.workout_type_map = {
            'amrap': 'amrap',
            'emom': 'emom',
            'for time': 'for_time',
            'rounds for time': 'rounds_for_time',
            'for load': 'for_load',
            'buy-in': 'buy_in',
            'cash-out': 'cash_out',
            'time cap': 'time_cap',
            'ladder': 'ladder',
            'mini circuit': 'mini_circuit',
            'explicit time guidance': 'explicit_time_guidance'
        }

    def connect(self) -> None:
        """Establish database connection."""
        if self.dry_run:
            logger.info("DRY RUN: Skipping database connection")
            return

        try:
            self.conn = psycopg2.connect(self.database_url)
            self.conn.autocommit = False
            logger.info("Successfully connected to database")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def close(self) -> None:
        """Close database connection."""
        if self.conn and not self.conn.closed:
            self.conn.close()
            logger.info("Database connection closed")

    def parse_time(self, time_str: Optional[str]) -> Optional[time_type]:
        """
        Parse time string to TIME type.

        Args:
            time_str: Time string in format "HH:MM", "MM:SS", or similar

        Returns:
            time object or None if parsing fails
        """
        if not time_str:
            return None

        # Try various time formats
        time_formats = [
            '%H:%M:%S',  # 14:30:00
            '%H:%M',     # 14:30
            '%M:%S',     # 30:00 (treat as minutes:seconds)
            '%I:%M %p',  # 2:30 PM
        ]

        for fmt in time_formats:
            try:
                parsed = datetime.strptime(time_str.strip(), fmt)
                # If only minutes:seconds, treat as duration from midnight
                if fmt == '%M:%S':
                    return time_type(0, parsed.minute, parsed.second)
                return parsed.time()
            except ValueError:
                continue

        logger.warning(f"Could not parse time string: {time_str}")
        return None

    def detect_workout_type(self, description_lines: List[Any]) -> str:
        """
        Detect workout type from description lines.

        Args:
            description_lines: List of workout description lines (strings or dicts)

        Returns:
            Workout type enum value
        """
        if not description_lines:
            return 'unknown'

        # Get first line text regardless of format
        first_obj = description_lines[0]
        if isinstance(first_obj, dict):
            first_line = first_obj.get('text', '').lower()
        else:
            first_line = str(first_obj).lower()

        # Check for common patterns
        if 'amrap' in first_line:
            return 'amrap'
        elif 'emom' in first_line:
            return 'emom'
        elif 'for time' in first_line:
            return 'for_time'
        elif 'rounds for time' in first_line:
            return 'rounds_for_time'
        elif 'for load' in first_line:
            return 'for_load'
        elif 'ladder' in first_line:
            return 'ladder'
        elif 'mini circuit' in first_line or 'circuit' in first_line:
            return 'mini_circuit'
        elif 'time cap' in first_line:
            return 'time_cap'

        return 'unknown'

    def detect_workout_goal(self, description_lines: List[Any]) -> str:
        """
        Detect workout goal from description.

        Args:
            description_lines: List of workout description lines (strings or dicts)

        Returns:
            Workout goal enum value
        """
        if not description_lines:
            return 'unknown'

        # Extract text from all lines
        text_lines = []
        for line in description_lines:
            if isinstance(line, dict):
                text_lines.append(line.get('text', ''))
            else:
                text_lines.append(str(line))
        
        full_desc = ' '.join(text_lines).lower()

        if 'max rounds' in full_desc or 'max reps' in full_desc:
            return 'max_rounds_reps'
        elif 'finish quickly' in full_desc or 'for time' in full_desc:
            return 'finish_quickly'
        elif 'complete rounds' in full_desc:
            return 'complete_rounds'
        elif 'max load' in full_desc or 'for load' in full_desc:
            return 'max_load'
        elif 'pace' in full_desc:
            return 'pace_work'
        elif 'endurance' in full_desc:
            return 'endurance'
        elif 'strength' in full_desc:
            return 'strength'

        return 'mixed'

    def parse_workout_line(self, line: str, line_number: int, workout_id: int,
                          is_buy_in: bool = False, is_cash_out: bool = False) -> Dict[str, Any]:
        """
        Parse a single workout line into structured data.

        Args:
            line: The workout line text
            line_number: Line number in the workout
            workout_id: Foreign key to workout
            is_buy_in: Whether this is a buy-in line
            is_cash_out: Whether this is a cash-out line

        Returns:
            Dictionary with parsed line data
        """
        line_lower = line.lower().strip()

        # Skip structural markers and invalid lines
        skip_patterns = [
            r'^then,?\s*',
            r'^time\s*$',
            r'^for\s+time\s*$',
            r'^amrap\s+',
            r'^emom\s+',
            r'^complete\s+',
            r'^rounds?\s+of\s*\d+',
            r'^\d+,\s*$',
            r'^\d+\s*:\s*$',
            r'^\)\s*$',
            r'^time\s+cap\b',
            r'^workout\s+of\s+the\s+week',
            r'^part\s+[a-z0-9]+',
            r'^round\s+\d+'
        ]
        
        for pattern in skip_patterns:
            if re.match(pattern, line_lower):
                return None

        # Check for rest (but not as part of other words like "restore")
        is_rest = line_lower == 'rest' or line_lower.startswith('rest ')

        # Initialize parsed data
        parsed = {
            'workout_id': workout_id,
            'line_number': line_number,
            'line_text': line,
            'is_rest': is_rest,
            'is_buy_in': is_buy_in,
            'is_cash_out': is_cash_out,
            'is_max_effort': False,
            'mini_circuit_id': None,
            'time_segment_id': None,
            'ladder_rung_id': None
        }

        # Skip rest lines for movement parsing
        if is_rest:
            parsed['movement_name'] = 'Rest'
            return parsed

        # Check for max effort
        if 'max' in line_lower:
            parsed['is_max_effort'] = True

        # Parse distance (meters)
        distance_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:meter|m)\s*(?:run|row|ski|bike|walk)?', line_lower)
        if distance_match:
            parsed['distance_meters'] = float(distance_match.group(1))

        # Parse reps
        reps_match = re.search(r'(\d+)\s*(?:reps|repetitions)?', line_lower)
        if reps_match:
            parsed['reps'] = int(reps_match.group(1))

        # Parse duration (seconds or minutes)
        duration_match = re.search(r'(\d+)\s*(?:second|sec|s)', line_lower)
        if duration_match:
            parsed['duration_seconds'] = int(duration_match.group(1))
        else:
            duration_match = re.search(r'(\d+)\s*(?:minute|min|m)\b', line_lower)
            if duration_match:
                parsed['duration_seconds'] = int(duration_match.group(1)) * 60

        # Parse weights (male/female)
        weight_match = re.search(r'\((\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)\s*lb\)', line_lower)
        if weight_match:
            parsed['weight_male'] = float(weight_match.group(1))
            parsed['weight_female'] = float(weight_match.group(2))

        # Parse calories
        calories_match = re.search(r'(\d+)\s*calorie', line_lower)
        if calories_match:
            parsed['calories'] = int(calories_match.group(1))

        # Extract movement name (remove numbers, weights, calories, etc.)
        movement_name = line
        # Remove weights in parentheses first (more specific)
        movement_name = re.sub(r'\(\d+(?:\.\d+)?\s*/\s*\d+(?:\.\d+)?\s*lb\)', '', movement_name)
        # Remove weights with 2x format
        movement_name = re.sub(r'\(2x\d+(?:\.\d+)?\s*/\s*\d+(?:\.\d+)?\s*lb\)', '', movement_name)
        # Remove calories
        movement_name = re.sub(r'\d+\s*calorie', '', movement_name)
        # Remove distances
        movement_name = re.sub(r'\d+(?:,\d{3})*\s*(?:meter|m|k|km)\b', '', movement_name, flags=re.IGNORECASE)
        # Remove reps, seconds, minutes
        movement_name = re.sub(r'\d+\s*(?:reps|sec|second|minute|min|m|round)\b', '', movement_name, flags=re.IGNORECASE)
        # Remove max and other structural words
        movement_name = re.sub(r'\b(max|for|complete|rounds? of?)\b', '', movement_name, flags=re.IGNORECASE)
        movement_name = movement_name.strip()

        # Clean up common words and structural markers
        movement_name = re.sub(r'\b(with|the|and|a|an|buy-in|buy in|cash-out|cash out)\b', '', movement_name, flags=re.IGNORECASE)
        # Remove trailing colons, commas, and leading colons
        movement_name = re.sub(r'^:\s*', '', movement_name)
        movement_name = re.sub(r'[:,\s]+$', '', movement_name)
        # Clean up multiple spaces
        movement_name = ' '.join(movement_name.split())

        if movement_name:
            parsed['movement_name'] = movement_name.capitalize()
        else:
            parsed['movement_name'] = 'Unknown Movement'

        return parsed

    def parse_workout_structure(self, workout_data: Dict[str, Any]) -> Dict[str, List]:
        """
        Parse workout into structure components (mini circuits, time segments, ladders).

        Args:
            workout_data: Raw workout data from JSON

        Returns:
            Dictionary with parsed structures
        """
        description_lines = workout_data.get('description_lines', [])
        full_desc = workout_data.get('full_description', '')
        workout_type = self.detect_workout_type(description_lines)

        structures = {
            'mini_circuits': [],
            'time_segments': [],
            'ladder_rungs': [],
            'tags': []
        }

        # Parse tags from badge
        badge = workout_data.get('badge')
        if badge:
            structures['tags'].append({
                'tag_name': badge,
                'tag_url': None
            })

        # Check for mini circuits (multiple rounds of the same movements)
        if 'rounds' in full_desc.lower() or 'circuit' in full_desc.lower():
            rounds_match = re.search(r'(\d+)\s*rounds?', full_desc.lower())
            if rounds_match:
                num_rounds = int(rounds_match.group(1))
                structures['mini_circuits'].append({
                    'circuit_number': 1,
                    'circuit_type': workout_type,
                    'num_rounds': num_rounds,
                    'start_time': None,
                    'end_time': None,
                    'duration_minutes': None,
                    'rest_after_minutes': None,
                    'notes': f'{num_rounds} rounds circuit'
                })

        # Check for time segments (explicit time guidance)
        time_segment_matches = re.findall(r'(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})', full_desc)
        for i, (start, end) in enumerate(time_segment_matches):
            structures['time_segments'].append({
                'segment_number': i + 1,
                'start_time': self.parse_time(start),
                'end_time': self.parse_time(end),
                'duration_minutes': None,
                'notes': f'Segment {i + 1}'
            })

        # Check for ladder structure
        # First check if scraper provided structured ladder rungs
        if workout_data.get('ladder_rungs'):
            for rung in workout_data.get('ladder_rungs'):
                structures['ladder_rungs'].append({
                    'rung_number': rung.get('rung_number'),
                    'reps_per_exercise': rung.get('rep_progression'),
                    'is_ascending': True, # Default to True if not specified
                    'notes': rung.get('description'),
                    'movements': rung.get('movements', []) # Keep movements for mapping
                })
        elif 'ladder' in workout_type:
            # Fallback to simplistic detection
            # Detect ascending or descending
            is_ascending = 'ascending' in full_desc.lower() or 'up' in full_desc.lower()
            structures['ladder_rungs'].append({
                'rung_number': 1,
                'reps_per_exercise': None,
                'is_ascending': is_ascending,
                'notes': 'Ladder workout'
            })

        return structures

    def insert_or_update_workout(self, workout_data: Dict[str, Any]) -> int:
        """
        Insert or update workout in hyrox_workouts_staging.

        Args:
            workout_data: Raw workout data from JSON

        Returns:
            The workout_id (primary key)
        """
        wod_id = workout_data.get('wod_id')
        description_lines = workout_data.get('description_lines', [])

        # Parse workout metadata
        workout_type = self.detect_workout_type(description_lines)
        workout_goal = self.detect_workout_goal(description_lines)

        # Parse time specifications
        time_spec = None
        total_time = None
        time_cap = None

        # Extract text from all lines
        text_lines = []
        for line in description_lines:
            if isinstance(line, dict):
                text_lines.append(line.get('text', ''))
            else:
                text_lines.append(str(line))
        
        first_line = text_lines[0] if text_lines else ''
        full_desc_str = workout_data.get('full_description', '') or ' '.join(text_lines)

        # Parse AMRAP time
        amrap_match = re.search(r'amrap\s+in\s+(\d+)\s*min', first_line.lower())
        if amrap_match:
            time_cap = int(amrap_match.group(1))

        # Parse time cap from full description (more reliable as it includes footer lines)
        if not time_cap:
            cap_match = re.search(r'time cap\s*:?\s*(\d+)\s*min', full_desc_str.lower())
            if cap_match:
                time_cap = int(cap_match.group(1))

        # Check for buy-in and cash-out
        has_buy_in = any('buy-in' in line.lower() for line in text_lines)
        has_cash_out = any('cash-out' in line.lower() or 'cash out' in line.lower() for line in text_lines)

        # Check for complexity (has buy-in, cash-out, or multiple structure types)
        is_complex = has_buy_in or has_cash_out

        if self.dry_run:
            logger.info(f"DRY RUN: Would insert/update workout: {wod_id}")
            return 1

        try:
            with self.conn.cursor() as cur:
                # Check if workout exists
                cur.execute(
                    "SELECT id FROM hyrox_workouts_staging WHERE wod_id = %s",
                    (wod_id,)
                )
                existing = cur.fetchone()

                if existing:
                    # Update existing workout
                    workout_id = existing[0]
                    cur.execute("""
                        UPDATE hyrox_workouts_staging
                        SET name = %s,
                            url = %s,
                            badge = %s,
                            workout_type = %s,
                            workout_goal = %s,
                            time_specification = %s,
                            time_cap_minutes = %s,
                            has_buy_in = %s,
                            has_cash_out = %s,
                            is_complex = %s,
                            full_description = %s,
                            status = 'pending_review'
                        WHERE id = %s
                    """, (
                        workout_data.get('name'),
                        workout_data.get('url'),
                        workout_data.get('badge'),
                        workout_type,
                        workout_goal,
                        time_spec,
                        time_cap,
                        has_buy_in,
                        has_cash_out,
                        is_complex,
                        workout_data.get('full_description'),
                        workout_id
                    ))
                    logger.info(f"Updated existing workout: {wod_id} (ID: {workout_id})")
                else:
                    # Insert new workout
                    cur.execute("""
                        INSERT INTO hyrox_workouts_staging
                        (wod_id, name, url, badge, workout_type, workout_goal,
                         time_specification, time_cap_minutes, has_buy_in, has_cash_out,
                         is_complex, full_description, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending_review')
                        RETURNING id
                    """, (
                        wod_id,
                        workout_data.get('name'),
                        workout_data.get('url'),
                        workout_data.get('badge'),
                        workout_type,
                        workout_goal,
                        time_spec,
                        time_cap,
                        has_buy_in,
                        has_cash_out,
                        is_complex,
                        workout_data.get('full_description')
                    ))
                    workout_id = cur.fetchone()[0]
                    logger.info(f"Inserted new workout: {wod_id} (ID: {workout_id})")

                self.conn.commit()
                return workout_id

        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error inserting/updating workout {wod_id}: {e}")
            raise

    def load_workout_lines(self, workout_data: Dict[str, Any], workout_id: int,
                           structures: Dict[str, List], structure_ids: Dict[str, List[int]]) -> None:
        """
        Load workout lines into staging table.

        Args:
            workout_data: Raw workout data from JSON
            workout_id: Foreign key to workout
            structures: Parsed workout structures
        """
        description_lines = workout_data.get('description_lines', [])

        if self.dry_run:
            logger.info(f"DRY RUN: Would load {len(description_lines)} lines for workout {workout_id}")
            return

        try:
            # Delete existing lines for this workout
            with self.conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM hyrox_workout_lines_staging WHERE workout_id = %s",
                    (workout_id,)
                )

            # Build ladder rung map (raw_line_number -> ladder_rung_id)
            line_to_ladder_rung = {}
            if structures['ladder_rungs'] and structure_ids['ladder_rungs']:
                for idx, rung in enumerate(structures['ladder_rungs']):
                    if idx < len(structure_ids['ladder_rungs']):
                        rung_id = structure_ids['ladder_rungs'][idx]
                        for m in rung.get('movements', []):
                            line_num = m.get('raw_line_number') if isinstance(m, dict) else getattr(m, 'raw_line_number', None)
                            if line_num is not None:
                                line_to_ladder_rung[line_num] = rung_id

            # Parse and insert new lines
            lines_to_insert = []
            current_buy_in = False
            current_cash_out = False

            for line_num, line_obj in enumerate(description_lines, start=1):
                # Handle line as dict (from scraper) or string (fallback)
                if isinstance(line_obj, dict):
                    line_text = line_obj.get('text', '')
                    raw_line_number = line_obj.get('raw_line_number', line_num - 1)
                elif hasattr(line_obj, 'text'):
                    line_text = line_obj.text
                    raw_line_number = getattr(line_obj, 'raw_line_number', line_num - 1)
                else:
                    line_text = str(line_obj)
                    raw_line_number = line_num - 1 # Approximation if not provided

                # Track buy-in/cash-out state
                line_lower = line_text.lower()
                if 'buy-in' in line_lower:
                    current_buy_in = True
                    continue
                elif 'cash-out' in line_lower or 'cash out' in line_lower:
                    current_cash_out = True
                    continue
                elif 'then,' in line_lower or 'then amrap' in line_lower:
                    current_buy_in = False
                    current_cash_out = False

                # Skip empty lines and structural markers
                if not line_text.strip() or 'rounds of' in line_lower:
                    continue

                parsed_line = self.parse_workout_line(
                    line_text,
                    line_num,
                    workout_id,
                    is_buy_in=current_buy_in,
                    is_cash_out=current_cash_out
                )

                # Skip if line should be ignored (structural markers, etc.)
                if parsed_line is None:
                    continue

                # Map to mini circuit if applicable
                if structures['mini_circuits'] and structure_ids['mini_circuits'] and not current_buy_in and not current_cash_out:
                    parsed_line['mini_circuit_id'] = structure_ids['mini_circuits'][0]  # First circuit ID

                # Map to ladder rung
                if raw_line_number in line_to_ladder_rung:
                    parsed_line['ladder_rung_id'] = line_to_ladder_rung[raw_line_number]

                # Ensure all required fields have default values
                parsed_line.setdefault('reps', None)
                parsed_line.setdefault('distance_meters', None)
                parsed_line.setdefault('duration_seconds', None)
                parsed_line.setdefault('weight_male', None)
                parsed_line.setdefault('weight_female', None)
                parsed_line.setdefault('calories', None)
                parsed_line.setdefault('notes', None)

                lines_to_insert.append(parsed_line)

            # Batch insert lines
            if lines_to_insert:
                with self.conn.cursor() as cur:
                    execute_batch(cur, """
                        INSERT INTO hyrox_workout_lines_staging
                        (workout_id, line_number, line_text, is_rest, is_buy_in, is_cash_out,
                         movement_name, reps, distance_meters, duration_seconds, weight_male,
                         weight_female, calories, is_max_effort, mini_circuit_id,
                         time_segment_id, ladder_rung_id, notes)
                        VALUES (%(workout_id)s, %(line_number)s, %(line_text)s, %(is_rest)s,
                                %(is_buy_in)s, %(is_cash_out)s, %(movement_name)s, %(reps)s,
                                %(distance_meters)s, %(duration_seconds)s, %(weight_male)s,
                                %(weight_female)s, %(calories)s, %(is_max_effort)s,
                                %(mini_circuit_id)s, %(time_segment_id)s, %(ladder_rung_id)s,
                                %(notes)s)
                    """, lines_to_insert)

                self.conn.commit()
                logger.info(f"Loaded {len(lines_to_insert)} lines for workout {workout_id}")

        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error loading workout lines for {workout_data.get('wod_id')}: {e}")
            raise

    def load_structures(self, workout_id: int, structures: Dict[str, List],
                         wod_id: str) -> Dict[str, List[int]]:
        """
        Load workout structures into staging tables.

        Args:
            workout_id: Foreign key to workout
            structures: Parsed workout structures
            wod_id: Workout identifier for logging

        Returns:
            Dictionary mapping structure types to lists of IDs
        """
        if self.dry_run:
            logger.info(f"DRY RUN: Would load structures for workout {wod_id}")
            return {'mini_circuits': [], 'time_segments': [], 'ladder_rungs': []}

        structure_ids = {'mini_circuits': [], 'time_segments': [], 'ladder_rungs': []}

        try:
            # Delete existing structures for this workout
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM hyrox_mini_circuits_staging WHERE workout_id = %s", (workout_id,))
                cur.execute("DELETE FROM hyrox_time_segments_staging WHERE workout_id = %s", (workout_id,))
                cur.execute("DELETE FROM hyrox_ladder_rungs_staging WHERE workout_id = %s", (workout_id,))
                cur.execute("DELETE FROM hyrox_workout_tags_staging WHERE workout_id = %s", (workout_id,))

            # Load mini circuits
            if structures['mini_circuits']:
                with self.conn.cursor() as cur:
                    for circuit in structures['mini_circuits']:
                        cur.execute("""
                            INSERT INTO hyrox_mini_circuits_staging
                            (workout_id, circuit_number, circuit_type, start_time, end_time,
                             duration_minutes, rest_after_minutes, notes)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            RETURNING id
                        """, (
                            workout_id,
                            circuit['circuit_number'],
                            circuit['circuit_type'],
                            circuit['start_time'],
                            circuit['end_time'],
                            circuit['duration_minutes'],
                            circuit['rest_after_minutes'],
                            circuit['notes']
                        ))
                        structure_ids['mini_circuits'].append(cur.fetchone()[0])

            # Load time segments
            if structures['time_segments']:
                with self.conn.cursor() as cur:
                    for segment in structures['time_segments']:
                        cur.execute("""
                            INSERT INTO hyrox_time_segments_staging
                            (workout_id, segment_number, start_time, end_time,
                             duration_minutes, notes)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            RETURNING id
                        """, (
                            workout_id,
                            segment['segment_number'],
                            segment['start_time'],
                            segment['end_time'],
                            segment['duration_minutes'],
                            segment['notes']
                        ))
                        structure_ids['time_segments'].append(cur.fetchone()[0])

            # Load ladder rungs
            if structures['ladder_rungs']:
                with self.conn.cursor() as cur:
                    for rung in structures['ladder_rungs']:
                        cur.execute("""
                            INSERT INTO hyrox_ladder_rungs_staging
                            (workout_id, rung_number, reps_per_exercise, is_ascending, notes)
                            VALUES (%s, %s, %s, %s, %s)
                            RETURNING id
                        """, (
                            workout_id,
                            rung['rung_number'],
                            rung['reps_per_exercise'],
                            rung['is_ascending'],
                            rung['notes']
                        ))
                        structure_ids['ladder_rungs'].append(cur.fetchone()[0])

            # Load tags
            if structures['tags']:
                with self.conn.cursor() as cur:
                    for tag in structures['tags']:
                        cur.execute("""
                            INSERT INTO hyrox_workout_tags_staging
                            (workout_id, tag_name, tag_url)
                            VALUES (%s, %s, %s)
                        """, (
                            workout_id,
                            tag['tag_name'],
                            tag['tag_url']
                        ))

            self.conn.commit()
            logger.info(f"Loaded structures for workout {wod_id}: "
                       f"{len(structure_ids['mini_circuits'])} circuits, "
                       f"{len(structure_ids['time_segments'])} segments, "
                       f"{len(structure_ids['ladder_rungs'])} rungs, "
                       f"{len(structures['tags'])} tags")

            return structure_ids

        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error loading structures for {wod_id}: {e}")
            raise

    def load_workout(self, workout_data: Dict[str, Any]) -> None:
        """
        Load a single workout into all staging tables.

        Args:
            workout_data: Raw workout data from JSON
        """
        wod_id = workout_data.get('wod_id')
        logger.info(f"Loading workout: {wod_id}")

        try:
            # Insert/update workout metadata
            workout_id = self.insert_or_update_workout(workout_data)

            # Parse workout structure
            structures = self.parse_workout_structure(workout_data)

            # Load structures (mini circuits, time segments, ladders, tags) - must be BEFORE lines
            structure_ids = self.load_structures(workout_id, structures, wod_id)

            # Load workout lines (now they can reference the structure IDs)
            self.load_workout_lines(workout_data, workout_id, structures, structure_ids)

            logger.info(f"Successfully loaded workout: {wod_id}")

        except Exception as e:
            logger.error(f"Failed to load workout {wod_id}: {e}")
            raise

    def load_from_file(self, input_file: str) -> Dict[str, Any]:
        """
        Load all workouts from a JSON file.

        Args:
            input_file: Path to JSON file

        Returns:
            Summary statistics
        """
        logger.info(f"Loading workouts from: {input_file}")

        # Read JSON file
        try:
            with open(input_file, 'r') as f:
                workouts = json.load(f)
        except Exception as e:
            logger.error(f"Failed to read JSON file: {e}")
            raise

        if not isinstance(workouts, list):
            logger.error("JSON file must contain an array of workouts")
            raise ValueError("Invalid JSON format")

        summary = {
            'total': len(workouts),
            'success': 0,
            'failed': 0,
            'errors': []
        }

        # Load each workout
        for i, workout_data in enumerate(workouts, start=1):
            try:
                logger.info(f"Processing workout {i}/{len(workouts)}")
                self.load_workout(workout_data)
                summary['success'] += 1
            except Exception as e:
                summary['failed'] += 1
                error_msg = f"Failed to load workout {workout_data.get('wod_id', 'unknown')}: {str(e)}"
                summary['errors'].append(error_msg)
                logger.error(error_msg)

        logger.info(f"Loading complete: {summary['success']}/{summary['total']} workouts loaded successfully")
        return summary


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Load Hyrox workout data from JSON into staging tables'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Path to JSON file containing workout data'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Parse and validate without writing to database'
    )

    args = parser.parse_args()

    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        logger.error("DATABASE_URL environment variable is required")
        sys.exit(1)

    # Validate input file
    if not os.path.exists(args.input):
        logger.error(f"Input file not found: {args.input}")
        sys.exit(1)

    # Create loader and process file
    loader = HyroxWorkoutLoader(database_url, dry_run=args.dry_run)

    try:
        loader.connect()
        summary = loader.load_from_file(args.input)

        # Print summary
        print("\n" + "="*60)
        print("LOAD SUMMARY")
        print("="*60)
        print(f"Total workouts: {summary['total']}")
        print(f"Successfully loaded: {summary['success']}")
        print(f"Failed: {summary['failed']}")
        if summary['errors']:
            print("\nErrors:")
            for error in summary['errors']:
                print(f"  - {error}")
        print("="*60)

        # Exit with error code if any failures
        if summary['failed'] > 0:
            sys.exit(1)

    except Exception as e:
        logger.error(f"Fatal error during loading: {e}")
        sys.exit(1)
    finally:
        loader.close()


if __name__ == '__main__':
    main()
