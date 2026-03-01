"""
Comprehensive Test Script for Enhanced 5-Day Program System Components
Tests pattern_subtype mapping, intelligent day spacing logic, region rotation logic,
enhanced movement service integration, and error logging with detailed verification.
"""

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text, and_

from services.error_logger import error_logger
from services.enhanced_program_service import EnhancedProgramService
from services.enhanced_movement_query_service_v2 import EnhancedMovementQueryServiceV2
from models.program import ProgramGenerationRequest, ProgramSkeleton, SessionSkeleton
from models.enums import SessionType, PrimaryRegion, BlockType


@dataclass
class TestResult:
    """Structured test result for detailed reporting."""
    test_name: str
    success: bool
    errors: List[str]
    warnings: List[str]
    details: Dict[str, Any]
    execution_time: float = 0.0
    trace_id: Optional[str] = None


class Enhanced5DayProgramTester:
    """Comprehensive tester for the enhanced 5-day program system components."""
    
    def __init__(self, database_url: str = "postgresql+asyncpg://jacked:jackedpass@localhost:5434/Jacked-DB"):
        """Initialize tester with database connection."""
        self.database_url = database_url
        self.engine = create_async_engine(database_url, echo=False)
        self.async_session = sessionmaker(self.engine, class_=AsyncSession)
        self.test_results: List[TestResult] = []
        
        # Expected 5-day pattern: Monday, Tuesday, Thursday, Friday, Saturday
        self.EXPECTED_5DAY_PATTERN = [1, 2, 4, 5, 6]
        
        # Region rotation expectations for 5-day program
        self.EXPECTED_REGION_ROTATION = {
            1: ["upper"],  # Monday: Upper body
            2: ["lower"],  # Tuesday: Lower body
            4: ["upper"],  # Thursday: Upper body (different from Monday)
            5: ["lower"],  # Friday: Lower body (different from Tuesday)
            6: ["full"]    # Saturday: Full body/core
        }
    
    async def run_comprehensive_5day_test(self) -> Dict[str, Any]:
        """Run comprehensive test suite for the enhanced 5-day program system components."""
        print("🚀 Starting Enhanced 5-Day Program System Component Test Suite")
        print("=" * 70)
        
        test_suite_start = datetime.now(timezone.utc)
        
        suite_results = {
            "test_suite_start_time": test_suite_start.isoformat(),
            "tests_run": [],
            "tests_passed": 0,
            "tests_failed": 0,
            "critical_failures": [],
            "warnings": [],
            "performance_metrics": {},
            "component_status": {}
        }
        
        try:
            async with self.async_session() as session:
                # Test 1: Pattern Subtype Mapping and Database Integration
                test1_start = datetime.now(timezone.utc)
                pattern_result = await self._test_pattern_subtype_mapping(session)
                pattern_result.execution_time = (datetime.now(timezone.utc) - test1_start).total_seconds()
                self.test_results.append(pattern_result)
                suite_results["component_status"]["pattern_subtype"] = pattern_result.success
                
                if pattern_result.success:
                    suite_results["tests_passed"] += 1
                    print(f"✅ Test 1 PASSED ({pattern_result.execution_time:.2f}s)")
                else:
                    suite_results["tests_failed"] += 1
                    suite_results["critical_failures"].extend(pattern_result.errors)
                    print(f"❌ Test 1 FAILED ({pattern_result.execution_time:.2f}s)")
                
                # Test 2: Enhanced Movement Service Integration
                test2_start = datetime.now(timezone.utc)
                movement_result = await self._test_enhanced_movement_integration(session)
                movement_result.execution_time = (datetime.now(timezone.utc) - test2_start).total_seconds()
                self.test_results.append(movement_result)
                suite_results["component_status"]["movement_service"] = movement_result.success
                
                if movement_result.success:
                    suite_results["tests_passed"] += 1
                    print(f"✅ Test 2 PASSED ({movement_result.execution_time:.2f}s)")
                else:
                    suite_results["tests_failed"] += 1
                    suite_results["critical_failures"].extend(movement_result.errors)
                    print(f"❌ Test 2 FAILED ({movement_result.execution_time:.2f}s)")
                
                # Test 3: Intelligent Day Spacing Logic (Unit Test)
                test3_start = datetime.now(timezone.utc)
                spacing_result = await self._test_day_spacing_logic_unit(session)
                spacing_result.execution_time = (datetime.now(timezone.utc) - test3_start).total_seconds()
                self.test_results.append(spacing_result)
                suite_results["component_status"]["day_spacing"] = spacing_result.success
                
                if spacing_result.success:
                    suite_results["tests_passed"] += 1
                    print(f"✅ Test 3 PASSED ({spacing_result.execution_time:.2f}s)")
                else:
                    suite_results["tests_failed"] += 1
                    suite_results["critical_failures"].extend(spacing_result.errors)
                    print(f"❌ Test 3 FAILED ({spacing_result.execution_time:.2f}s)")
                
                # Test 4: Primary Region Rotation Logic (Unit Test)
                test4_start = datetime.now(timezone.utc)
                rotation_result = await self._test_region_rotation_logic_unit(session)
                rotation_result.execution_time = (datetime.now(timezone.utc) - test4_start).total_seconds()
                self.test_results.append(rotation_result)
                suite_results["component_status"]["region_rotation"] = rotation_result.success
                
                if rotation_result.success:
                    suite_results["tests_passed"] += 1
                    print(f"✅ Test 4 PASSED ({rotation_result.execution_time:.2f}s)")
                else:
                    suite_results["tests_failed"] += 1
                    suite_results["critical_failures"].extend(rotation_result.errors)
                    print(f"❌ Test 4 FAILED ({rotation_result.execution_time:.2f}s)")
                
                # Test 5: Configuration and Service Integration
                test5_start = datetime.now(timezone.utc)
                config_result = await self._test_configuration_integration(session)
                config_result.execution_time = (datetime.now(timezone.utc) - test5_start).total_seconds()
                self.test_results.append(config_result)
                suite_results["component_status"]["configuration"] = config_result.success
                
                if config_result.success:
                    suite_results["tests_passed"] += 1
                    print(f"✅ Test 5 PASSED ({config_result.execution_time:.2f}s)")
                else:
                    suite_results["tests_failed"] += 1
                    suite_results["critical_failures"].extend(config_result.errors)
                    print(f"❌ Test 5 FAILED ({config_result.execution_time:.2f}s)")
                
                # Test 6: Error Handling and Logging System
                test6_start = datetime.now(timezone.utc)
                error_result = await self._test_error_logging_system()
                error_result.execution_time = (datetime.now(timezone.utc) - test6_start).total_seconds()
                self.test_results.append(error_result)
                suite_results["component_status"]["error_logging"] = error_result.success
                
                if error_result.success:
                    suite_results["tests_passed"] += 1
                    print(f"✅ Test 6 PASSED ({error_result.execution_time:.2f}s)")
                else:
                    suite_results["tests_failed"] += 1
                    suite_results["critical_failures"].extend(error_result.errors)
                    print(f"❌ Test 6 FAILED ({error_result.execution_time:.2f}s)")
                
        except Exception as e:
            error_trace_id = error_logger.log_error(
                error_code="TEST_SUITE_CRITICAL_FAILURE",
                error_message="Critical test suite failure",
                error_details={"error_type": type(e).__name__, "error_message": str(e)},
                context={"test_phase": "suite_execution"}
            )
            suite_results["critical_failures"].append(f"Test suite crashed: {str(e)}")
            suite_results["error_trace_id"] = error_trace_id
        
        finally:
            suite_end = datetime.now(timezone.utc)
            suite_results["test_suite_end_time"] = suite_end.isoformat()
            suite_results["total_duration_seconds"] = (suite_end - test_suite_start).total_seconds()
            
            # Aggregate warnings
            for test_result in self.test_results:
                suite_results["warnings"].extend(test_result.warnings)
            
            # Performance metrics
            suite_results["performance_metrics"] = {
                "total_tests": len(self.test_results),
                "average_test_duration": sum(tr.execution_time for tr in self.test_results) / len(self.test_results) if self.test_results else 0,
                "slowest_test": max((tr.execution_time, tr.test_name) for tr in self.test_results) if self.test_results else (0, "none"),
                "fastest_test": min((tr.execution_time, tr.test_name) for tr in self.test_results) if self.test_results else (0, "none")
            }
        
        return suite_results
    
    async def _test_pattern_subtype_mapping(self, session: AsyncSession) -> TestResult:
        """Test pattern_subtype mapping and database integration."""
        print("\n📊 Test 1: Pattern Subtype Mapping and Database Integration")
        print("-" * 60)
        
        result = TestResult(
            test_name="Pattern Subtype Mapping",
            success=False,
            errors=[],
            warnings=[],
            details={}
        )
        
        try:
            # Verify pattern_subtype column exists and has data
            column_check = await session.execute(text("""
                SELECT COUNT(*) as total_count,
                       COUNT(pattern_subtype) as filled_count,
                       COUNT(DISTINCT pattern_subtype) as unique_subtypes
                FROM movements 
                WHERE pattern_subtype IS NOT NULL
            """))
            
            column_data = column_check.fetchone()
            result.details["database_stats"] = {
                "total_movements": column_data[0],
                "movements_with_subtype": column_data[1],
                "unique_subtypes": column_data[2],
                "coverage_percentage": (column_data[1] / column_data[0] * 100) if column_data[0] > 0 else 0
            }
            
            print(f"📈 Database Coverage: {result.details['database_stats']['coverage_percentage']:.1f}%")
            print(f"📈 Unique Subtypes: {result.details['database_stats']['unique_subtypes']}")
            
            # Get detailed subtype distribution
            subtype_query = await session.execute(text("""
                SELECT pattern_subtype, COUNT(*) as count
                FROM movements 
                WHERE pattern_subtype IS NOT NULL
                GROUP BY pattern_subtype
                ORDER BY count DESC
                LIMIT 20
            """))
            
            subtype_distribution = {}
            for row in subtype_query.fetchall():
                subtype, count = row
                subtype_distribution[subtype] = count
            
            result.details["subtype_distribution"] = subtype_distribution
            
            # Verify expected subtypes are present
            expected_subtypes = {
                "squat", "hinge", "horizontal_push", "horizontal_pull",
                "vertical_push", "vertical_pull", "lunge", "rotation",
                "carry", "jump", "run", "row", "bike", "mobility"
            }
            
            found_subtypes = set(subtype_distribution.keys())
            missing_subtypes = expected_subtypes - found_subtypes
            
            if missing_subtypes:
                result.warnings.append(f"Missing expected subtypes: {missing_subtypes}")
                print(f"⚠️  Missing subtypes: {missing_subtypes}")
            
            # Test subtype-region mapping consistency
            region_mapping_query = await session.execute(text("""
                SELECT pattern_subtype, primary_region, COUNT(*) as count
                FROM movements 
                WHERE pattern_subtype IS NOT NULL
                GROUP BY pattern_subtype, primary_region
                ORDER BY pattern_subtype, count DESC
            """))
            
            region_mappings = {}
            for row in region_mapping_query.fetchall():
                subtype, region, count = row
                if subtype not in region_mappings:
                    region_mappings[subtype] = {}
                region_mappings[subtype][region] = count
            
            result.details["region_mappings"] = region_mappings
            
            # Validate logical mappings
            inconsistent_mappings = []
            for subtype, regions in region_mappings.items():
                if subtype in ["squat", "lunge"] and "lower body" not in regions:
                    inconsistent_mappings.append(f"{subtype} missing lower body mapping")
                elif subtype in ["horizontal_push", "vertical_push"] and "upper body" not in regions:
                    inconsistent_mappings.append(f"{subtype} missing upper body mapping")
                elif subtype in ["horizontal_pull", "vertical_pull"] and "upper body" not in regions:
                    inconsistent_mappings.append(f"{subtype} missing upper body mapping")
            
            if inconsistent_mappings:
                result.warnings.extend(inconsistent_mappings)
                print(f"⚠️  Inconsistent mappings: {inconsistent_mappings}")
            
            result.success = len(result.errors) == 0 and result.details["database_stats"]["coverage_percentage"] > 30
            
            if result.success:
                print("✅ Pattern subtype mapping verification passed")
            else:
                print("❌ Pattern subtype mapping verification failed")
                
        except Exception as e:
            error_trace_id = error_logger.log_error(
                error_code="PATTERN_SUBTYPE_TEST_FAILED",
                error_message="Pattern subtype mapping test failed",
                error_details={"error_type": type(e).__name__, "error_message": str(e)},
                context={"test_phase": "pattern_subtype_verification"}
            )
            result.errors.append(f"Pattern subtype test failed: {str(e)}")
            result.trace_id = error_trace_id
        
        return result
    
    async def _test_enhanced_movement_integration(self, session: AsyncSession) -> TestResult:
        """Test enhanced movement service integration with pattern_subtype."""
        print("\n🏋️ Test 2: Enhanced Movement Service Integration")
        print("-" * 60)
        
        result = TestResult(
            test_name="Enhanced Movement Service Integration",
            success=False,
            errors=[],
            warnings=[],
            details={}
        )
        
        try:
            movement_service = EnhancedMovementQueryServiceV2(session)
            
            # Test different session types with pattern_subtype filtering
            test_scenarios = [
                {
                    "name": "5-Day Resistance Program - Upper Focus",
                    "session_type": "resistance_accessory",
                    "equipment": ["barbell", "dumbbell"],
                    "target_regions": ["anterior upper", "posterior upper"],
                    "expected_subtypes": ["horizontal_push", "horizontal_pull", "vertical_push", "vertical_pull"]
                },
                {
                    "name": "5-Day Resistance Program - Lower Focus", 
                    "session_type": "resistance_accessory",
                    "equipment": ["barbell", "dumbbell"],
                    "target_regions": ["anterior lower", "posterior lower"],
                    "expected_subtypes": ["squat", "hinge", "lunge"]
                },
                {
                    "name": "5-Day Mobility Focus",
                    "session_type": "mobility_only",
                    "equipment": ["bodyweight", "band"],
                    "target_regions": ["full body"],
                    "expected_subtypes": ["mobility", "stretch", "activation"]
                }
            ]
            
            for scenario in test_scenarios:
                print(f"🧪 Testing: {scenario['name']}")
                
                try:
                    movements = await movement_service.get_balanced_movement_set(
                        session_type=scenario["session_type"],
                        equipment_available=scenario["equipment"],
                        target_regions=scenario["target_regions"],
                        max_movements=8,
                        include_variations=True
                    )
                    
                    # Verify movement characteristics
                    movement_analysis = {
                        "total_movements": len(movements),
                        "subtype_coverage": {},
                        "equipment_coverage": {},
                        "region_coverage": {},
                        "sample_movements": []
                    }
                    
                    # Analyze subtype coverage
                    for movement in movements:
                        subtype = movement.get("pattern_subtype", "unknown")
                        equipment = movement.get("equipment_category", "unknown")
                        region = movement.get("primary_region", "unknown")
                        name = movement.get("name", "unknown")
                        
                        movement_analysis["subtype_coverage"][subtype] = movement_analysis["subtype_coverage"].get(subtype, 0) + 1
                        movement_analysis["equipment_coverage"][equipment] = movement_analysis["equipment_coverage"].get(equipment, 0) + 1
                        movement_analysis["region_coverage"][region] = movement_analysis["region_coverage"].get(region, 0) + 1
                        
                        if len(movement_analysis["sample_movements"]) < 3:
                            movement_analysis["sample_movements"].append({
                                "name": name,
                                "subtype": subtype,
                                "equipment": equipment,
                                "region": region
                            })
                    
                    # Check expected subtype coverage
                    found_subtypes = set(movement_analysis["subtype_coverage"].keys())
                    expected_coverage = set(scenario["expected_subtypes"])
                    coverage_percentage = len(found_subtypes.intersection(expected_coverage)) / len(expected_coverage) * 100 if expected_coverage else 0
                    
                    movement_analysis["expected_coverage_percentage"] = coverage_percentage
                    movement_analysis["missing_expected_subtypes"] = list(expected_coverage - found_subtypes)
                    movement_analysis["unexpected_subtypes"] = list(found_subtypes - expected_coverage)
                    
                    result.details[scenario["name"]] = movement_analysis
                    
                    print(f"   ✅ Found {len(movements)} movements")
                    print(f"   📊 Subtype coverage: {coverage_percentage:.1f}%")
                    
                    if coverage_percentage < 50:
                        result.warnings.append(f"{scenario['name']}: Low subtype coverage ({coverage_percentage:.1f}%)")
                    
                    # Print sample movements
                    for sample in movement_analysis["sample_movements"]:
                        print(f"   🏃 {sample['name']} ({sample['subtype']}, {sample['equipment']}, {sample['region']})")
                    
                except Exception as e:
                    error_trace_id = error_logger.log_error(
                        error_code="MOVEMENT_SERVICE_INTEGRATION_FAILED",
                        error_message=f"Movement service integration failed for {scenario['name']}",
                        error_details={"scenario": scenario["name"], "error": str(e)},
                        context={"test_phase": "movement_service_integration"}
                    )
                    result.errors.append(f"{scenario['name']} failed: {str(e)}")
            
            result.success = len(result.errors) == 0
            
            if result.success:
                print("✅ Enhanced movement service integration passed")
            else:
                print("❌ Enhanced movement service integration failed")
                
        except Exception as e:
            error_trace_id = error_logger.log_error(
                error_code="MOVEMENT_SERVICE_INIT_FAILED",
                error_message="Failed to initialize movement service",
                error_details={"error_type": type(e).__name__, "error_message": str(e)},
                context={"test_phase": "movement_service_initialization"}
            )
            result.errors.append(f"Movement service initialization failed: {str(e)}")
            result.trace_id = error_trace_id
        
        return result
    
    async def _test_day_spacing_logic_unit(self, session: AsyncSession) -> TestResult:
        """Test the intelligent day spacing logic as a unit test."""
        print("\n📅 Test 3: Intelligent Day Spacing Logic (Unit Test)")
        print("-" * 60)
        
        result = TestResult(
            test_name="Day Spacing Logic Unit Test",
            success=False,
            errors=[],
            warnings=[],
            details={}
        )
        
        try:
            program_service = EnhancedProgramService(db_session=session)
            
            # Test the day spacing logic directly
            test_cases = [
                {"days_per_week": 1, "program_length_weeks": 4, "expected_min_days": 1},
                {"days_per_week": 3, "program_length_weeks": 8, "expected_min_days": 3},
                {"days_per_week": 5, "program_length_weeks": 12, "expected_min_days": 5},
                {"days_per_week": 6, "program_length_weeks": 6, "expected_min_days": 6}
            ]
            
            spacing_tests = {}
            
            for test_case in test_cases:
                days_per_week = test_case["days_per_week"]
                program_length_weeks = test_case["program_length_weeks"]
                
                print(f"🧪 Testing {days_per_week} days per week for {program_length_weeks} weeks...")
                
                # Test the intelligent spacing method directly
                training_days = program_service._get_intelligent_training_days(days_per_week, program_length_weeks)
                
                spacing_analysis = {
                    "training_days": training_days,
                    "day_count": len(training_days),
                    "consecutive_analysis": self._analyze_consecutive_days(training_days),
                    "rest_day_analysis": self._analyze_rest_days(training_days),
                    "spacing_quality": "unknown"
                }
                
                # Validate the spacing
                validation_results = self._validate_day_spacing(training_days, days_per_week)
                spacing_analysis["validation"] = validation_results
                
                if validation_results["valid"]:
                    spacing_analysis["spacing_quality"] = "optimal" if training_days == self.EXPECTED_5DAY_PATTERN and days_per_week == 5 else "acceptable"
                    print(f"   ✅ Valid spacing: {training_days}")
                else:
                    spacing_analysis["spacing_quality"] = "suboptimal"
                    print(f"   ⚠️  Suboptimal spacing: {training_days}")
                    if validation_results["issues"]:
                        print(f"   📋 Issues: {validation_results['issues']}")
                
                spacing_tests[f"{days_per_week}_days"] = spacing_analysis
            
            result.details["spacing_tests"] = spacing_tests
            
            # Overall validation
            total_tests = len(spacing_tests)
            valid_tests = sum(1 for test in spacing_tests.values() if test["validation"]["valid"])
            
            result.details["overall_validation"] = {
                "total_tests": total_tests,
                "valid_tests": valid_tests,
                "success_rate": (valid_tests / total_tests * 100) if total_tests > 0 else 0
            }
            
            result.success = valid_tests == total_tests and total_tests > 0
            
            if result.success:
                print("✅ Day spacing logic unit test passed")
            else:
                print("❌ Day spacing logic unit test failed")
                
        except Exception as e:
            error_trace_id = error_logger.log_error(
                error_code="DAY_SPACING_UNIT_TEST_FAILED",
                error_message="Day spacing logic unit test failed",
                error_details={"error_type": type(e).__name__, "error_message": str(e)},
                context={"test_phase": "day_spacing_unit_test"}
            )
            result.errors.append(f"Day spacing unit test failed: {str(e)}")
            result.trace_id = error_trace_id
        
        return result
    
    async def _test_region_rotation_logic_unit(self, session: AsyncSession) -> TestResult:
        """Test primary region rotation logic as unit test."""
        print("\n🔄 Test 4: Primary Region Rotation Logic (Unit Test)")
        print("-" * 60)
        
        result = TestResult(
            test_name="Region Rotation Logic Unit Test",
            success=False,
            errors=[],
            warnings=[],
            details={}
        )
        
        try:
            program_service = EnhancedProgramService(db_session=session)
            
            # Test region rotation logic directly
            test_scenarios = [
                {
                    "name": "Monday Upper Body",
                    "session_type": SessionType.RESISTANCE_ACCESSORY,
                    "day_number": 1,
                    "week_number": 1,
                    "previous_regions": [],
                    "expected_region_type": "upper"
                },
                {
                    "name": "Tuesday Lower Body", 
                    "session_type": SessionType.RESISTANCE_ACCESSORY,
                    "day_number": 2,
                    "week_number": 1,
                    "previous_regions": [PrimaryRegion.ANTERIOR_UPPER],
                    "expected_region_type": "lower"
                },
                {
                    "name": "Thursday Upper Body (Different)",
                    "session_type": SessionType.RESISTANCE_ACCESSORY,
                    "day_number": 4,
                    "week_number": 1,
                    "previous_regions": [PrimaryRegion.ANTERIOR_UPPER, PrimaryRegion.ANTERIOR_LOWER],
                    "expected_region_type": "upper"
                },
                {
                    "name": "Saturday Full Body",
                    "session_type": SessionType.RESISTANCE_ACCESSORY,
                    "day_number": 6,
                    "week_number": 1,
                    "previous_regions": [PrimaryRegion.ANTERIOR_UPPER, PrimaryRegion.ANTERIOR_LOWER, PrimaryRegion.POSTERIOR_UPPER],
                    "expected_region_type": "full"
                }
            ]
            
            rotation_tests = {}
            
            for scenario in test_scenarios:
                print(f"🧪 Testing: {scenario['name']}")
                
                # Test region selection logic
                selected_regions = program_service._select_primary_region_with_rotation(
                    session_type=scenario["session_type"],
                    day_number=scenario["day_number"],
                    previous_regions=scenario["previous_regions"],
                    week_number=scenario["week_number"]
                )
                
                rotation_analysis = {
                    "selected_regions": [str(region) for region in selected_regions],
                    "previous_regions": [str(region) for region in scenario["previous_regions"]],
                    "rotation_valid": True,
                    "issues": []
                }
                
                # Validate rotation
                if scenario["previous_regions"] and selected_regions:
                    last_region = scenario["previous_regions"][-1]
                    current_region = selected_regions[0]
                    
                    # Check for consecutive same major regions
                    if self._are_same_major_region(last_region, current_region):
                        rotation_analysis["rotation_valid"] = False
                        rotation_analysis["issues"].append(f"Consecutive same major region: {last_region} -> {current_region}")
                
                # Check expected region type
                actual_region_type = self._get_major_region_type(selected_regions[0]) if selected_regions else "unknown"
                if actual_region_type != scenario["expected_region_type"]:
                    rotation_analysis["rotation_valid"] = False
                    rotation_analysis["issues"].append(f"Expected {scenario['expected_region_type']}, got {actual_region_type}")
                
                if rotation_analysis["rotation_valid"]:
                    print(f"   ✅ Valid rotation: {rotation_analysis['selected_regions']}")
                else:
                    print(f"   ⚠️  Rotation issues: {rotation_analysis['issues']}")
                
                rotation_tests[scenario["name"]] = rotation_analysis
            
            result.details["rotation_tests"] = rotation_tests
            
            # Overall validation
            total_tests = len(rotation_tests)
            valid_tests = sum(1 for test in rotation_tests.values() if test["rotation_valid"])
            
            result.details["overall_validation"] = {
                "total_tests": total_tests,
                "valid_tests": valid_tests,
                "success_rate": (valid_tests / total_tests * 100) if total_tests > 0 else 0
            }
            
            result.success = valid_tests == total_tests and total_tests > 0
            
            if result.success:
                print("✅ Region rotation logic unit test passed")
            else:
                print("❌ Region rotation logic unit test failed")
                
        except Exception as e:
            error_trace_id = error_logger.log_error(
                error_code="REGION_ROTATION_UNIT_TEST_FAILED",
                error_message="Region rotation logic unit test failed",
                error_details={"error_type": type(e).__name__, "error_message": str(e)},
                context={"test_phase": "region_rotation_unit_test"}
            )
            result.errors.append(f"Region rotation unit test failed: {str(e)}")
            result.trace_id = error_trace_id
        
        return result
    
    async def _test_configuration_integration(self, session: AsyncSession) -> TestResult:
        """Test configuration and service integration."""
        print("\n⚙️ Test 5: Configuration and Service Integration")
        print("-" * 60)
        
        result = TestResult(
            test_name="Configuration Integration",
            success=False,
            errors=[],
            warnings=[],
            details={}
        )
        
        try:
            # Test service initialization
            program_service = EnhancedProgramService(db_session=session)
            
            config_test = {
                "service_initialization": True,
                "config_loading": False,
                "movement_service_integration": False,
                "day_patterns_available": False,
                "region_mappings_available": False
            }
            
            # Test configuration loading
            try:
                if hasattr(program_service, 'config') and program_service.config:
                    config_test["config_loading"] = True
                    print("✅ Configuration loaded successfully")
                else:
                    print("⚠️  Configuration not loaded or empty")
            except Exception as e:
                print(f"❌ Configuration loading failed: {e}")
            
            # Test movement service integration
            try:
                if hasattr(program_service, 'movement_query_service') or program_service.db_session:
                    config_test["movement_service_integration"] = True
                    print("✅ Movement service integration available")
                else:
                    print("⚠️  Movement service integration not available")
            except Exception as e:
                print(f"❌ Movement service integration failed: {e}")
            
            # Test day spacing patterns
            try:
                if hasattr(program_service, 'DAY_SPACING_PATTERNS') and program_service.DAY_SPACING_PATTERNS:
                    config_test["day_patterns_available"] = True
                    print(f"✅ Day spacing patterns available: {len(program_service.DAY_SPACING_PATTERNS)} patterns")
                else:
                    print("⚠️  Day spacing patterns not available")
            except Exception as e:
                print(f"❌ Day spacing patterns test failed: {e}")
            
            # Test region rotation mappings
            try:
                if hasattr(program_service, 'REGION_ROTATION') and program_service.REGION_ROTATION:
                    config_test["region_mappings_available"] = True
                    print(f"✅ Region rotation mappings available: {len(program_service.REGION_ROTATION)} categories")
                else:
                    print("⚠️  Region rotation mappings not available")
            except Exception as e:
                print(f"❌ Region rotation mappings test failed: {e}")
            
            result.details["configuration_tests"] = config_test
            
            # Calculate success rate
            total_checks = len(config_test)
            successful_checks = sum(1 for check in config_test.values() if check)
            success_rate = (successful_checks / total_checks * 100) if total_checks > 0 else 0
            
            result.details["success_rate"] = success_rate
            result.success = success_rate >= 60  # At least 60% of components working
            
            if result.success:
                print(f"✅ Configuration integration passed ({success_rate:.1f}% success rate)")
            else:
                print(f"❌ Configuration integration failed ({success_rate:.1f}% success rate)")
                
        except Exception as e:
            error_trace_id = error_logger.log_error(
                error_code="CONFIGURATION_INTEGRATION_TEST_FAILED",
                error_message="Configuration integration test failed",
                error_details={"error_type": type(e).__name__, "error_message": str(e)},
                context={"test_phase": "configuration_integration"}
            )
            result.errors.append(f"Configuration integration test failed: {str(e)}")
            result.trace_id = error_trace_id
        
        return result
    
    async def _test_error_logging_system(self) -> TestResult:
        """Test error handling and logging system."""
        print("\n🚨 Test 6: Error Handling and Logging System")
        print("-" * 60)
        
        result = TestResult(
            test_name="Error Logging System",
            success=False,
            errors=[],
            warnings=[],
            details={}
        )
        
        try:
            # Test error logging capabilities
            test_errors = [
                {
                    "code": "TEST_ERROR_001",
                    "message": "Test error for logging validation",
                    "details": {"test": "data", "timestamp": datetime.now(timezone.utc).isoformat()},
                    "context": {"test_phase": "error_handling_test"}
                },
                {
                    "code": "DATABASE_CONNECTION_TEST",
                    "message": "Simulated database connection issue",
                    "details": {"connection_string": "test", "timeout": 30},
                    "context": {"test_phase": "database_simulation"}
                }
            ]
            
            logged_errors = []
            for test_error in test_errors:
                trace_id = error_logger.log_error(
                    error_code=test_error["code"],
                    error_message=test_error["message"],
                    error_details=test_error["details"],
                    context=test_error["context"]
                )
                logged_errors.append({
                    "trace_id": trace_id,
                    "error_code": test_error["code"]
                })
            
            result.details["logged_errors"] = logged_errors
            
            # Verify error retrieval
            recent_errors = error_logger.get_recent_errors(limit=10)
            result.details["retrieved_errors"] = len(recent_errors)
            
            print(f"✅ Logged {len(logged_errors)} test errors")
            print(f"✅ Retrieved {len(recent_errors)} recent errors")
            
            # Test error traceability (if method exists)
            traceability_test = "not_available"
            if logged_errors:
                sample_trace_id = logged_errors[0]["trace_id"]
                try:
                    # Try different possible method names
                    if hasattr(error_logger, 'get_error_by_trace_id'):
                        traced_error = error_logger.get_error_by_trace_id(sample_trace_id)
                        traceability_test = "passed" if traced_error else "failed"
                    elif hasattr(error_logger, 'get_error'):
                        traced_error = error_logger.get_error(sample_trace_id)
                        traceability_test = "passed" if traced_error else "failed"
                    else:
                        traceability_test = "method_not_found"
                except Exception as e:
                    traceability_test = f"error: {str(e)}"
            
            result.details["traceability_test"] = traceability_test
            
            if traceability_test == "passed":
                print("✅ Error traceability working correctly")
            elif traceability_test == "not_available":
                print("⚠️  Error traceability method not available")
                result.warnings.append("Error traceability method not found")
            else:
                print(f"⚠️  Error traceability test: {traceability_test}")
                result.warnings.append(f"Error traceability issue: {traceability_test}")
            
            result.success = len(logged_errors) > 0 and len(recent_errors) > 0
            
            if result.success:
                print("✅ Error handling and logging system passed")
            else:
                print("❌ Error handling and logging system failed")
                
        except Exception as e:
            error_trace_id = error_logger.log_error(
                error_code="ERROR_LOGGING_TEST_FAILED",
                error_message="Error logging system test failed",
                error_details={"error_type": type(e).__name__, "error_message": str(e)},
                context={"test_phase": "error_logging_system"}
            )
            result.errors.append(f"Error logging test failed: {str(e)}")
            result.trace_id = error_trace_id
        
        return result
    
    # Helper methods for analysis
    def _analyze_consecutive_days(self, training_days: List[int]) -> Dict[str, Any]:
        """Analyze consecutive training days."""
        if not training_days:
            return {"max_consecutive": 0, "consecutive_sequences": []}
        
        consecutive_sequences = []
        current_sequence = [training_days[0]]
        max_consecutive = 1
        
        for i in range(1, len(training_days)):
            if training_days[i] == training_days[i-1] + 1:
                current_sequence.append(training_days[i])
            else:
                if len(current_sequence) > 1:
                    consecutive_sequences.append(current_sequence.copy())
                current_sequence = [training_days[i]]
            max_consecutive = max(max_consecutive, len(current_sequence))
        
        if len(current_sequence) > 1:
            consecutive_sequences.append(current_sequence)
        
        return {
            "max_consecutive": max_consecutive,
            "consecutive_sequences": consecutive_sequences
        }
    
    def _analyze_rest_days(self, training_days: List[int]) -> Dict[str, Any]:
        """Analyze rest day distribution."""
        all_days = set(range(1, 8))  # Days 1-7
        rest_days = sorted(list(all_days - set(training_days)))
        
        return {
            "rest_days": rest_days,
            "rest_day_count": len(rest_days),
            "has_weekend_rest": 6 in rest_days or 7 in rest_days,
            "has_midweek_rest": 4 in rest_days
        }
    
    def _validate_day_spacing(self, training_days: List[int], expected_days_per_week: int) -> Dict[str, Any]:
        """Validate day spacing against requirements."""
        validation = {
            "valid": True,
            "issues": []
        }
        
        # Check day count
        if len(training_days) != expected_days_per_week:
            validation["valid"] = False
            validation["issues"].append(f"Expected {expected_days_per_week} days, got {len(training_days)}")
        
        # Check for too many consecutive days
        consecutive_analysis = self._analyze_consecutive_days(training_days)
        if consecutive_analysis["max_consecutive"] > 2:
            validation["valid"] = False
            validation["issues"].append(f"Too many consecutive days: {consecutive_analysis['max_consecutive']}")
        
        # Check for optimal 5-day pattern
        if expected_days_per_week == 5 and training_days != self.EXPECTED_5DAY_PATTERN:
            validation["issues"].append(f"Not optimal 5-day pattern: {training_days} (expected {self.EXPECTED_5DAY_PATTERN})")
        
        return validation
    
    def _are_same_major_region(self, region1: PrimaryRegion, region2: PrimaryRegion) -> bool:
        """Check if two regions are in the same major category."""
        region1_str = str(region1).lower()
        region2_str = str(region2).lower()
        
        # Define major region categories
        upper_regions = ["anterior_upper", "posterior_upper", "shoulder"]
        lower_regions = ["anterior_lower", "posterior_lower"]
        full_regions = ["full_body", "core"]
        
        # Check if both are in the same category
        for category in [upper_regions, lower_regions, full_regions]:
            if any(r in region1_str for r in category) and any(r in region2_str for r in category):
                return True
        
        return False
    
    def _get_major_region_type(self, region: PrimaryRegion) -> str:
        """Get the major region type for a given region."""
        region_str = str(region).lower()
        
        if "upper" in region_str:
            return "upper"
        elif "lower" in region_str:
            return "lower"
        elif "full" in region_str:
            return "full"
        elif "core" in region_str:
            return "full"
        else:
            return "unknown"


