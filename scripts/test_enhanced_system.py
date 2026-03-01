"""
Test Script for Enhanced Alloy AI Fitness System
Tests 5-day program generation with comprehensive error logging.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from services.error_logger import error_logger
from services.safe_migration_runner import run_migration_safely
from services.enhanced_program_service import EnhancedProgramService
from services.enhanced_movement_query_service_v2 import EnhancedMovementQueryServiceV2
from models.program import ProgramGenerationRequest
from models.enums import SessionType, PrimaryRegion


class EnhancedSystemTester:
    """Comprehensive tester for the enhanced Alloy AI system."""
    
    def __init__(self, database_url: str = "postgresql+asyncpg://jacked:jackedpass@localhost:5434/Jacked-DB"):
        """Initialize tester with database connection."""
        self.database_url = database_url
        self.engine = create_async_engine(database_url, echo=True)
        self.async_session = sessionmaker(self.engine, class_=AsyncSession)
        self.test_results = []
    
    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive test suite for the enhanced system."""
        print("🚀 Starting Enhanced Alloy AI System Test Suite")
        print("=" * 60)
        
        test_results = {
            "test_start_time": datetime.utcnow().isoformat(),
            "tests_run": [],
            "tests_passed": 0,
            "tests_failed": 0,
            "errors": []
        }
        
        try:
            async with self.async_session() as session:
                # Test 1: Database Migration
                migration_result = await self._test_pattern_subtype_migration(session)
                test_results["tests_run"].append(migration_result)
                if migration_result["success"]:
                    test_results["tests_passed"] += 1
                else:
                    test_results["tests_failed"] += 1
                    test_results["errors"].extend(migration_result.get("errors", []))
                
                if migration_result["success"]:
                    # Test 2: Enhanced Movement Service
                    movement_result = await self._test_enhanced_movement_service(session)
                    test_results["tests_run"].append(movement_result)
                    if movement_result["success"]:
                        test_results["tests_passed"] += 1
                    else:
                        test_results["tests_failed"] += 1
                        test_results["errors"].extend(movement_result.get("errors", []))
                    
                    # Test 3: 5-Day Program Generation
                    program_result = await self._test_5_day_program_generation(session)
                    test_results["tests_run"].append(program_result)
                    if program_result["success"]:
                        test_results["tests_passed"] += 1
                    else:
                        test_results["tests_failed"] += 1
                        test_results["errors"].extend(program_result.get("errors", []))
                    
                    # Test 4: Day Spacing Logic
                    spacing_result = await self._test_day_spacing_logic(session)
                    test_results["tests_run"].append(spacing_result)
                    if spacing_result["success"]:
                        test_results["tests_passed"] += 1
                    else:
                        test_results["tests_failed"] += 1
                        test_results["errors"].extend(spacing_result.get("errors", []))
                    
                    # Test 5: Region Rotation Logic
                    rotation_result = await self._test_region_rotation_logic(session)
                    test_results["tests_run"].append(rotation_result)
                    if rotation_result["success"]:
                        test_results["tests_passed"] += 1
                    else:
                        test_results["tests_failed"] += 1
                        test_results["errors"].extend(rotation_result.get("errors", []))
        
        except Exception as e:
            error_trace_id = error_logger.log_error(
                error_code="TEST_SUITE_FAILURE",
                error_message="Test suite failed with unexpected error",
                error_details={"error_type": type(e).__name__, "error_message": str(e)},
                context={"test_phase": "initialization"}
            )
            test_results["errors"].append(f"Test suite initialization failed: {str(e)}")
            test_results["test_suite_error_trace_id"] = error_trace_id
        
        finally:
            test_results["test_end_time"] = datetime.utcnow().isoformat()
            test_results["total_duration_seconds"] = (
                datetime.fromisoformat(test_results["test_end_time"]) - 
                datetime.fromisoformat(test_results["test_start_time"])
            ).total_seconds()
        
        return test_results
    
    async def _test_pattern_subtype_migration(self, session: AsyncSession) -> Dict[str, Any]:
        """Test the pattern_subtype migration."""
        print("\n📊 Test 1: Pattern Subtype Migration")
        print("-" * 40)
        
        test_result = {
            "test_name": "Pattern Subtype Migration",
            "success": False,
            "errors": [],
            "warnings": [],
            "details": {}
        }
        
        try:
            # Load migration SQL
            migration_path = Path(__file__).parent / "migrations" / "20260227_enhance_pattern_subtype.sql"
            
            if not migration_path.exists():
                test_result["errors"].append(f"Migration file not found: {migration_path}")
                return test_result
            
            with open(migration_path, 'r') as f:
                migration_sql = f.read()
            
            # Run migration with dry run first
            print("🧪 Running dry-run simulation...")
            dry_run_result = await run_migration_safely(
                db_session=session,
                migration_sql=migration_sql,
                migration_name="20260227_enhance_pattern_subtype",
                backup_before=True,
                dry_run=True
            )
            
            test_result["dry_run"] = dry_run_result
            
            if dry_run_result.get("errors"):
                test_result["errors"].extend(dry_run_result["errors"])
                print(f"❌ Dry-run failed with errors")
                return test_result
            
            if dry_run_result.get("warnings"):
                test_result["warnings"].extend(dry_run_result["warnings"])
                print(f"⚠️  Dry-run completed with warnings")
            
            print("✅ Dry-run simulation successful")
            print("🚀 Executing actual migration...")
            
            # Run actual migration
            migration_result = await run_migration_safely(
                db_session=session,
                migration_sql=migration_sql,
                migration_name="20260227_enhance_pattern_subtype",
                backup_before=True,
                dry_run=False
            )
            
            test_result["migration_result"] = migration_result
            
            if migration_result["success"]:
                print("✅ Migration executed successfully")
                
                # Verify migration results
                verification_result = await self._verify_migration_results(session)
                test_result["verification"] = verification_result
                
                if verification_result["success"]:
                    test_result["success"] = True
                    print(f"✅ Migration verification passed")
                    print(f"   Pattern subtypes created: {verification_result['pattern_subtype_count']}")
                    print(f"   Movements with subtypes: {verification_result['movements_with_subtype']}")
                else:
                    test_result["errors"].extend(verification_result.get("errors", []))
                    print(f"❌ Migration verification failed")
            else:
                test_result["errors"].extend(migration_result.get("errors", []))
                print(f"❌ Migration failed")
        
        except Exception as e:
            error_trace_id = error_logger.log_migration_error(
                migration_name="20260227_enhance_pattern_subtype_test",
                error=e,
                context={"test_phase": "pattern_subtype_migration"}
            )
            test_result["errors"].append(f"Migration test failed: {str(e)}")
            test_result["error_trace_id"] = error_trace_id
        
        return test_result
    
    async def _verify_migration_results(self, session: AsyncSession) -> Dict[str, Any]:
        """Verify that the migration produced expected results."""
        verification_result = {
            "success": False,
            "errors": [],
            "pattern_subtype_count": 0,
            "movements_with_subtype": 0,
            "pattern_subtype_distribution": {}
        }
        
        try:
            # Check if pattern_subtype column exists
            check_column_query = text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns 
                    WHERE table_name = 'movements' 
                    AND column_name = 'pattern_subtype'
                )
            """)
            
            result = await session.execute(check_column_query)
            column_exists = result.scalar()
            
            if not column_exists:
                verification_result["errors"].append("pattern_subtype column not found")
                return verification_result
            
            # Count pattern subtypes
            count_query = text("""
                SELECT pattern_subtype::text as pattern_subtype_text, COUNT(*) as count
                FROM movements 
                WHERE pattern_subtype IS NOT NULL
                GROUP BY pattern_subtype
                ORDER BY count DESC
            """)
            
            result = await session.execute(count_query)
            subtype_counts = result.fetchall()
            
            verification_result["pattern_subtype_count"] = len(subtype_counts)
            verification_result["movements_with_subtype"] = sum(row[1] for row in subtype_counts)
            verification_result["pattern_subtype_distribution"] = {
                row[0]: row[1] for row in subtype_counts
            }
            
            # Check for expected subtypes
            expected_subtypes = {
                "squat", "hinge", "horizontal_push", "horizontal_pull",
                "vertical_push", "vertical_pull", "lunge", "rotation",
                "carry", "jump", "run", "row", "bike", "swim",
                "mobility", "stretch", "activation"
            }
            
            found_subtypes = {row[0] for row in subtype_counts}
            missing_subtypes = expected_subtypes - found_subtypes
            
            if missing_subtypes:
                verification_result["warnings"] = [f"Missing expected subtypes: {missing_subtypes}"]
            
            # Check for movements without subtypes
            null_count_query = text("SELECT COUNT(*) FROM movements WHERE pattern_subtype IS NULL")
            result = await session.execute(null_count_query)
            null_count = result.scalar()
            
            if null_count > 0:
                verification_result["warnings"] = [f"{null_count} movements without pattern_subtype"]
            
            verification_result["success"] = True
            
        except Exception as e:
            error_logger.log_error(
                error_code="MIGRATION_VERIFICATION_FAILED",
                error_message="Failed to verify migration results",
                error_details={"error_type": type(e).__name__, "error_message": str(e)},
                context={"verification_phase": "pattern_subtype"}
            )
            verification_result["errors"].append(f"Verification failed: {str(e)}")
        
        return verification_result
    
    async def _test_enhanced_movement_service(self, session: AsyncSession) -> Dict[str, Any]:
        """Test the enhanced movement query service."""
        print("\n🏋️ Test 2: Enhanced Movement Query Service")
        print("-" * 40)
        
        test_result = {
            "test_name": "Enhanced Movement Service",
            "success": False,
            "errors": [],
            "warnings": [],
            "details": {}
        }
        
        try:
            # Initialize enhanced movement service
            movement_service = EnhancedMovementQueryServiceV2(session)
            
            # Test different movement categories
            test_cases = [
                {
                    "name": "Warmup Movements",
                    "method": "get_warmup_movements",
                    "params": {"equipment_available": ["bodyweight", "band"], "max_movements": 5}
                },
                {
                    "name": "Strength Movements",
                    "method": "get_strength_movements", 
                    "params": {"equipment_available": ["barbell", "dumbbell"], "max_movements": 6}
                },
                {
                    "name": "Cardio Movements",
                    "method": "get_cardio_movements",
                    "params": {"equipment_available": ["bodyweight"], "max_movements": 4}
                }
            ]
            
            for test_case in test_cases:
                print(f"🧪 Testing {test_case['name']}...")
                
                try:
                    method = getattr(movement_service, test_case["method"])
                    result = await method(**test_case["params"])
                    
                    test_result["details"][test_case["name"]] = {
                        "success": True,
                        "movement_count": len(result),
                        "sample_movements": [m["name"] for m in result[:3]] if result else []
                    }
                    
                    print(f"✅ {test_case['name']}: Found {len(result)} movements")
                    
                except Exception as e:
                    error_logger.log_error(
                        error_code="MOVEMENT_SERVICE_TEST_FAILED",
                        error_message=f"Failed to test {test_case['name']}",
                        error_details={"test_case": test_case["name"], "error": str(e)},
                        context={"test_phase": "movement_service"}
                    )
                    test_result["errors"].append(f"{test_case['name']} test failed: {str(e)}")
            
            test_result["success"] = len(test_result["errors"]) == 0
            
        except Exception as e:
            error_trace_id = error_logger.log_error(
                error_code="MOVEMENT_SERVICE_INIT_FAILED",
                error_message="Failed to initialize movement service",
                error_details={"error_type": type(e).__name__, "error_message": str(e)},
                context={"test_phase": "movement_service_initialization"}
            )
            test_result["errors"].append(f"Movement service initialization failed: {str(e)}")
            test_result["error_trace_id"] = error_trace_id
        
        return test_result
    
    async def _test_5_day_program_generation(self, session: AsyncSession) -> Dict[str, Any]:
        """Test 5-day program generation with enhanced service."""
        print("\n📅 Test 3: 5-Day Program Generation")
        print("-" * 40)
        
        test_result = {
            "test_name": "5-Day Program Generation",
            "success": False,
            "errors": [],
            "warnings": [],
            "details": {}
        }
        
        try:
            # Create test request for 5-day program
            test_request = ProgramGenerationRequest(
                normalized_goals={
                    "primary_strength": 0.7,
                    "normalized_hypertrophy_fat_loss": 0.5,
                    "normalized_power_mobility": 0.3,
                    "strength_bias": 0.8,
                    "endurance_bias": 0.4
                },
                availability={"days_per_week": 5},
                equipment_available=["barbell", "dumbbell", "bodyweight"],
                program_length_weeks=8,
                user_level="intermediate"
            )
            
            # Initialize enhanced program service
            program_service = EnhancedProgramService(db_session=session)
            
            print("🧪 Generating 5-day program...")
            
            # Generate program
            result = await program_service.generate_program_skeleton(test_request)
            
            if result.success:
                print("✅ Program generation successful")
                
                # Analyze the generated program
                program_skeleton = result.program_skeleton
                
                test_result["details"] = {
                    "total_weeks": len(program_skeleton.training_blocks),
                    "total_sessions": self._count_total_sessions(program_skeleton),
                    "session_breakdown": result.session_breakdown,
                    "sample_week": self._analyze_sample_week(program_skeleton)
                }
                
                # Validate day distribution
                day_validation = self._validate_day_distribution(program_skeleton)
                if not day_validation["valid"]:
                    test_result["warnings"].extend(day_validation["issues"])
                
                test_result["success"] = True
                
            else:
                test_result["errors"] = result.errors or ["Program generation failed without specific errors"]
                print(f"❌ Program generation failed: {result.errors}")
                
                # Log detailed error
                error_logger.log_program_generation_error(
                    error=Exception("Program generation failed"),
                    request_data=test_request.dict(),
                    validation_errors=result.errors
                )
        
        except Exception as e:
            error_trace_id = error_logger.log_program_generation_error(
                error=e,
                request_data=test_request.dict() if 'test_request' in locals() else None,
                context={"test_phase": "5_day_program_generation"}
            )
            test_result["errors"].append(f"5-day program generation test failed: {str(e)}")
            test_result["error_trace_id"] = error_trace_id
        
        return test_result
    
    def _count_total_sessions(self, program_skeleton) -> int:
        """Count total sessions in program skeleton."""
        total = 0
        for block in program_skeleton.training_blocks:
            for week in block.weekly_plans:
                total += len(week.sessions)
        return total
    
    def _analyze_sample_week(self, program_skeleton) -> Dict[str, Any]:
        """Analyze a sample week from the program."""
        if not program_skeleton.training_blocks:
            return {}
        
        sample_block = program_skeleton.training_blocks[0]
        if not sample_block.weekly_plans:
            return {}
        
        sample_week = sample_block.weekly_plans[0]
        
        return {
            "week_number": sample_week.week_number,
            "session_count": len(sample_week.sessions),
            "session_types": [s.session_type.value for s in sample_week.sessions],
            "training_days": [s.day_number for s in sample_week.sessions]
        }
    
    def _validate_day_distribution(self, program_skeleton) -> Dict[str, Any]:
        """Validate that training days are properly distributed."""
        validation = {
            "valid": True,
            "issues": []
        }
        
        # This is a placeholder - would need actual implementation
        # to check for proper day spacing (e.g., 2 active, 1 rest, 2 active, etc.)
        
        return validation
    
    async def _test_day_spacing_logic(self, session: AsyncSession) -> Dict[str, Any]:
        """Test the intelligent day spacing logic."""
        print("\n📊 Test 4: Day Spacing Logic")
        print("-" * 40)
        
        test_result = {
            "test_name": "Day Spacing Logic",
            "success": False,
            "errors": [],
            "warnings": [],
            "details": {}
        }
        
        try:
            # Test different day configurations
            day_configs = [3, 4, 5, 6]
            
            for days_per_week in day_configs:
                print(f"🧪 Testing {days_per_week} days per week...")
                
                # Create test request
                test_request = ProgramGenerationRequest(
                    normalized_goals={
                        "primary_strength": 0.6,
                        "normalized_hypertrophy_fat_loss": 0.5,
                        "normalized_power_mobility": 0.4,
                        "strength_bias": 0.7,
                        "endurance_bias": 0.5
                    },
                    availability={"days_per_week": days_per_week},
                    equipment_available=["barbell", "dumbbell"],
                    program_length_weeks=8,
                    user_level="intermediate"
                )
                
                program_service = EnhancedProgramService(db_session=session)
                result = await program_service.generate_program_skeleton(test_request)
                
                if result.success:
                    day_analysis = self._analyze_day_spacing(result.program_skeleton, days_per_week)
                    test_result["details"][f"{days_per_week}_days"] = day_analysis
                    
                    if day_analysis["valid_spacing"]:
                        print(f"✅ {days_per_week} days: Valid spacing")
                    else:
                        test_result["warnings"].extend(day_analysis["spacing_issues"])
                        print(f"⚠️  {days_per_week} days: Spacing issues detected")
                else:
                    test_result["errors"].append(f"Failed to generate {days_per_week}-day program")
            
            test_result["success"] = len(test_result["errors"]) == 0
            
        except Exception as e:
            error_trace_id = error_logger.log_error(
                error_code="DAY_SPACING_TEST_FAILED",
                error_message="Day spacing logic test failed",
                error_details={"error_type": type(e).__name__, "error_message": str(e)},
                context={"test_phase": "day_spacing"}
            )
            test_result["errors"].append(f"Day spacing test failed: {str(e)}")
            test_result["error_trace_id"] = error_trace_id
        
        return test_result
    
    def _analyze_day_spacing(self, program_skeleton, expected_days_per_week) -> Dict[str, Any]:
        """Analyze day spacing in generated program."""
        analysis = {
            "valid_spacing": True,
            "spacing_issues": [],
            "training_days": [],
            "rest_days": [],
            "consecutive_training_days": 0,
            "max_consecutive_rest": 0
        }
        
        # Extract training days from first week
        if program_skeleton.training_blocks and program_skeleton.training_blocks[0].weekly_plans:
            first_week = program_skeleton.training_blocks[0].weekly_plans[0]
            training_days = sorted([s.day_number for s in first_week.sessions])
            
            analysis["training_days"] = training_days
            analysis["rest_days"] = [day for day in range(1, 8) if day not in training_days]
            
            # Check for valid spacing patterns
            if len(training_days) != expected_days_per_week:
                analysis["spacing_issues"].append(
                    f"Expected {expected_days_per_week} training days, got {len(training_days)}"
                )
                analysis["valid_spacing"] = False
            
            # Check consecutive training days
            consecutive = 1
            max_consecutive = 1
            for i in range(1, len(training_days)):
                if training_days[i] == training_days[i-1] + 1:
                    consecutive += 1
                    max_consecutive = max(max_consecutive, consecutive)
                else:
                    consecutive = 1
            
            analysis["consecutive_training_days"] = max_consecutive
            
            # For 5-day programs, we expect max 2 consecutive training days
            if expected_days_per_week == 5 and max_consecutive > 2:
                analysis["spacing_issues"].append(
                    f"Too many consecutive training days: {max_consecutive} (expected max 2)"
                )
                analysis["valid_spacing"] = False
        
        return analysis
    
    async def _test_region_rotation_logic(self, session: AsyncSession) -> Dict[str, Any]:
        """Test the primary region rotation logic."""
        print("\n🔄 Test 5: Region Rotation Logic")
        print("-" * 40)
        
        test_result = {
            "test_name": "Region Rotation Logic",
            "success": False,
            "errors": [],
            "warnings": [],
            "details": {}
        }
        
        try:
            # Test resistance-focused program (should have region rotation)
            test_request = ProgramGenerationRequest(
                normalized_goals={
                    "primary_strength": 0.8,
                    "normalized_hypertrophy_fat_loss": 0.6,
                    "normalized_power_mobility": 0.2,
                    "strength_bias": 0.9,
                    "endurance_bias": 0.3
                },
                availability={"days_per_week": 5},
                equipment_available=["barbell", "dumbbell", "bodyweight"],
                program_length_weeks=8,
                user_level="intermediate"
            )
            
            program_service = EnhancedProgramService(db_session=session)
            result = await program_service.generate_program_skeleton(test_request)
            
            if result.success:
                region_analysis = self._analyze_region_rotation(result.program_skeleton)
                test_result["details"] = region_analysis
                
                if region_analysis["valid_rotation"]:
                    print("✅ Region rotation logic working correctly")
                    test_result["success"] = True
                else:
                    test_result["warnings"].extend(region_analysis["rotation_issues"])
                    print(f"⚠️  Region rotation issues: {region_analysis['rotation_issues']}")
            else:
                test_result["errors"].append("Failed to generate program for region rotation test")
        
        except Exception as e:
            error_trace_id = error_logger.log_error(
                error_code="REGION_ROTATION_TEST_FAILED",
                error_message="Region rotation logic test failed",
                error_details={"error_type": type(e).__name__, "error_message": str(e)},
                context={"test_phase": "region_rotation"}
            )
            test_result["errors"].append(f"Region rotation test failed: {str(e)}")
            test_result["error_trace_id"] = error_trace_id
        
        return test_result
    
    def _analyze_region_rotation(self, program_skeleton) -> Dict[str, Any]:
        """Analyze region rotation in generated program."""
        analysis = {
            "valid_rotation": True,
            "rotation_issues": [],
            "consecutive_same_regions": 0,
            "region_sequence": [],
            "upper_lower_balance": {"upper": 0, "lower": 0, "full": 0}
        }
        
        # Extract region sequence from sessions
        regions = []
        if program_skeleton.training_blocks and program_skeleton.training_blocks[0].weekly_plans:
            for week in program_skeleton.training_blocks[0].weekly_plans[:2]:  # First 2 weeks
                for session in week.sessions:
                    # This is simplified - would need actual region extraction logic
                    if session.session_type in [SessionType.RESISTANCE_ACCESSORY, SessionType.RESISTANCE_CIRCUITS]:
                        regions.append("resistance")  # Placeholder
        
        analysis["region_sequence"] = regions
        
        # Check for consecutive same regions (simplified logic)
        consecutive_count = 1
        max_consecutive = 1
        for i in range(1, len(regions)):
            if regions[i] == regions[i-1]:
                consecutive_count += 1
                max_consecutive = max(max_consecutive, consecutive_count)
            else:
                consecutive_count = 1
        
        analysis["consecutive_same_regions"] = max_consecutive
        
        if max_consecutive > 2:
            analysis["rotation_issues"].append(
                f"Too many consecutive same regions: {max_consecutive} (expected max 2)"
            )
            analysis["valid_rotation"] = False
        
        return analysis


async def main():
    """Main test execution."""
    print("🚀 Enhanced Alloy AI Fitness System Test Suite")
    print("=" * 60)
    
    tester = EnhancedSystemTester()
    
    try:
        # Run comprehensive test
        results = await tester.run_comprehensive_test()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        print(f"✅ Tests Passed: {results['tests_passed']}")
        print(f"❌ Tests Failed: {results['tests_failed']}")
        print(f"⏱️  Total Duration: {results['total_duration_seconds']:.2f} seconds")
        
        if results['errors']:
            print(f"\n🚨 Errors Encountered:")
            for error in results['errors']:
                print(f"   - {error}")
        
        # Save detailed results
        results_path = Path(__file__).parent / "test_results" / f"enhanced_system_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        results_path.parent.mkdir(exist_ok=True)
        
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n📁 Detailed results saved to: {results_path}")
        
        # Show recent errors if any
        recent_errors = error_logger.get_recent_errors(limit=5)
        if recent_errors:
            print(f"\n🔍 Recent Errors (last 5):")
            for error in recent_errors:
                print(f"   - {error['error']['code']}: {error['error']['message']}")
        
        return results
        
    except Exception as e:
        print(f"💥 Test suite crashed: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())