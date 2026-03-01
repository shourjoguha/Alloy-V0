#!/usr/bin/env python3
"""
Pattern Subtype Mapping Verification Script

This script performs comprehensive verification of the pattern_subtype mapping
results from the migration 20260227_enhance_pattern_subtype.sql

Features:
1. Query all movements and show pattern_subtype distribution
2. Identify movements without pattern_subtype assignments
3. Verify the mapping logic used in the migration
4. Show examples of movements for each pattern_subtype
5. Provide statistics on coverage and distribution
6. Export detailed verification report
"""

import psycopg2
import psycopg2.extras
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import os
from pathlib import Path

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

# Database connection settings
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'Jacked-DB',
    'user': 'jacked',
    'password': 'jacked_password'
}

class PatternSubtypeVerifier:
    """Comprehensive verifier for pattern_subtype mappings"""
    
    def __init__(self):
        self.connection = None
        self.verification_results = {}
        
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            logger.info("Connected to database successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    def get_total_movements(self) -> int:
        """Get total number of movements"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM movements")
            return cursor.fetchone()[0]
    
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
        
        with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    
    def get_unmapped_movements(self) -> List[Dict[str, Any]]:
        """Get movements without pattern_subtype assignments"""
        query = """
        SELECT 
            id,
            name,
            pattern::text as original_pattern,
            discipline::text as discipline,
            created_at
        FROM movements 
        WHERE pattern_subtype IS NULL 
        ORDER BY name;
        """
        
        with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    
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
        
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            return {
                'total_movements': row[0],
                'mapped_movements': row[1],
                'unmapped_movements': row[2],
                'coverage_percentage': row[3]
            }
    
    def get_movement_examples_by_subtype(self, limit_per_subtype: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """Get example movements for each pattern_subtype"""
        query = """
        SELECT 
            pattern_subtype,
            name,
            pattern::text as original_pattern,
            discipline::text as discipline,
            created_at
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
        
        with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query, (limit_per_subtype,))
            results = cursor.fetchall()
            
            examples = {}
            for row in results:
                subtype = row['pattern_subtype']
                if subtype not in examples:
                    examples[subtype] = []
                examples[subtype].append({
                    'name': row['name'],
                    'original_pattern': row['original_pattern'],
                    'discipline': row['discipline'],
                    'created_at': row['created_at'].isoformat() if row['created_at'] else None
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
            SELECT COUNT(*) 
            FROM movements 
            WHERE pattern = %s AND pattern_subtype = %s;
            """
            with self.connection.cursor() as cursor:
                cursor.execute(query, (original_pattern, expected_subtype))
                count = cursor.fetchone()[0]
                
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
            SELECT COUNT(*) 
            FROM movements 
            WHERE name ILIKE %s AND pattern_subtype = %s;
            """
            with self.connection.cursor() as cursor:
                cursor.execute(query, (name_pattern, expected_subtype))
                count = cursor.fetchone()[0]
                
                verification_checks.append({
                    'check_type': 'name_based_mapping',
                    'name_pattern': name_pattern,
                    'expected_subtype': expected_subtype,
                    'count': count,
                    'status': 'PASS' if count > 0 else 'INFO'
                })
        
        # Check 3: Verify discipline-based mappings
        discipline_mappings = [
            ('mobility', 'mobility'),
            ('stretch', 'mobility'),
            ('resistance training', None)  # Special case with multiple rules
        ]
        
        for discipline, expected_subtype in discipline_mappings:
            if expected_subtype:
                query = """
                SELECT COUNT(*) 
                FROM movements 
                WHERE discipline = %s AND pattern_subtype = %s;
                """
                with self.connection.cursor() as cursor:
                    cursor.execute(query, (discipline, expected_subtype))
                    count = cursor.fetchone()[0]
                    
                    verification_checks.append({
                        'check_type': 'discipline_based_mapping',
                        'discipline': discipline,
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
        
        with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    
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
                    'host': DB_CONFIG['host'],
                    'database': DB_CONFIG['database'],
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
            
        except Exception as e:
            logger.error(f"Verification failed: {e}")
            return {'error': str(e)}
        finally:
            self.disconnect()
    
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
        report.append(f"Database: {results['database_info']['database']}")
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
            report.append(f"{dist['pattern_subtype']:25} | Count: {dist['count']:4} | {dist['percentage']:6.2f}%")
            if dist['original_patterns']:
                report.append(f"{'':25} | Original Patterns: {dist['original_patterns']}")
            report.append("")
        
        # Unmapped Movements
        report.append("UNMAPPED MOVEMENTS")
        report.append("-" * 40)
        if results['unmapped_movements']:
            report.append(f"Total Unmapped: {len(results['unmapped_movements'])}")
            for i, movement in enumerate(results['unmapped_movements'][:10]):  # Show first 10
                report.append(f"{i+1:2}. {movement['name']:<40} | Pattern: {movement['original_pattern'] or 'None':<15} | Discipline: {movement['discipline'] or 'None'}")
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
                report.append(f"  {i+1}. {example['name']:<35} | Pattern: {example['original_pattern'] or 'None':<15} | Discipline: {example['discipline'] or 'None'}")
        
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
    
    verifier = PatternSubtypeVerifier()
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