async def main():
    """Main test execution for enhanced 5-day program system components."""
    print("🚀 Enhanced 5-Day Program System Component Test Suite")
    print("=" * 70)
    print("Testing comprehensive 5-day program components:")
    print("• Pattern subtype mapping and database integration")
    print("• Enhanced movement service with pattern_subtype filtering")
    print("• Intelligent day spacing logic [1,2,4,5,6]")
    print("• Primary region rotation to avoid consecutive same regions")
    print("• Configuration and service integration")
    print("• Comprehensive error logging and validation")
    print("=" * 70)
    
    tester = Enhanced5DayProgramTester()
    
    try:
        # Run comprehensive test suite
        results = await tester.run_comprehensive_5day_test()
        
        # Print detailed results summary
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE COMPONENT TEST RESULTS SUMMARY")
        print("=" * 70)
        
        print(f"✅ Tests Passed: {results['tests_passed']}")
        print(f"❌ Tests Failed: {results['tests_failed']}")
        print(f"⏱️  Total Duration: {results['total_duration_seconds']:.2f} seconds")
        
        # Component status summary
        print(f"\n🔧 Component Status:")
        for component, status in results.get('component_status', {}).items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {component.replace('_', ' ').title()}")
        
        if results['critical_failures']:
            print(f"\n🚨 Critical Failures:")
            for failure in results['critical_failures']:
                print(f"   - {failure}")
        
        if results['warnings']:
            print(f"\n⚠️  Warnings:")
            for warning in results['warnings'][:5]:  # Show first 5 warnings
                print(f"   - {warning}")
            if len(results['warnings']) > 5:
                print(f"   ... and {len(results['warnings']) - 5} more warnings")
        
        # Performance metrics
        perf = results['performance_metrics']
        print(f"\n📈 Performance Metrics:")
        print(f"   Average test duration: {perf['average_test_duration']:.2f}s")
        print(f"   Slowest test: {perf['slowest_test'][1]} ({perf['slowest_test'][0]:.2f}s)")
        print(f"   Fastest test: {perf['fastest_test'][1]} ({perf['fastest_test'][0]:.2f}s)")
        
        # Save detailed results
        results_dir = Path(__file__).parent / "test_results"
        results_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = results_dir / f"5day_enhanced_components_test_{timestamp}.json"
        
        # Convert test results to serializable format
        serializable_results = {
            **results,
            "detailed_test_results": [
                {
                    "test_name": tr.test_name,
                    "success": tr.success,
                    "errors": tr.errors,
                    "warnings": tr.warnings,
                    "details": tr.details,
                    "execution_time": tr.execution_time,
                    "trace_id": tr.trace_id
                }
                for tr in tester.test_results
            ]
        }
        
        with open(results_file, 'w') as f:
            json.dump(serializable_results, f, indent=2, default=str)
        
        print(f"\n📁 Detailed results saved to: {results_file}")
        
        # Show recent system errors if any
        recent_system_errors = error_logger.get_recent_errors(limit=3)
        if recent_system_errors:
            print(f"\n🔍 Recent System Errors:")
            for error in recent_system_errors:
                print(f"   - {error['error']['code']}: {error['error']['message']}")
        
        # Return success status based on critical components
        critical_components = ['pattern_subtype', 'movement_service', 'day_spacing', 'region_rotation']
        critical_success = all(results.get('component_status', {}).get(comp, False) for comp in critical_components)
        
        return critical_success and results['tests_failed'] == 0
        
    except Exception as e:
        print(f"💥 Test suite crashed: {str(e)}")
        # Log the crash
        error_logger.log_error(
            error_code="TEST_SUITE_CRASH",
            error_message="5-day enhanced system component test suite crashed",
            error_details={"error_type": type(e).__name__, "error_message": str(e)},
            context={"test_phase": "suite_execution"}
        )
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)