#!/usr/bin/env python3
"""
Pattern Subtype Mapping Verification Script - Direct Database Connection

This script performs comprehensive verification of the pattern_subtype mapping
using direct PostgreSQL connection instead of Docker exec, avoiding timeout issues.

Features:
1. Query all movements and show pattern_subtype distribution
2. Identify movements without pattern_subtype assignments
3. Verify the mapping logic used in the migration
4. Show examples of movements for each pattern_subtype
5. Provide statistics on coverage and distribution
6. Export detailed verification report
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pattern_subtype_verification.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Database connection settings from environment
DB_HOST = os.getenv('DATABASE_HOST', 'localhost')
DB_PORT = os.getenv('DATABASE_PORT', '5434')
DB_NAME = os.getenv('DATABASE_NAME', 'Jacked-DB')
DB_USER = os.getenv('DATABASE_USER', 'jacked')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD', 'jackedpass')


class DirectPatternSubtypeVerifier:
    """Comprehensive verifier for pattern_subtype mappings using direct DB connection"""

    def __init__(self):
        self.connection = None
        self.verification_results = {}

    def connect(self) -> bool:
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                connect_timeout=10
            )
            logger.info(f"Connected to database {DB_NAME} at {DB_HOST}:{DB_PORT}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Execute SQL query and return results as list of dicts"""
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params or ())
                results = cursor.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            logger.error(f"Query: {query[:200]}...")
            return []

    def get_total_movements(self) -> int:
        """Get total number of movements"""
        results = self.execute_query("SELECT COUNT(*) as count FROM movements;")
        return int(results[0]['count']) if results else 0

    def get_pattern_subtype_distribution(self) -> List[Dict[str, Any]]:
        """Get distribution of pattern_subtype values"""
        query = """
        SELECT
            pattern_subtype,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM movements), 2) as percentage,
            STRING_AGG(DISTINCT pattern::text, ', ' ORDER BY pattern::text) as original_patterns,
            STRING_AGG(DISTINCT discipline::text, ', ' ORDER BY discipline::text) as disciplines
        FROM movements
        WHERE pattern_subtype IS NOT NULL
        GROUP BY pattern_subtype
        ORDER BY count DESC;
        """
        return self.execute_query(query)

    def get_unmapped_movements(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get movements without pattern_subtype assignments"""
        query = """
        SELECT
            id,
            name,
            pattern::text as original_pattern,
            discipline::text as discipline,
            created_at::text as created_at
        FROM movements
        WHERE pattern_subtype IS NULL
        ORDER BY name
        LIMIT %s;
        """
        return self.execute_query(query, (limit,))

    def get_mapping_coverage_stats(self) -> Dict[str, Any]:
        """Get coverage statistics"""
        query = """
        SELECT
            COUNT(*) as total_movements,
            COUNT(CASE WHEN pattern_subtype IS NOT NULL THEN 1 END) as mapped_movements,
            COUNT(CASE WHEN pattern_subtype IS NULL THEN 1 END) as unmapped_movements,
            ROUND(COUNT(CASE WHEN pattern_subtype IS NOT NULL THEN 1 END) * 100.0 / COUNT(*), 2) as coverage_percentage
        FROM movements;
        """
        results = self.execute_query(query)
        if results:
            row = results[0]
            return {
                'total_movements': int(row['total_movements']),
                'mapped_movements': int(row['mapped_movements']),
                'unmapped_movements': int(row['unmapped_movements']),
                'coverage_percentage': float(row['coverage_percentage'])
            }
        return {
            'total_movements': 0,
            'mapped_movements': 0,
            'unmapped_movements': 0,
            'coverage_percentage': 0.0
        }

    def get_movement_examples_by_subtype(self, limit_per_subtype: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """Get example movements for each pattern_subtype"""
        query = """
        SELECT
            pattern_subtype,
            name,
            pattern::text as original_pattern,
            discipline::text as discipline,
            created_at::text as created_at
        FROM (
            SELECT
                pattern_subtype,
                name,
                pattern,
                discipline,
                created_at,
                ROW_NUMBER() OVER (PARTITION BY pattern_subtype ORDER BY name) as rn
            FROM movements
            WHERE pattern_subtype IS NOT NULL
        ) ranked
        WHERE rn <= %s
        ORDER BY pattern_subtype, name;
        """
        results = self.execute_query(query, (limit_per_subtype,))
        examples = {}
        for row in results:
            subtype = row['pattern_subtype']
            if subtype not in examples:
                examples[subtype] = []
            examples[subtype].append({
                'name': row['name'],
                'original_pattern': row['original_pattern'],
                'discipline': row['discipline'],
                'created_at': row['created_at']
            })
        return examples

    def verify_mapping_logic(self) -> Dict[str, Any]:
        """Verify the mapping logic used in the migration"""
        verification_checks = []

        # Check 1: Verify direct pattern-to-subtype mappings
        direct_mappings = [
            ('squat', 'squat'),
            ('hinge', 'hinge'),
            ('lunge', 'lunge'),
            ('horizontal_push', 'horizontal_push'),
            ('horizontal_pull', 'horizontal_pull'),
            ('vertical_push', 'vertical_push'),
            ('vertical_pull', 'vertical_pull'),
            ('rotation', 'rotation'),
            ('carry', 'carry')
        ]

        for original_pattern, expected_subtype in direct_mappings:
            query = """
            SELECT COUNT(*) as count
            FROM movements
            WHERE pattern = %s AND pattern_subtype = %s;
            """
            results = self.execute_query(query, (original_pattern, expected_subtype))
            count = int(results[0]['count']) if results else 0

            verification_checks.append({
                'check_type': 'direct_pattern_mapping',
                'original_pattern': original_pattern,
                'expected_subtype': expected_subtype,
                'count': count,
                'status': 'PASS' if count > 0 else 'WARNING'
            })

        # Check 2: Verify name-based mappings
        name_patterns = [
            ('%jump%', 'jump'),
            ('%leap%', 'leap'),
            ('%hop%', 'hop'),
            ('%bound%', 'bounding'),
            ('%explosive%', 'explosive'),
            ('%farmer%', 'farmer_carry'),
            ('%waiter%', 'waiter_carry'),
            ('%suitcase%', 'suitcase_carry'),
            ('%run%', 'run'),
            ('%row%', 'row'),
            ('%bike%', 'bike'),
            ('%cycle%', 'cycle'),
            ('%swim%', 'swim'),
            ('%burpee%', 'burpee'),
            ('%turkish%', 'turkish_get_up'),
            ('%bear%crawl%', 'bear_crawl'),
            ('%crab%walk%', 'crab_walk'),
            ('%stretch%', 'stretch'),
            ('%activation%', 'activation'),
            ('%dynamic%', 'dynamic_warmup'),
            ('%static%', 'static_stretch'),
            ('%foam%', 'foam_roll')
        ]

        for name_pattern, expected_subtype in name_patterns:
            query = """
            SELECT COUNT(*) as count
            FROM movements
            WHERE name ILIKE %s AND pattern_subtype = %s;
            """
            results = self.execute_query(query, (name_pattern, expected_subtype))
            count = int(results[0]['count']) if results else 0

            verification_checks.append({
                'check_type': 'name_based_mapping',
                'name_pattern': name_pattern,
                'expected_subtype': expected_subtype,
                'count': count,
                'status': 'PASS' if count > 0 else 'INFO'
            })

        return {
            'total_checks': len(verification_checks),
            'passed_checks': len([c for c in verification_checks if c['status'] == 'PASS']),
            'checks': verification_checks
        }

    def get_discipline_breakdown(self) -> List[Dict[str, Any]]:
        """Get breakdown by discipline and pattern_subtype"""
        query = """
        SELECT
            discipline::text as discipline,
            pattern_subtype,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY discipline), 2) as percentage_within_discipline
        FROM movements
        WHERE discipline IS NOT NULL
        GROUP BY discipline, pattern_subtype
        ORDER BY discipline, count DESC;
        """
        return self.execute_query(query)

    def run_verification(self) -> Dict[str, Any]:
        """Run complete verification process"""
        logger.info("Starting pattern_subtype mapping verification")

        if not self.connect():
            return {'error': 'Failed to connect to database'}

        try:
            # Collect all verification data
            self.verification_results = {
                'timestamp': datetime.now().isoformat(),
                'database_info': {
                    'host': DB_HOST,
                    'port': DB_PORT,
                    'database': DB_NAME,
                    'total_movements': self.get_total_movements()
                },
                'coverage_stats': self.get_mapping_coverage_stats(),
                'pattern_subtype_distribution': self.get_pattern_subtype_distribution(),
                'unmapped_movements': self.get_unmapped_movements(),
                'movement_examples': self.get_movement_examples_by_subtype(),
                'mapping_verification': self.verify_mapping_logic(),
                'discipline_breakdown': self.get_discipline_breakdown()
            }

            logger.info("Verification completed successfully")
            return self.verification_results
        finally:
            self.close()

    def generate_report(self, results: Dict[str, Any], output_format: str = 'both') -> str:
        """Generate verification report in multiple formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_base_path = f"pattern_subtype_verification_report_{timestamp}"

        if output_format in ['json', 'both']:
            json_path = f"{report_base_path}.json"
            with open(json_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"JSON report saved to {json_path}")

        if output_format in ['text', 'both']:
            text_path = f"{report_base_path}.txt"
            with open(text_path, 'w') as f:
                f.write(self._generate_text_report(results))
            logger.info(f"Text report saved to {text_path}")

        return report_base_path

    def _generate_text_report(self, results: Dict[str, Any]) -> str:
        """Generate human-readable text report"""
        report = []
        report.append("=" * 80)
        report.append("PATTERN SUBTYPE MAPPING VERIFICATION REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {results['timestamp']}")
        report.append(f"Database: {results['database_info']['database']} @ {results['database_info']['host']}:{results['database_info']['port']}")
        report.append(f"Total Movements: {results['database_info']['total_movements']}")
        report.append("")

        # Coverage Statistics
        report.append("COVERAGE STATISTICS")
        report.append("-" * 40)
        stats = results['coverage_stats']
        report.append(f"Total Movements: {stats['total_movements']}")
        report.append(f"Mapped Movements: {stats['mapped_movements']}")
        report.append(f"Unmapped Movements: {stats['unmapped_movements']}")
        report.append(f"Coverage Percentage: {stats['coverage_percentage']}%")
        report.append("")

        # Pattern Subtype Distribution
        report.append("PATTERN SUBTYPE DISTRIBUTION")
        report.append("-" * 40)
        for dist in results['pattern_subtype_distribution']:
            report.append(f"{dist['pattern_subtype']:25} | Count: {dist['count']:4} | {float(dist['percentage']):6.2f}%")
            if dist.get('original_patterns'):
                report.append(f"{'':25} | Original Patterns: {dist['original_patterns']}")
            report.append("")

        # Unmapped Movements
        report.append("UNMAPPED MOVEMENTS")
        report.append("-" * 40)
        if results['unmapped_movements']:
            report.append(f"Total Unmapped: {len(results['unmapped_movements'])}")
            for i, movement in enumerate(results['unmapped_movements'][:10]):
                pattern = movement.get('original_pattern', 'None') or 'None'
                discipline = movement.get('discipline', 'None') or 'None'
                report.append(f"{i+1:2}. {movement['name']:<40} | Pattern: {pattern:<15} | Discipline: {discipline}")
            if len(results['unmapped_movements']) > 10:
                report.append(f"... and {len(results['unmapped_movements']) - 10} more unmapped movements")
        else:
            report.append("No unmapped movements found!")
        report.append("")

        # Movement Examples
        report.append("MOVEMENT EXAMPLES BY PATTERN SUBTYPE")
        report.append("-" * 40)
        for subtype, examples in results['movement_examples'].items():
            report.append(f"\n{subtype.upper()}:")
            for i, example in enumerate(examples):
                pattern = example.get('original_pattern', 'None') or 'None'
                discipline = example.get('discipline', 'None') or 'None'
                report.append(f"  {i+1}. {example['name']:<35} | Pattern: {pattern:<15} | Discipline: {discipline}")

        # Mapping Verification Results
        report.append("\nMAPPING VERIFICATION RESULTS")
        report.append("-" * 40)
        verification = results['mapping_verification']
        report.append(f"Total Checks: {verification['total_checks']}")
        report.append(f"Passed Checks: {verification['passed_checks']}")
        report.append(f"Success Rate: {(verification['passed_checks'] / verification['total_checks'] * 100):.1f}%")

        report.append("\nFailed/Warnings:")
        for check in verification['checks']:
            if check['status'] in ['WARNING', 'INFO']:
                report.append(f"  {check['status']:8} | {check['check_type']:<20} | Count: {check.get('count', 0)}")

        report.append("\n" + "=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)

        return "\n".join(report)


def main():
    """Main execution function"""
    logger.info("Starting Pattern Subtype Mapping Verification")

    verifier = DirectPatternSubtypeVerifier()
    results = verifier.run_verification()

    if 'error' in results:
        logger.error(f"Verification failed: {results['error']}")
        return 1

    # Generate reports
    report_path = verifier.generate_report(results, output_format='both')
    logger.info(f"Verification reports generated: {report_path}")

    # Print summary to console
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"Total Movements: {results['coverage_stats']['total_movements']}")
    print(f"Mapped Movements: {results['coverage_stats']['mapped_movements']}")
    print(f"Coverage: {results['coverage_stats']['coverage_percentage']}%")
    print(f"Unmapped: {results['coverage_stats']['unmapped_movements']}")
    print(f"Pattern Subtypes: {len(results['pattern_subtype_distribution'])}")
    print(f"Verification Checks: {results['mapping_verification']['passed_checks']}/{results['mapping_verification']['total_checks']}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    exit(main())
