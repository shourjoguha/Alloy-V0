"""
Validation and Analysis Script for Hyrox Workouts Scraper
Analyzes scraped data and generates quality reports
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Any


def load_scraped_data(json_file: str) -> Dict:
    """Load scraped workout data from JSON file"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_workout_types(workouts: List[Dict]) -> Dict:
    """Analyze workout type distribution"""
    type_counter = Counter()
    goal_counter = Counter()
    
    for workout in workouts:
        workout_type = workout.get('workout_type', 'unknown')
        type_counter[workout_type] += 1
        
        workout_goal = workout.get('workout_goal', 'unknown')
        goal_counter[workout_goal] += 1
    
    return {
        'type_distribution': dict(type_counter.most_common()),
        'goal_distribution': dict(goal_counter.most_common())
    }


def analyze_movements(workouts: List[Dict]) -> Dict:
    """Analyze movement distribution across all workouts"""
    movement_counter = Counter()
    
    for workout in workouts:
        description_lines = workout.get('description_lines', [])
        for line in description_lines:
            movement = line.get('movement_name')
            if movement and movement != 'None':
                movement_counter[movement] += 1
    
    return {
        'movement_distribution': dict(movement_counter.most_common(20)),
        'unique_movements': len(movement_counter),
        'total_movement_instances': sum(movement_counter.values())
    }


