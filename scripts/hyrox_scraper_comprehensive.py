"""
Comprehensive Hyrox Workouts Scraper
Scrapes Hyrox workouts from wodwell.com with complete data extraction and validation
"""

import asyncio
import json
import logging
import re
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
import time
import traceback

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)

try:
    from playwright.async_api import async_playwright, Page, Browser, Error as PlaywrightError
except ImportError:
    raise ImportError(
        "Playwright not installed. Install with: pip install playwright && playwright install chromium"
    )


# ============================================================================
# Configuration and Enums
# ============================================================================

class WorkoutType(str, Enum):
    """Standardized workout types"""
    AMRAP = "amrap"
    EMOM = "emom"
    FOR_TIME = "for_time"
    RFT = "rounds_for_time"
    CHIPPER = "chipper"
    LADDER = "ladder"
    BUY_IN = "buy_in"
    CASH_OUT = "cash_out"
    TIME_CAP = "time_cap"
    MINI_CIRCUIT = "mini_circuit"
    EXPLICIT_TIME = "explicit_time_guidance"
    UNKNOWN = "unknown"


class WorkoutGoal(str, Enum):
    """Standardized workout goals"""
    MAX_ROUNDS_REPS = "max_rounds_reps"
    FINISH_QUICKLY = "finish_quickly"
    COMPLETE_ROUNDS = "complete_rounds"
    MAX_LOAD = "max_load"
    PACE_WORK = "pace_work"
    UNKNOWN = "unknown"


class ScrapingStatus(str, Enum):
    """Status of scraping operation"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class DataQuality(str, Enum):
    """Data quality flags"""
    VALID = "valid"
    MISSING_REQUIRED = "missing_required"
    INVALID_FORMAT = "invalid_format"
    DUPLICATE = "duplicate"
    INCOMPLETE = "incomplete"


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class MovementLine:
    """Individual movement line from workout description"""
    text: str
    movement_name: Optional[str] = None
    reps: Optional[int] = None
    distance_meters: Optional[int] = None
    duration_seconds: Optional[int] = None
    weight_male_lb: Optional[int] = None
    weight_female_lb: Optional[int] = None
    weight_male_kg: Optional[float] = None
    weight_female_kg: Optional[float] = None
    calories: Optional[int] = None
    is_rest: bool = False
    is_header: bool = False
    is_cash_out: bool = False
    is_buy_in: bool = False
    raw_line_number: int = 0


@dataclass
class MiniCircuit:
    """Mini circuit within workout"""
    circuit_number: int
    description: str
    movements: List[MovementLine] = field(default_factory=list)
    rounds: Optional[int] = None
    time_seconds: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    interval_seconds: Optional[int] = None


@dataclass
class TimeSegment:
    """Time segment within workout"""
    segment_number: int
    description: str
    movements: List[MovementLine] = field(default_factory=list)
    time_seconds: Optional[int] = None
    type: str = "segment"  # segment, buy_in, cash_out


@dataclass
class LadderRung:
    """Ladder rung for ladder workouts"""
    rung_number: int
    description: str
    movements: List[MovementLine] = field(default_factory=list)
    rep_progression: Optional[List[int]] = None


@dataclass
class WorkoutStats:
    """Workout engagement statistics"""
    favorites: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0


@dataclass
class HyroxWorkout:
    """Complete Hyrox workout data model"""
    wod_id: Optional[str] = None
    url: Optional[str] = None
    name: Optional[str] = None
    badge: Optional[str] = None
    workout_type: WorkoutType = WorkoutType.UNKNOWN
    workout_goal: WorkoutGoal = WorkoutGoal.UNKNOWN
    time_specification: Optional[str] = None
    time_cap_minutes: Optional[int] = None
    total_time_minutes: Optional[int] = None
    full_description: Optional[str] = None
    
    # Parsed structure
    total_rounds: Optional[int] = None
    description_lines: List[MovementLine] = field(default_factory=list)
    mini_circuits: List[MiniCircuit] = field(default_factory=list)
    time_segments: List[TimeSegment] = field(default_factory=list)
    ladder_rungs: List[LadderRung] = field(default_factory=list)
    
    # Flags
    has_buy_in: bool = False
    has_cash_out: bool = False
    is_complex: bool = False
    is_interval: bool = False
    
    # Scraping metadata
    scraped_at: str = field(default_factory=lambda: datetime.now().isoformat())
    source_page: str = "hyrox_workouts"
    session_id: str = ""
    status: ScrapingStatus = ScrapingStatus.PENDING
    data_quality: DataQuality = DataQuality.VALID
    validation_errors: List[str] = field(default_factory=list)
    notes: Optional[str] = None


@dataclass
class ScrapingProgress:
    """Track scraping progress"""
    session_id: str
    started_at: str
    current_page: int = 1
    workouts_found: int = 0
    workouts_scraped: int = 0
    workouts_failed: int = 0
    pages_scraped: int = 0
    total_workouts_estimated: int = 0
    errors: List[Dict] = field(default_factory=list)
    warnings: List[Dict] = field(default_factory=list)


# ============================================================================
# Parser Classes
# ============================================================================

class WorkoutParser:
    """Parse workout descriptions into structured data"""
    
    # Movement patterns for Hyrox workouts
    MOVEMENT_PATTERNS = [
        r'(?i)\bwall\s+ball\s+shots?\b',
        r'(?i)\bski\s+erg\b',
        r'(?i)\blunges?\b',
        r'(?i)\bburpees?\b',
        r'(?i)\bv-ups?\b',
        r'(?i)\bsit-ups?\b',
        r'(?i)\bpush-ups?\b',
        r'(?i)\bpull-ups?\b',
        r'(?i)\bchest\s+to\s+bar\b',
        r'(?i)\btoes\s+to\s+bar\b',
        r'(?i)\bhand\s+release\s+push-ups?\b',
        r'(?i)\bsandbag\s+lunges?\b',
        r'(?i)\bfarmer.?s\s+carry\b',
        r'(?i)\bsled\s+push\b',
        r'(?i)\bsled\s+pull\b',
        r'(?i)\brow\b',
        r'(?i)\brun\b',
        r'(?i)\bthrusters?\b',
        r'(?i)\bdeadlifts?\b',
        r'(?i)\bsquat\s+cleans?\b',
        r'(?i)\bpower\s+cleans?\b',
        r'(?i)\bsnatches?\b',
        r'(?i)\bbox\s+jumps?\b',
        r'(?i)\bdouble\s+unders?\b',
        r'(?i)\bsingle\s+unders?\b',
        r'(?i)\bkettlebell\s+swings?\b',
        r'(?i)\bmuscle-ups?\b',
        r'(?i)\bplank\b',
        r'(?i)\bhollow\s+rock\b',
        r'(?i)\barch\s+hold\b',
        r'(?i)\bjumping\s+jacks?\b',
        r'(?i)\bmountain\s+climbers?\b',
        r'(?i)\bair\s+squats?\b',
        r'(?i)\bjump\s+squats?\b',
        r'(?i)\bpush\s+press\b',
        r'(?i)\bstrict\s+press\b',
        r'(?i)\bjerk\b',
        r'(?i)\bsnatch\s+balance\b',
        r'(?i)\boverhead\s+squat\b',
        r'(?i)\bfront\s+squat\b',
        r'(?i)\bback\s+squat\b',
        r'(?i)\bbench\s+press\b',
        r'(?i)\btricep\s+dips?\b',
        r'(?i)\bbroad\s+jumps?\b',
        r'(?i)\bbear\s+crawls?\b',
        r'(?i)\bcrab\s+walks?\b',
        r'(?i)\bwheel\s+barrow\b',
            r'(?i)\bfarmer.?s\s+walks?\b',
            r'(?i)\bcarry\b',
        r'(?i)\bwalking\s+lunges?\b',
        r'(?i)\bjumping\s+lunges?\b',
        r'(?i)\bstep-ups?\b',
        r'(?i)\bbox\s+step-ups?\b',
        r'(?i)\bjump\s+ropes?\b',
        r'(?i)\bsprints?\b',
    ]
    
    # Workout type patterns
    WORKOUT_TYPE_PATTERNS = {
        r'(?i)\bamrap\s+(?:in\s+)?(\d+)\s*(?:min|minutes?)\b': WorkoutType.AMRAP,
        r'(?i)\bamrap\b': WorkoutType.AMRAP,
        r'(?i)\bemom\s+(?:for\s+)?(\d+)\s*(?:min|minutes?)\b': WorkoutType.EMOM,
        r'(?i)\bemom\b': WorkoutType.EMOM,
        r'(?i)\b(?:complete\s+)?(\d+)\s+rounds?\s+for\s+time\b': WorkoutType.RFT,
        r'(?i)\brounds?\s+for\s+total\b': WorkoutType.RFT,
        r'(?i)\b(?:rounds?\s+)?(?:for\s+time)\b': WorkoutType.FOR_TIME,
        r'(?i)\bfor\s+time\b': WorkoutType.FOR_TIME,
        r'(?i)\bchipper\b': WorkoutType.CHIPPER,
        r'(?i)\bladder\b': WorkoutType.LADDER,
        r'(?i)\bbuy-in\b': WorkoutType.BUY_IN,
        r'(?i)\bcash-out\b': WorkoutType.CASH_OUT,
        r'(?i)\btime\s+cap\s*:?\s*(\d+)\s*(?:min|minutes?)\b': WorkoutType.TIME_CAP,
        r'(?i)\bmini\s+circuit\b': WorkoutType.MINI_CIRCUIT,
    }
    
    # Workout goal patterns
    WORKOUT_GOAL_PATTERNS = {
        r'(?i)\bas\s+many\s+rounds\s+as\s+possible\b': WorkoutGoal.MAX_ROUNDS_REPS,
        r'(?i)\bamrap\b': WorkoutGoal.MAX_ROUNDS_REPS,
        r'(?i)\bmax\s+reps\b': WorkoutGoal.MAX_ROUNDS_REPS,
        r'(?i)\bfor\s+total\s+reps\b': WorkoutGoal.MAX_ROUNDS_REPS,
        r'(?i)\bas\s+quickly\s+as\s+possible\b': WorkoutGoal.FINISH_QUICKLY,
        r'(?i)\bfinish\s+(?:as\s+)?quickly\s+as\s+possible\b': WorkoutGoal.FINISH_QUICKLY,
        r'(?i)\bfor\s+time\b': WorkoutGoal.FINISH_QUICKLY,
        r'(?i)\b(?:complete|finish)\s+all\s+rounds?\b': WorkoutGoal.COMPLETE_ROUNDS,
        r'(?i)\bbuild\s+up\s+to\s+heaviest\b': WorkoutGoal.MAX_LOAD,
        r'(?i)\bfor\s+load\b': WorkoutGoal.MAX_LOAD,
        r'(?i)\bmax\s+load\b': WorkoutGoal.MAX_LOAD,
        r'(?i)\bpace\s+work\b': WorkoutGoal.PACE_WORK,
        r'(?i)\bmax\s+effort\b': WorkoutGoal.PACE_WORK,
    }
    
    @classmethod
    def parse_workout_type(cls, text: str) -> WorkoutType:
        """Extract workout type from text"""
        for pattern, workout_type in cls.WORKOUT_TYPE_PATTERNS.items():
            if re.search(pattern, text):
                return workout_type
        return WorkoutType.UNKNOWN
    
    @classmethod
    def parse_workout_goal(cls, text: str) -> WorkoutGoal:
        """Extract workout goal from text"""
        for pattern, goal in cls.WORKOUT_GOAL_PATTERNS.items():
            if re.search(pattern, text):
                return goal
        return WorkoutGoal.UNKNOWN
    
    @classmethod
    def parse_time_specification(cls, text: str) -> Optional[str]:
        """Extract time specification from text"""
        time_patterns = [
            r'(\d+)\s*(?:min|minutes?)\b',
            r'(\d+):(\d+)\b',
            r'(\d+)\s*(?:sec|seconds?)\b',
            r'(\d+)\s*(?:hours?|hrs?)\b',
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return None
    
    @classmethod
    def parse_total_minutes(cls, text: str) -> Optional[int]:
        """Extract total workout time in minutes"""
        minutes_match = re.search(r'(\d+)\s*(?:min|minutes?)\b', text, re.IGNORECASE)
        if minutes_match:
            return int(minutes_match.group(1))
        
        time_match = re.search(r'(\d+):(\d+)\b', text)
        if time_match:
            hours = int(time_match.group(1))
            minutes = int(time_match.group(2))
            return hours * 60 + minutes
        
        seconds_match = re.search(r'(\d+)\s*(?:sec|seconds?)\b', text, re.IGNORECASE)
        if seconds_match:
            return int(seconds_match.group(1)) // 60
        
        return None
    
    @classmethod
    def parse_time_cap(cls, text: str) -> Optional[int]:
        """Extract time cap in minutes"""
        cap_patterns = [
            r'(?i)\btime\s+cap\s*:?\s*(\d+)\s*(?:min|minutes?)\b',
            r'(?i)\bcap\s*:?\s*(\d+)\s*(?:min|minutes?)\b',
        ]
        
        for pattern in cap_patterns:
            match = re.search(pattern, text)
            if match:
                return int(match.group(1))
        
        return None
    
    @classmethod
    def parse_description_lines(cls, full_description: str) -> List[MovementLine]:
        """Parse description text into structured movement lines"""
        lines = full_description.split('\n')
        parsed_lines = []
        
        for idx, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            movement_line = cls._parse_single_line(line, idx)
            parsed_lines.append(movement_line)
        
        return parsed_lines
    
    @classmethod
    def _parse_single_line(cls, text: str, line_number: int) -> MovementLine:
        """Parse a single movement line"""
        text_lower = text.lower()
        
        # Check if it's a header or rest line
        is_header = any(indicator in text_lower for indicator in [
            'round', 'complete', 'for time', 'amrap', 'emom', 'rft',
            'buy-in', 'cash-out', 'circuit', 'segment', 'ladder',
            'time cap', 'cap:', 'repeat', 'for load', 'reps of',
            'directly into', 'then, perform', 'for total',
            'every minute', 'tabata', 'finally into'
        ])
        
        # Regex check for 'part [a-z]' and 'every \d+'
        if not is_header:
            is_header = bool(re.search(r'\bpart\s+[a-z]\b', text_lower)) or \
                        bool(re.search(r'every\s+\d+', text_lower))
        is_rest = any(indicator in text_lower for indicator in [
            'rest', 'transition', 'break'
        ])
        is_cash_out = 'cash-out' in text_lower or 'cash out' in text_lower
        is_buy_in = 'buy-in' in text_lower or 'buy in' in text_lower
        
        # Extract metrics with priority
        distance = cls._extract_distance(text)
        calories = cls._extract_calories(text)
        duration = cls._extract_duration(text)
        
        # Reps should only be captured if no other metric is present
        reps = None
        if not (distance or calories or duration):
            reps = cls._extract_reps(text)
            
        movement_line = MovementLine(
            text=text,
            is_header=is_header,
            is_rest=is_rest,
            is_cash_out=is_cash_out,
            is_buy_in=is_buy_in,
            raw_line_number=line_number,
            movement_name=cls._extract_movement_name(text),
            reps=reps,
            distance_meters=distance,
            duration_seconds=duration,
            weight_male_lb=cls._extract_weight(text, 'lb', 'male'),
            weight_female_lb=cls._extract_weight(text, 'lb', 'female'),
            weight_male_kg=cls._extract_weight(text, 'kg', 'male'),
            weight_female_kg=cls._extract_weight(text, 'kg', 'female'),
            calories=calories,
        )
        
        return movement_line
    
    @classmethod
    def _extract_movement_name(cls, text: str) -> Optional[str]:
        """Extract movement name from text"""
        text_lower = text.lower()
        
        # Known Hyrox movements mapping
        # Key: regex pattern, Value: standardized name
        MOVEMENT_MAPPINGS = {
            r'(?i)\bwall\s+ball\s+shots?\b': 'Wall Ball',
            r'(?i)\bwall\s+balls?\b': 'Wall Ball',
            r'(?i)\bskierg\b': 'Calorie Ski Erg',
            r'(?i)\bski\s+erg\b': 'Calorie Ski Erg',
            r'(?i)\bski\b': 'Calorie Ski Erg',
            r'(?i)\bsandbag\s+lunges?\b': 'Sandbag Lunges',
            r'(?i)\bwalking\s+lunges?\b': 'Lunges',
            r'(?i)\blunges?\b': 'Lunges',
            r'(?i)\bburpee\s+broad\s+jumps?\b': 'Burpee Broad Jumps',
            r'(?i)\bburpees?\b': 'Burpees',
            r'(?i)\bv-ups?\b': 'V-Ups',
            r'(?i)\bsit-ups?\b': 'Sit-Ups',
            r'(?i)\bpush-ups?\b': 'Push-Ups',
            r'(?i)\bpull-ups?\b': 'Pull-Ups',
            r'(?i)\bchest\s+to\s+bar\b': 'Chest-to-Bar Pull-Ups',
            r'(?i)\btoes\s+to\s+bar\b': 'Toes-to-Bar',
            r'(?i)\bhand\s+release\s+push-ups?\b': 'Hand Release Push-Ups',
            r'(?i)\bfarmer.?s\s+carry\b': "Farmer'S Carry",
            r'(?i)\bfarmer.?s\s+walks?\b': "Farmer'S Carry",
            r'(?i)\bsled\s+push\b': 'Sled Push',
            r'(?i)\bsled\s+pulls?\b': 'Sled Pull',
            r'(?i)\brow\b': 'Rowing Machine',
            r'(?i)\browing\b': 'Rowing Machine',
            r'(?i)\brower\b': 'Rowing Machine',
            r'(?i)\brun\b': 'Run',
            r'(?i)\brunning\b': 'Run',
            r'(?i)\bthrusters?\b': 'Thrusters',
            r'(?i)\bdeadlifts?\b': 'Deadlifts',
            r'(?i)\bsquat\s+cleans?\b': 'Squat Cleans',
            r'(?i)\bpower\s+cleans?\b': 'Power Cleans',
            r'(?i)\bsnatches?\b': 'Snatches',
            r'(?i)\bbox\s+jumps?\b': 'Box Jumps',
            r'(?i)\bdouble\s+unders?\b': 'Double Unders',
            r'(?i)\bsingle\s+unders?\b': 'Single Unders',
            r'(?i)\bkettlebell\s+swings?\b': 'Kettlebell Swings',
            r'(?i)\bmuscle-ups?\b': 'Muscle-Ups',
            r'(?i)\bplank\b': 'Plank',
            r'(?i)\bhollow\s+rock\b': 'Hollow Rock',
            r'(?i)\barch\s+hold\b': 'Arch Hold',
            r'(?i)\bjumping\s+jacks?\b': 'Jumping Jacks',
            r'(?i)\bmountain\s+climbers?\b': 'Mountain Climbers',
            r'(?i)\bair\s+squats?\b': 'Air Squats',
            r'(?i)\bjump(?:ing)?\s+squats?\b': 'Jump Squats',
            r'(?i)\bpush\s+press\b': 'Push Press',
            r'(?i)\bstrict\s+press\b': 'Strict Press',
            r'(?i)\bjerk\b': 'Jerk',
            r'(?i)\bsnatch\s+balance\b': 'Snatch Balance',
            r'(?i)\boverhead\s+squat\b': 'Overhead Squat',
            r'(?i)\bfront\s+squat\b': 'Front Squat',
            r'(?i)\bback\s+squats?\b': 'Back Squat',
            r'(?i)\bbench\s+press(?:es)?\b': 'Bench Press',
            r'(?i)\btricep\s+dips?\b': 'Tricep Dips',
            r'(?i)\bbroad\s+jumps?\b': 'Broad Jumps',
            r'(?i)\bbear\s+crawls?\b': 'Bear Crawl',
            r'(?i)\bcrab\s+walks?\b': 'Crab Walk',
            r'(?i)\bwheel\s+barrow\b': 'Wheelbarrow',
            r'(?i)\bcarry\b': 'Carry',
            r'(?i)\bstep-ups?\b': 'Step-Ups',
            r'(?i)\bbox\s+step-ups?\b': 'Box Step-Ups',
            r'(?i)\bjump\s+ropes?\b': 'Jump Rope',
            r'(?i)\bdevil\s+press(?:es)?\b': 'Devil Press',
            r'(?i)\bgoblet\s+squats?\b': 'Goblet Squats',
            r'(?i)\bshuttle\s+runs?\b': 'Shuttle Runs',
            r'(?i)\bwall\s+walks?\b': 'Wall Walks',
            r'(?i)\bsprints?\b': 'Sprint',
        }
        
        for pattern, name in MOVEMENT_MAPPINGS.items():
            match = re.search(pattern, text_lower)
            if match:
                return name
        
        return None

    @classmethod
    def _time_str_to_seconds(cls, time_str: str) -> int:
        """Convert MM:SS or HH:MM:SS to seconds"""
        if not time_str:
            return 0
        
        parts = time_str.split(':')
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return 0

    @classmethod
    def _extract_rounds(cls, text: str) -> Optional[int]:
        """Extract number of rounds from text"""
        patterns = [
            r'(\d+)\s+rounds?\b',
            r'rounds?\s+(\d+)\b',
            r'^(\d+)\s*RFT\b',
            r'repeat\s+(\d+)x',
            r'(\d+)\s+rounds?\s+of',
            r'(?i)for\s+(\d+)\s+rounds?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    @classmethod
    def _extract_reps(cls, text: str) -> Optional[int]:
        """Extract repetitions from text"""
        patterns = [
            r'^(\d+)\s+(?!meter|cal|lb|kg|min|sec|hour)',
            r'(\d+)\s+(?:reps?|rep(?:etitions)?)\b',
            r'(\d+)-(\d+)\s+reps?',  # Range like "10-15 reps"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    @classmethod
    def _extract_distance(cls, text: str) -> Optional[int]:
        """Extract distance from text"""
        patterns = [
            r'([\d,]+)\s*(?:m|meter)\b',  # Handle "1,000 m" or "10,000 m"
            r'(\d+)\s*(?:m|meter|km|kilometer)\b',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value_str = match.group(1).replace(',', '')
                try:
                    value = int(value_str)
                    
                    # Check if it was km/kilometer
                    if 'km' in match.group(0).lower() or 'kilometer' in match.group(0).lower():
                        return value * 1000
                    return value
                except ValueError:
                    continue
        
        return None
    
    @classmethod
    def _extract_duration(cls, text: str) -> Optional[int]:
        """Extract duration in seconds"""
        # Handle "Minute [n]" pattern (implies 60s)
        if re.search(r'Minute\s+\d+', text, re.IGNORECASE):
            return 60
            
        patterns = [
            r'(\d+)\s*(?:sec|seconds?)\b',
            r'(\d+):(\d+)\b',
            r'(\d+)\s*(?:min|minutes?)\b',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    # MM:SS format
                    return int(match.group(1)) * 60 + int(match.group(2))
                value = int(match.group(1))
                if 'min' in pattern.lower():
                    return value * 60
                return value
        
        return None
    
    @classmethod
    def _extract_weight(cls, text: str, unit: str, gender: str) -> Optional[int]:
        """Extract weight from text"""
        # Pattern for "20/14 lb" format
        if '/' in text and unit in text.lower():
            parts = text.split('/')
            if len(parts) == 2:
                try:
                    if gender == 'male':
                        match = re.search(r'(\d+)\s*' + re.escape(unit), parts[0])
                        if match:
                            return int(match.group(1))
                    elif gender == 'female':
                        match = re.search(r'(\d+)\s*' + re.escape(unit), parts[1])
                        if match:
                            return int(match.group(1))
                except (ValueError, IndexError):
                    pass
        
        # Pattern for single weight value
        pattern = r'(\d+)\s*' + re.escape(unit)
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = int(match.group(1))
            # Assume it's male weight if single value
            return value if gender == 'male' else None
        
        return None
    
    @classmethod
    def _extract_calories(cls, text: str) -> Optional[int]:
        """Extract calories from text"""
        match = re.search(r'(\d+)\s*(?:cal|calorie|kcal)\b', text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None
    
    @classmethod
    def detect_complex_structure(cls, description_lines: List[MovementLine]) -> bool:
        """Detect if workout has complex structure"""
        complex_indicators = [
            'mini circuit',
            'ladder',
            'time segment',
            'buy-in',
            'cash-out',
            'then',
            'after that',
            'followed by',
        ]
        
        for line in description_lines:
            if any(indicator in line.text.lower() for indicator in complex_indicators):
                return True
        
        return False
    
    @classmethod
    def parse_mini_circuits(cls, description_lines: List[MovementLine]) -> List[MiniCircuit]:
        """Parse mini circuits from workout description"""
        circuits = []
        current_circuit = None
        circuit_num = 0
        
        # Regex patterns
        interval_pattern = r'(?i)from\s+(\d+:\d+)-(\d+:\d+),?\s+every\s+(\d+)\s*(?:sec|seconds?)'
        time_block_pattern = r'^(\d+:\d+)-(\d+:\d+):?'
        rounds_pattern = r'(?i)(?:repeat\s+)?(\d+)\s*(?:x|rounds?)'
        
        for line in description_lines:
            text = line.text.strip()
            text_lower = text.lower()
            
            # Check for new circuit indicators
            is_new_circuit = False
            rounds = None
            start_time = None
            end_time = None
            interval = None
            
            # Pattern 1: Interval (e.g., "From 0:00-9:00, every 90 seconds")
            interval_match = re.search(interval_pattern, text)
            if interval_match:
                is_new_circuit = True
                start_time = interval_match.group(1)
                end_time = interval_match.group(2)
                interval = int(interval_match.group(3))
                # Calculate rounds
                start_secs = cls._time_str_to_seconds(start_time)
                end_secs = cls._time_str_to_seconds(end_time)
                if interval > 0:
                    rounds = (end_secs - start_secs) // interval
            
            # Pattern 2: Time Block (e.g., "0:00-2:00: ...")
            if not is_new_circuit:
                block_match = re.search(time_block_pattern, text)
                if block_match:
                    is_new_circuit = True
                    start_time = block_match.group(1)
                    end_time = block_match.group(2)
            
            # Pattern 3: Explicit Rounds / Headers
            if not is_new_circuit:
                if 'rounds' in text_lower or 'repeat' in text_lower or 'mini circuit' in text_lower:
                     # Check if it's a header line or contains round info
                     rounds_match = re.search(rounds_pattern, text)
                     if rounds_match or line.is_header:
                         # Check if we should merge with current empty circuit (e.g. Time Block followed by Rounds)
                         if (current_circuit and 
                             len(current_circuit.movements) == 0 and 
                             current_circuit.start_time is not None and 
                             rounds_match):
                             # Merge rounds into current circuit
                             current_circuit.rounds = int(rounds_match.group(1))
                             # Skip creating new circuit, continue to next line
                             continue

                         # Distinguish "Round 1" vs "5 Rounds"
                         # If it's "Round X", it might be a specific round, but here we group circuits.
                         # If it says "5 Rounds", it's a circuit definition.
                         is_new_circuit = True
                         if rounds_match:
                             rounds = int(rounds_match.group(1))
                
                # Check for "Then..." which often starts a new section
                if text_lower.startswith('then') and ('rounds' in text_lower or 'circuit' in text_lower):
                    is_new_circuit = True
                    rounds_match = re.search(rounds_pattern, text)
                    if rounds_match:
                        rounds = int(rounds_match.group(1))

            if is_new_circuit:
                if current_circuit:
                    circuits.append(current_circuit)
                circuit_num += 1
                current_circuit = MiniCircuit(
                    circuit_number=circuit_num,
                    description=text,
                    movements=[],
                    rounds=rounds,
                    start_time=start_time,
                    end_time=end_time,
                    interval_seconds=interval
                )
            elif current_circuit and not line.is_header:
                current_circuit.movements.append(line)
        
        if current_circuit:
            circuits.append(current_circuit)
        
        return circuits
    
    @classmethod
    def parse_time_segments(cls, description_lines: List[MovementLine]) -> List[TimeSegment]:
        """Parse time segments from workout description"""
        segments = []
        current_segment = None
        segment_num = 0
        
        for line in description_lines:
            if any(indicator in line.text.lower() for indicator in ['buy-in', 'cash-out', 'segment']):
                if current_segment:
                    segments.append(current_segment)
                segment_num += 1
                
                segment_type = 'buy_in' if 'buy-in' in line.text.lower() else 'cash_out'
                segment_type = segment_type if 'cash-out' in line.text.lower() else 'segment'
                
                current_segment = TimeSegment(
                    segment_number=segment_num,
                    description=line.text,
                    movements=[],
                    type=segment_type
                )
            elif current_segment and not line.is_header:
                current_segment.movements.append(line)
        
        if current_segment:
            segments.append(current_segment)
        
        return segments
    
    @classmethod
    def parse_ladder_rungs(cls, description_lines: List[MovementLine], workout_type: WorkoutType = None) -> List[LadderRung]:
        """Parse ladder rungs from workout description"""
        # If explicitly not a ladder workout, be strict about finding "ladder" keyword
        if workout_type and workout_type != WorkoutType.LADDER:
            has_ladder_keyword = any('ladder' in line.text.lower() for line in description_lines)
            if not has_ladder_keyword:
                return []

        rungs = []
        current_rung = None
        rung_num = 0
        
        for line in description_lines:
            text_lower = line.text.lower()
            
            # Skip Time Cap lines for ladder rungs
            if 'time cap' in text_lower or 'cap:' in text_lower:
                continue
                
            if 'ladder' in text_lower or (line.reps and current_rung is None and workout_type == WorkoutType.LADDER):
                if current_rung:
                    rungs.append(current_rung)
                rung_num += 1
                current_rung = LadderRung(
                    rung_number=rung_num,
                    description=line.text,
                    movements=[line] if line.movement_name else []
                )
            elif current_rung and not line.is_header:
                current_rung.movements.append(line)
        
        if current_rung:
            rungs.append(current_rung)
        
        return rungs


# ============================================================================
# Quality Validator
# ============================================================================

class DataQualityValidator:
    """Validate scraped workout data for quality issues"""
    
    REQUIRED_FIELDS = ['wod_id', 'name', 'full_description', 'workout_type']
    
    @classmethod
    def validate_workout(cls, workout: HyroxWorkout) -> Tuple[bool, List[str]]:
        """
        Validate workout data
        
        Returns:
            Tuple of (is_valid, list of errors)
        """
        errors = []
        
        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            value = getattr(workout, field, None)
            if not value or (isinstance(value, str) and not value.strip()):
                errors.append(f"Missing required field: {field}")
        
        # Validate workout type
        if workout.workout_type == WorkoutType.UNKNOWN:
            errors.append("Unknown workout type detected")
        
        # Validate description lines
        if workout.description_lines:
            movement_count = sum(1 for line in workout.description_lines if line.movement_name)
            if movement_count == 0:
                errors.append("No movements found in description")
        else:
            errors.append("No description lines parsed")
        
        # Validate URL format
        if workout.url and not workout.url.startswith('https://'):
            errors.append(f"Invalid URL format: {workout.url}")
        
        # Check for reasonable time values
        if workout.total_time_minutes and (workout.total_time_minutes < 0 or workout.total_time_minutes > 300):
            errors.append(f"Suspicious total time: {workout.total_time_minutes} minutes")
        
        if workout.time_cap_minutes and (workout.time_cap_minutes < 0 or workout.time_cap_minutes > 180):
            errors.append(f"Suspicious time cap: {workout.time_cap_minutes} minutes")
        
        # Validate movement data
        for line in workout.description_lines:
            if line.distance_meters and line.distance_meters > 10000:
                errors.append(f"Suspicious distance: {line.distance_meters} meters")
            
            if line.duration_seconds and line.duration_seconds > 3600:
                errors.append(f"Suspicious duration: {line.duration_seconds} seconds")
            
            if line.calories and line.calories > 500:
                errors.append(f"Suspicious calorie count: {line.calories}")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    @classmethod
    def check_duplicates(cls, workouts: List[HyroxWorkout]) -> List[str]:
        """Check for duplicate workouts"""
        seen_urls = set()
        seen_names = set()
        duplicates = []
        
        for workout in workouts:
            if workout.url:
                if workout.url in seen_urls:
                    duplicates.append(f"Duplicate URL: {workout.url}")
                seen_urls.add(workout.url)
            
            if workout.name:
                name_key = f"{workout.name}_{workout.workout_type}"
                if name_key in seen_names:
                    duplicates.append(f"Duplicate name/type: {workout.name}")
                seen_names.add(name_key)
        
        return duplicates


# ============================================================================
# Main Scraper Class
# ============================================================================

class HyroxWorkoutScraper:
    """
    Comprehensive Hyrox workouts scraper using Playwright
    
    Features:
    - Infinite scroll pagination
    - Complete data extraction
    - Structured parsing of workout components
    - Retry logic with exponential backoff
    - Progress tracking and logging
    - Data quality validation
    """
    
    BASE_URL = "https://wodwell.com/wods/tag/hyrox-workouts/?sort=newest"
    MAX_PAGES = 20  # Safety limit
    MAX_RETRIES = 3
    SCROLL_WAIT_MS = 2000
    PAGE_LOAD_TIMEOUT_MS = 60000
    REQUEST_TIMEOUT_MS = 30000
    
    def __init__(self, session_id: str = None, log_level: str = "INFO"):
        self.session_id = session_id or str(uuid.uuid4())
        self.progress = ScrapingProgress(
            session_id=self.session_id,
            started_at=datetime.now().isoformat()
        )
        
        # Setup logging
        self.logger = self._setup_logger(log_level)
        self.logger.info(f"Initialized scraper with session ID: {self.session_id}")
        
        # Scraped data storage
        self.workouts: List[HyroxWorkout] = []
        self.scraped_urls: Set[str] = set()
        
    def _setup_logger(self, log_level: str) -> logging.Logger:
        """Setup structured logging"""
        logger = logging.getLogger(f"HyroxScraper.{self.session_id}")
        logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        
        # File handler
        log_file = Path(f"logs/hyrox_scraper_{self.session_id}.log")
        log_file.parent.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(PlaywrightError),
        before_sleep=before_sleep_log(logging.getLogger("HyroxScraper"), logging.WARNING)
    )
    async def scrape_all_workouts(self, max_workouts: int = None) -> List[HyroxWorkout]:
        """
        Scrape all Hyrox workouts from wodwell.com
        
        Args:
            max_workouts: Maximum number of workouts to scrape (None for all)
            
        Returns:
            List of scraped HyroxWorkout objects
        """
        self.logger.info("=" * 80)
        self.logger.info("STARTING HYROX WORKOUTS SCRAPER")
        self.logger.info("=" * 80)
        
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    viewport={'width': 1920, 'height': 1080}
                )
                page = await context.new_page()
                
                # Set default timeout
                page.set_default_timeout(self.PAGE_LOAD_TIMEOUT_MS)
                
                self.logger.info(f"Browser launched successfully")
                
                try:
                    await self._scrape_with_pagination(page, max_workouts)
                    
                    # Final validation
                    self._perform_final_validation()
                    
                    self.logger.info("=" * 80)
                    self.logger.info("SCRAPING COMPLETED SUCCESSFULLY")
                    self.logger.info("=" * 80)
                    
                    return self.workouts
                    
                finally:
                    await browser.close()
                    
            except Exception as e:
                self.logger.error(f"Fatal error during scraping: {str(e)}")
                self.logger.error(traceback.format_exc())
                raise
    
    async def _remove_overlays(self, page: Page):
        """
        Aggressively remove sticky elements/overlays using page.evaluate.
        Removes elements with z-index > 999 or fixed position if they cover the center.
        """
        try:
            await page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('*');
                    const centerX = window.innerWidth / 2;
                    const centerY = window.innerHeight / 2;
                    
                    elements.forEach(el => {
                        const style = window.getComputedStyle(el);
                        const rect = el.getBoundingClientRect();
                        
                        // Check if covers center
                        const coversCenter = (
                            rect.left <= centerX && 
                            rect.right >= centerX && 
                            rect.top <= centerY && 
                            rect.bottom >= centerY
                        );
                        
                        if (coversCenter) {
                            if (style.position === 'fixed' || style.position === 'sticky' || parseInt(style.zIndex) > 999) {
                                console.log('Removing blocking element:', el);
                                el.remove();
                            }
                        }
                    });
                }
            """)
            self.logger.info("Aggressively removed blocking overlays")
        except Exception as e:
            self.logger.warning(f"Error removing overlays: {e}")

    async def _scrape_with_pagination(self, page: Page, max_workouts: int = None):
        """Scrape workouts with pagination handling"""
        url = self.BASE_URL
        self.logger.info(f"Starting URL: {url}")
        
        # Use domcontentloaded instead of networkidle to avoid timeouts on slow assets
        await page.goto(url, wait_until='domcontentloaded', timeout=self.PAGE_LOAD_TIMEOUT_MS)
        
        # Wait for initial content to load
        await page.wait_for_selector('.wod-list', timeout=30000)
        
        self.logger.info("Initial page loaded")
        
        # Check for "Show All" button and click if exists
        try:
            # Handle popups first
            try:
                # Newsletter popup
                popup_close = await page.query_selector('.pum-close')
                if popup_close and await popup_close.is_visible():
                    self.logger.info("Closing newsletter popup...")
                    await popup_close.click(force=True)
                    await asyncio.sleep(1)
                
                # Cookie/GDPR banner
                # Try common accept button selectors
                cookie_btns = [
                    'button:has-text("Accept")',
                    'button:has-text("Agree")',
                    'button:has-text("Allow all")',
                    'button:has-text("I Accept")',
                    '[aria-label="Accept cookies"]',
                    '.cc-btn-accept',
                    '#onetrust-accept-btn-handler'
                ]
                
                for selector in cookie_btns:
                    btn = await page.query_selector(selector)
                    if btn and await btn.is_visible():
                        self.logger.info(f"Closing cookie banner ({selector})...")
                        await btn.click(force=True)
                        await asyncio.sleep(1)
                        break
                        
            except Exception as e:
                self.logger.warning(f"Error handling popups: {e}")

            # Aggressively remove overlays before clicking Show All
            await self._remove_overlays(page)

            show_all_btn = await page.query_selector('button:has-text("Show All")')
            if not show_all_btn:
                # Try partial match or other common selectors
                show_all_btn = await page.query_selector('text="Show All"')
            
            if show_all_btn:
                self.logger.info("Found 'Show All' button, clicking...")
                await show_all_btn.click(force=True)
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(2) # Wait for DOM update
            else:
                self.logger.info("'Show All' button not found, proceeding with scroll")
        except Exception as e:
            self.logger.warning(f"Error checking/clicking 'Show All' button: {e}")

        self.logger.info("Starting infinite scroll")
        
        # Handle infinite scroll
        previous_workout_count = 0
        scroll_attempts = 0
        max_scroll_attempts = 50  # Safety limit
        
        while scroll_attempts < max_scroll_attempts:
            # Scroll to bottom
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await asyncio.sleep(self.SCROLL_WAIT_MS / 1000)
            
            # Get current workout count
            workout_cards = await page.query_selector_all('.wod-list a[href*="/wod/"]')
            current_count = len(workout_cards)
            
            self.logger.info(f"Scroll attempt {scroll_attempts + 1}: Found {current_count} workouts")
            
            # Check if we've loaded new workouts
            if current_count == previous_workout_count:
                # No new workouts loaded, check if we're at the end
                scroll_attempts += 1
                if scroll_attempts >= 3:
                    self.logger.info("No more workouts to load (end of page)")
                    break
            else:
                scroll_attempts = 0
                previous_workout_count = current_count
            
            # Check max workouts limit
            if max_workouts and current_count >= max_workouts:
                self.logger.info(f"Reached max_workouts limit: {max_workouts}")
                workout_cards = workout_cards[:max_workouts]
                break
            
            self.progress.workouts_found = current_count
            self.progress.total_workouts_estimated = current_count
        
        # Scrape all workout cards
        self.logger.info(f"Total workout cards to scrape: {len(workout_cards)}")
        
        for idx, card in enumerate(workout_cards, 1):
            self.logger.info(f"Scraping workout {idx}/{len(workout_cards)}")
            
            try:
                workout = await self._parse_workout_card(card)
                
                if workout:
                    # Check for duplicates
                    if workout.url and workout.url in self.scraped_urls:
                        self.logger.warning(f"Duplicate URL skipped: {workout.url}")
                        self.progress.warnings.append({
                            'type': 'duplicate_url',
                            'url': workout.url,
                            'timestamp': datetime.now().isoformat()
                        })
                        continue
                    
                    self.scraped_urls.add(workout.url)
                    self.workouts.append(workout)
                    self.progress.workouts_scraped += 1
                    
                    self.logger.debug(f"Successfully scraped: {workout.name}")
                else:
                    self.progress.workouts_failed += 1
                    
            except Exception as e:
                self.progress.workouts_failed += 1
                error_info = {
                    'workout_index': idx,
                    'error': str(e),
                    'traceback': traceback.format_exc(),
                    'timestamp': datetime.now().isoformat()
                }
                self.progress.errors.append(error_info)
                self.logger.error(f"Error scraping workout {idx}: {str(e)}")
                self.logger.debug(traceback.format_exc())
            
            # Rate limiting
            if idx % 10 == 0:
                await asyncio.sleep(1)
    
    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=1, max=5)
    )
    async def _parse_workout_card(self, card) -> Optional[HyroxWorkout]:
        """
        Parse a workout card HTML element
        
        Args:
            card: Playwright element handle for workout card
            
        Returns:
            HyroxWorkout object or None if parsing failed
        """
        try:
            workout = HyroxWorkout(session_id=self.session_id)
            
            # Extract URL
            workout.url = await card.get_attribute('href')
            if not workout.url:
                self.logger.warning("No URL found for workout card")
                return None
            
            # Ensure full URL
            if workout.url.startswith('/'):
                workout.url = f"https://wodwell.com{workout.url}"
            
            # Extract wod_id from URL
            wod_id_match = re.search(r'/wod/([a-z0-9-]+)/', workout.url)
            workout.wod_id = wod_id_match.group(1) if wod_id_match else None
            
            # Extract name
            name_el = await card.query_selector('h2')
            workout.name = await name_el.inner_text() if name_el else None
            
            # Extract badge
            badge_el = await card.query_selector('[class*="badge-text"]')
            workout.badge = await badge_el.inner_text() if badge_el else None
            
            # Extract description
            description_spans = await card.query_selector_all('[class*="workout-"] span')
            if description_spans:
                description_parts = []
                for span in description_spans:
                    text = await span.inner_text()
                    if text and text.strip():
                        description_parts.append(text.strip())
                
                workout.full_description = '\n'.join(description_parts)
                
                # Parse workout type and goal
                workout.workout_type = WorkoutParser.parse_workout_type(workout.full_description)
                workout.workout_goal = WorkoutParser.parse_workout_goal(workout.full_description)
                workout.time_specification = WorkoutParser.parse_time_specification(workout.full_description)
                workout.total_time_minutes = WorkoutParser.parse_total_minutes(workout.full_description)
                workout.time_cap_minutes = WorkoutParser.parse_time_cap(workout.full_description)
                
                # Parse description into structured lines
                workout.description_lines = WorkoutParser.parse_description_lines(workout.full_description)
                
                # Parse complex structures
                workout.has_buy_in = 'buy-in' in workout.full_description.lower()
                workout.has_cash_out = 'cash-out' in workout.full_description.lower()
                workout.is_complex = WorkoutParser.detect_complex_structure(workout.description_lines)
                workout.is_interval = 'interval' in workout.full_description.lower() or any(
                    'emom' in line.text.lower() or 'rest' in line.text.lower()
                    for line in workout.description_lines
                )
                
                # Parse structured components
                workout.mini_circuits = WorkoutParser.parse_mini_circuits(workout.description_lines)
                workout.time_segments = WorkoutParser.parse_time_segments(workout.description_lines)
                workout.ladder_rungs = WorkoutParser.parse_ladder_rungs(workout.description_lines, workout.workout_type)
                
                # Calculate total rounds
                circuit_rounds = sum(c.rounds for c in workout.mini_circuits if c.rounds)
                if circuit_rounds > 0:
                    workout.total_rounds = circuit_rounds
                else:
                    workout.total_rounds = WorkoutParser._extract_rounds(workout.full_description)
                
                # Filter out pure headers from description_lines so they don't appear in staging
                # Keep headers that have movement data (e.g. "Cash-Out: 1000m Run")
                workout.description_lines = [
                    line for line in workout.description_lines
                    if not (line.is_header and not line.movement_name)
                ]
            
            # Extract tags (SKIP as per new plan)
            # tags_container = await card.query_selector('[class*="wod-terms"]')
            # if tags_container:
            #     tag_elements = await tags_container.query_selector_all('a')
            #     tags = []
            #     for tag_el in tag_elements:
            #         tag_text = await tag_el.inner_text()
            #         if tag_text and tag_text.strip():
            #             tags.append(tag_text.strip())
            #     workout.tags = tags
            # else:
            #     workout.tags = ['hyrox']
            
            # Extract background image (SKIP as per new plan)
            # bg_image_el = await card.query_selector('[class*="namesake-wod-preview"][style*="background-image"]')
            # if bg_image_el:
            #     style = await bg_image_el.get_attribute('style')
            #     url_match = re.search(r"url\(['\"]?([^'\"]+)['\"]?\)", style or '')
            #     workout.background_image = url_match.group(1) if url_match else None
            
            # Extract stats (SKIP as per new plan)
            # stats_container = await card.query_selector('[data-id]')
            # if stats_container:
            #     workout.stats = await self._parse_stats(stats_container)
            
            # Validate workout data
            is_valid, validation_errors = DataQualityValidator.validate_workout(workout)
            workout.validation_errors = validation_errors
            workout.data_quality = DataQuality.VALID if is_valid else DataQuality.INVALID_FORMAT
            workout.status = ScrapingStatus.COMPLETED if is_valid else ScrapingStatus.PARTIAL
            
            if not is_valid:
                self.logger.warning(f"Validation errors for {workout.name}: {validation_errors}")
            
            return workout
            
        except Exception as e:
            self.logger.error(f"Error parsing workout card: {str(e)}")
            self.logger.debug(traceback.format_exc())
            return None
    
    async def _parse_stats(self, stats_container) -> WorkoutStats:
        """Parse workout statistics"""
        # SKIP stats parsing as per new plan
        return WorkoutStats()
    
    def _perform_final_validation(self):
        """Perform final validation on all scraped workouts"""
        self.logger.info("=" * 80)
        self.logger.info("PERFORMING FINAL VALIDATION")
        self.logger.info("=" * 80)
        
        # Check for duplicates
        duplicates = DataQualityValidator.check_duplicates(self.workouts)
        if duplicates:
            self.logger.warning(f"Found {len(duplicates)} duplicate workouts")
            for duplicate in duplicates[:10]:
                self.logger.warning(f"  {duplicate}")
        
        # Validate all workouts
        valid_count = 0
        partial_count = 0
        failed_count = 0
        
        for workout in self.workouts:
            if workout.status == ScrapingStatus.COMPLETED:
                valid_count += 1
            elif workout.status == ScrapingStatus.PARTIAL:
                partial_count += 1
            else:
                failed_count += 1
        
        self.logger.info(f"Validation Results:")
        self.logger.info(f"  Valid workouts: {valid_count}")
        self.logger.info(f"  Partial workouts: {partial_count}")
        self.logger.info(f"  Failed workouts: {failed_count}")
        
        # Calculate coverage
        total_workouts = len(self.workouts)
        if total_workouts > 0:
            coverage = (valid_count / total_workouts) * 100
            self.logger.info(f"  Data quality coverage: {coverage:.2f}%")
            
            if coverage >= 80:
                self.logger.info("  ✓ Target coverage achieved (80%+)")
            else:
                self.logger.warning(f"  ✗ Target coverage not achieved (80%+)")
    
    def save_to_json(self, output_file: str = None) -> str:
        """
        Save scraped workouts to JSON file
        
        Args:
            output_file: Output file path (auto-generated if None)
            
        Returns:
            Path to saved file
        """
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"hyrox_workouts_scraped_{timestamp}.json"
        
        output_path = Path(output_file)
        
        # Prepare data for serialization
        data = {
            'metadata': {
                'session_id': self.session_id,
                'scraped_at': datetime.now().isoformat(),
                'total_workouts': len(self.workouts),
                'progress': asdict(self.progress),
            },
            'workouts': []
        }
        
        # Convert workouts to dict
        for workout in self.workouts:
            workout_dict = asdict(workout)
            
            # Convert enums to strings
            for key, value in workout_dict.items():
                if isinstance(value, Enum):
                    workout_dict[key] = value.value
            
            data['workouts'].append(workout_dict)
        
        # Write to file
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Data saved to: {output_path.absolute()}")
        
        return str(output_path.absolute())
    
    def get_summary(self) -> Dict:
        """Get scraping summary"""
        return {
            'session_id': self.session_id,
            'started_at': self.progress.started_at,
            'workouts_scraped': self.progress.workouts_scraped,
            'workouts_failed': self.progress.workouts_failed,
            'total_workouts': len(self.workouts),
            'errors_count': len(self.progress.errors),
            'warnings_count': len(self.progress.warnings),
            'coverage_percentage': (
                (len([w for w in self.workouts if w.status == ScrapingStatus.COMPLETED]) / len(self.workouts)) * 100
                if self.workouts else 0
            )
        }