def analyze_time_data(workouts: List[Dict]) -> Dict:
    """Analyze time-related data"""
    total_times = []
    time_caps = []
    
    for workout in workouts:
        total_time = workout.get('total_time_minutes')
        if total_time:
            total_times.append(total_time)
        
        time_cap = workout.get('time_cap_minutes')
        if time_cap:
            time_caps.append(time_cap)
    
    def calculate_stats(values: List[float]) -> Dict:
        if not values:
            return {}
        
        values_sorted = sorted(values)
        n = len(values)
        
        return {
            'min': min(values),
            'max': max(values),
            'mean': sum(values) / n,
            'median': values_sorted[n // 2] if n % 2 == 1 else (values_sorted[n // 2 - 1] + values_sorted[n // 2]) / 2,
            'count': n
        }
    
    return {
        'total_time_stats': calculate_stats(total_times),
        'time_cap_stats': calculate_stats(time_caps)
    }


def analyze_complexity(workouts: List[Dict]) -> Dict:
    """Analyze workout complexity"""
    has_buy_in = sum(1 for w in workouts if w.get('has_buy_in', False))
    has_cash_out = sum(1 for w in workouts if w.get('has_cash_out', False))
    is_complex = sum(1 for w in workouts if w.get('is_complex', False))
    is_interval = sum(1 for w in workouts if w.get('is_interval', False))
    
    has_mini_circuits = sum(1 for w in workouts if w.get('mini_circuits'))
    has_time_segments = sum(1 for w in workouts if w.get('time_segments'))
    has_ladder_rungs = sum(1 for w in workouts if w.get('ladder_rungs'))
    
    total = len(workouts)
    
    return {
        'total_workouts': total,
        'with_buy_in': has_buy_in,
        'with_cash_out': has_cash_out,
        'complex_workouts': is_complex,
        'interval_workouts': is_interval,
        'with_mini_circuits': has_mini_circuits,
        'with_time_segments': has_time_segments,
        'with_ladder_rungs': has_ladder_rungs,
        'percentages': {
            'buy_in': (has_buy_in / total * 100) if total > 0 else 0,
            'cash_out': (has_cash_out / total * 100) if total > 0 else 0,
            'complex': (is_complex / total * 100) if total > 0 else 0,
            'interval': (is_interval / total * 100) if total > 0 else 0
        }
    }


def analyze_data_quality(workouts: List[Dict]) -> Dict:
    """Analyze data quality metrics"""
    valid = sum(1 for w in workouts if w.get('status') == 'completed')
    partial = sum(1 for w in workouts if w.get('status') == 'partial')
    failed = sum(1 for w in workouts if w.get('status') == 'failed')
    
    quality_valid = sum(1 for w in workouts if w.get('data_quality') == 'valid')
    quality_invalid = sum(1 for w in workouts if w.get('data_quality') == 'invalid_format')
    quality_incomplete = sum(1 for w in workouts if w.get('data_quality') == 'incomplete')
    
    # Check for missing required fields
    missing_name = sum(1 for w in workouts if not w.get('name'))
    missing_url = sum(1 for w in workouts if not w.get('url'))
    missing_description = sum(1 for w in workouts if not w.get('full_description'))
    
    total = len(workouts)
    
    return {
        'status_distribution': {
            'completed': valid,
            'partial': partial,
            'failed': failed
        },
        'quality_distribution': {
            'valid': quality_valid,
            'invalid_format': quality_invalid,
            'incomplete': quality_incomplete
        },
        'missing_fields': {
            'name': missing_name,
            'url': missing_url,
            'description': missing_description
        },
        'coverage_percentage': (valid / total * 100) if total > 0 else 0
    }


def analyze_engagement(workouts: List[Dict]) -> Dict:
    """Analyze user engagement stats"""
    favorites = []
    comments = []
    
    for workout in workouts:
        stats = workout.get('stats', {})
        favorites.append(stats.get('favorites', 0))
        comments.append(stats.get('comments', 0))
    
    def calculate_stats(values: List[int]) -> Dict:
        if not values:
            return {}
        
        values_sorted = sorted(values)
        n = len(values)
        
        return {
            'min': min(values),
            'max': max(values),
            'mean': sum(values) / n,
            'median': values_sorted[n // 2] if n % 2 == 1 else (values_sorted[n // 2 - 1] + values_sorted[n // 2]) / 2,
            'total': sum(values),
            'count': n
        }
    
    return {
        'favorites_stats': calculate_stats(favorites),
        'comments_stats': calculate_stats(comments)
    }


def generate_validation_report(data: Dict, output_file: str = None) -> str:
    """Generate comprehensive validation report"""
    metadata = data.get('metadata', {})
    workouts = data.get('workouts', [])
    
    # Run all analyses
    type_analysis = analyze_workout_types(workouts)
    movement_analysis = analyze_movements(workouts)
    time_analysis = analyze_time_data(workouts)
    complexity_analysis = analyze_complexity(workouts)
    quality_analysis = analyze_data_quality(workouts)
    engagement_analysis = analyze_engagement(workouts)
    
    # Build report
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("HYROX WORKOUTS VALIDATION REPORT")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    # Metadata
    report_lines.append("METADATA")
    report_lines.append("-" * 80)
    report_lines.append(f"Session ID: {metadata.get('session_id', 'N/A')}")
    report_lines.append(f"Scraped At: {metadata.get('scraped_at', 'N/A')}")
    report_lines.append(f"Total Workouts: {metadata.get('total_workouts', len(workouts))}")
    report_lines.append("")
    
    # Data Quality
    report_lines.append("DATA QUALITY")
    report_lines.append("-" * 80)
    quality = quality_analysis
    report_lines.append(f"Coverage: {quality.get('coverage_percentage', 0):.2f}%")
    report_lines.append(f"Valid Workouts: {quality['status_distribution']['completed']}")
    report_lines.append(f"Partial Workouts: {quality['status_distribution']['partial']}")
    report_lines.append(f"Failed Workouts: {quality['status_distribution']['failed']}")
    report_lines.append("")
    report_lines.append("Missing Required Fields:")
    report_lines.append(f"  - Name: {quality['missing_fields']['name']}")
    report_lines.append(f"  - URL: {quality['missing_fields']['url']}")
    report_lines.append(f"  - Description: {quality['missing_fields']['description']}")
    report_lines.append("")
    
    # Workout Types
    report_lines.append("WORKOUT TYPE DISTRIBUTION")
    report_lines.append("-" * 80)
    for workout_type, count in type_analysis['type_distribution'].items():
        percentage = (count / len(workouts)) * 100 if workouts else 0
        report_lines.append(f"{workout_type}: {count} ({percentage:.1f}%)")
    report_lines.append("")
    
    # Workout Goals
    report_lines.append("WORKOUT GOAL DISTRIBUTION")
    report_lines.append("-" * 80)
    for goal, count in type_analysis['goal_distribution'].items():
        percentage = (count / len(workouts)) * 100 if workouts else 0
        report_lines.append(f"{goal}: {count} ({percentage:.1f}%)")
    report_lines.append("")
    
    # Movement Analysis
    report_lines.append("MOVEMENT ANALYSIS")
    report_lines.append("-" * 80)
    report_lines.append(f"Unique Movements: {movement_analysis['unique_movements']}")
    report_lines.append(f"Total Movement Instances: {movement_analysis['total_movement_instances']}")
    report_lines.append("")
    report_lines.append("Top 20 Movements:")
    for movement, count in list(movement_analysis['movement_distribution'].items())[:20]:
        percentage = (count / movement_analysis['total_movement_instances']) * 100 if movement_analysis['total_movement_instances'] > 0 else 0
        report_lines.append(f"  {movement}: {count} ({percentage:.1f}%)")
    report_lines.append("")
    
    # Time Analysis
    report_lines.append("TIME ANALYSIS")
    report_lines.append("-" * 80)
    total_time_stats = time_analysis.get('total_time_stats', {})
    if total_time_stats:
        report_lines.append("Total Workout Time (minutes):")
        report_lines.append(f"  - Min: {total_time_stats.get('min', 'N/A')}")
        report_lines.append(f"  - Max: {total_time_stats.get('max', 'N/A')}")
        report_lines.append(f"  - Mean: {total_time_stats.get('mean', 0):.1f}")
        report_lines.append(f"  - Median: {total_time_stats.get('median', 0):.1f}")
        report_lines.append("")
    
    time_cap_stats = time_analysis.get('time_cap_stats', {})
    if time_cap_stats:
        report_lines.append("Time Cap (minutes):")
        report_lines.append(f"  - Min: {time_cap_stats.get('min', 'N/A')}")
        report_lines.append(f"  - Max: {time_cap_stats.get('max', 'N/A')}")
        report_lines.append(f"  - Mean: {time_cap_stats.get('mean', 0):.1f}")
        report_lines.append(f"  - Median: {time_cap_stats.get('median', 0):.1f}")
        report_lines.append("")
    
    # Complexity Analysis
    report_lines.append("WORKOUT COMPLEXITY")
    report_lines.append("-" * 80)
    complexity = complexity_analysis
    report_lines.append(f"Total Workouts: {complexity['total_workouts']}")
    report_lines.append(f"Complex Workouts: {complexity['complex_workouts']} ({complexity['percentages']['complex']:.1f}%)")
    report_lines.append(f"Interval Workouts: {complexity['interval_workouts']} ({complexity['percentages']['interval']:.1f}%)")
    report_lines.append(f"With Buy-In: {complexity['with_buy_in']} ({complexity['percentages']['buy_in']:.1f}%)")
    report_lines.append(f"With Cash-Out: {complexity['with_cash_out']} ({complexity['percentages']['cash_out']:.1f}%)")
    report_lines.append(f"With Mini Circuits: {complexity['with_mini_circuits']}")
    report_lines.append(f"With Time Segments: {complexity['with_time_segments']}")
    report_lines.append(f"With Ladder Rungs: {complexity['with_ladder_rungs']}")
    report_lines.append("")
    
    # Engagement Analysis
    report_lines.append("USER ENGAGEMENT")
    report_lines.append("-" * 80)
    fav_stats = engagement_analysis.get('favorites_stats', {})
    if fav_stats:
        report_lines.append("Favorites:")
        report_lines.append(f"  - Min: {fav_stats.get('min', 'N/A')}")
        report_lines.append(f"  - Max: {fav_stats.get('max', 'N/A')}")
        report_lines.append(f"  - Mean: {fav_stats.get('mean', 0):.1f}")
        report_lines.append(f"  - Median: {fav_stats.get('median', 0):.1f}")
        report_lines.append(f"  - Total: {fav_stats.get('total', 0)}")
        report_lines.append("")
    
    comment_stats = engagement_analysis.get('comments_stats', {})
    if comment_stats:
        report_lines.append("Comments:")
        report_lines.append(f"  - Min: {comment_stats.get('min', 'N/A')}")
        report_lines.append(f"  - Max: {comment_stats.get('max', 'N/A')}")
        report_lines.append(f"  - Mean: {comment_stats.get('mean', 0):.1f}")
        report_lines.append(f"  - Median: {comment_stats.get('median', 0):.1f}")
        report_lines.append(f"  - Total: {comment_stats.get('total', 0)}")
        report_lines.append("")
    
    # Quality Assessment
    report_lines.append("=" * 80)
    report_lines.append("QUALITY ASSESSMENT")
    report_lines.append("=" * 80)
    
    coverage = quality_analysis.get('coverage_percentage', 0)
    if coverage >= 90:
        status = "EXCELLENT"
        emoji = "✓"
    elif coverage >= 80:
        status = "GOOD"
        emoji = "✓"
    elif coverage >= 70:
        status = "ACCEPTABLE"
        emoji = "~"
    else:
        status = "NEEDS IMPROVEMENT"
        emoji = "✗"
    
    report_lines.append(f"Overall Status: {status} {emoji}")
    report_lines.append(f"Coverage: {coverage:.2f}%")
    report_lines.append("")
    
    if coverage >= 80:
        report_lines.append("✓ Target coverage achieved (80%+)")
    else:
        report_lines.append(f"✗ Target coverage not achieved (80%+)")
    
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("END OF REPORT")
    report_lines.append("=" * 80)
    
    report_text = "\n".join(report_lines)
    
    # Print report
    print(report_text)
    
    # Save to file
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"\nReport saved to: {output_path.absolute()}")
    
    return report_text


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python validate_hyrox_scraper.py <json_file> [output_report_file]")
        print("\nExample:")
        print("  python validate_hyrox_scraper.py hyrox_workouts_scraped_20260228_120000.json")
        print("  python validate_hyrox_scraper.py hyrox_workouts_scraped_20260228_120000.json validation_report.txt")
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_report = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"Loading data from: {json_file}")
    
    try:
        data = load_scraped_data(json_file)
        print(f"Loaded {len(data.get('workouts', []))} workouts")
        print()
        
        generate_validation_report(data, output_report)
        
    except FileNotFoundError:
        print(f"Error: File not found: {json_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