# ============================================================================
# Main Entry Point
# ============================================================================

async def main():
    """Main entry point for Hyrox scraper"""
    print("=" * 80)
    print("HYROX WORKOUTS COMPREHENSIVE SCRAPER")
    print("=" * 80)
    print()
    
    # Configuration
    MAX_WORKOUTS = None  # Set to None to scrape all, or a number to limit
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
    
    # Initialize scraper
    scraper = HyroxWorkoutScraper(log_level=LOG_LEVEL)
    
    try:
        # Scrape workouts
        workouts = await scraper.scrape_all_workouts(max_workouts=MAX_WORKOUTS)
        
        # Save to JSON
        output_file = scraper.save_to_json()
        
        # Print summary
        print("\n" + "=" * 80)
        print("SCRAPING SUMMARY")
        print("=" * 80)
        
        summary = scraper.get_summary()
        print(f"Session ID: {summary['session_id']}")
        print(f"Workouts scraped: {summary['workouts_scraped']}")
        print(f"Workouts failed: {summary['workouts_failed']}")
        print(f"Total workouts: {summary['total_workouts']}")
        print(f"Errors: {summary['errors_count']}")
        print(f"Warnings: {summary['warnings_count']}")
        print(f"Coverage: {summary['coverage_percentage']:.2f}%")
        print(f"\nData saved to: {output_file}")
        
        # Print sample workouts
        print("\n" + "=" * 80)
        print("SAMPLE WORKOUTS (first 5)")
        print("=" * 80)
        
        for i, workout in enumerate(workouts[:5], 1):
            print(f"\n{i}. {workout.name}")
            print(f"   Type: {workout.workout_type.value}")
            print(f"   Goal: {workout.workout_goal.value}")
            print(f"   URL: {workout.url}")
            print(f"   Description lines: {len(workout.description_lines)}")
            print(f"   Movements: {len([l for l in workout.description_lines if l.movement_name])}")
            print(f"   Status: {workout.status.value}")
            print(f"   Quality: {workout.data_quality.value}")
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
    except Exception as e:
        print(f"\n\nFatal error: {str(e)}")
        print("\nCheck the log file for details:")
        print(f"logs/hyrox_scraper_{scraper.session_id}.log")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
