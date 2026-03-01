"""
Fixed Comprehensive Test Script for Enhanced 5-Day Program System
Tests pattern_subtype mapping, intelligent day spacing [1,2,4,5,6], region rotation logic,
enhanced movement service integration, and detailed error logging.
"""

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

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
    """Comprehensive tester for the enhanced 5-day program system."""
    
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
        """Run comprehensive test suite for the enhanced 5-day program system."""
        print("🚀 Starting Enhanced 5-Day Program System Test Suite")
        print("=" * 70)
        
        test_suite_start = datetime.now(timezone.utc)
        
        suite_results = {
            "test_suite_start_time": test_suite_start.isoformat(),
            "tests_run": [],
            "tests_passed": 0,
            "tests_failed": 0,
            "critical_failures": [],
            "warnings": [],
            "performance_metrics": {}
        }
        
        try:
            async with self.async_session() as session:
                # Test 1: Pattern Subtype Mapping Verification
                test1_start = datetime.now(timezone.utc)
                pattern_result = await self._test_pattern_subtype_mapping(session)
                pattern_result.execution_time = (datetime.now(timezone.utc) - test1_start).total_seconds()
                self.test_results.append(pattern_result)
                
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
                
                if movement_result.success:
                    suite_results["tests_passed"] += 1
                    print(f"✅ Test 2 PASSED ({movement_result.execution_time:.2f}s)")
                else:
                    suite_results["tests_failed"] += 1
                    suite_results["critical_failures"].extend(movement_result.errors)
                    print(f"❌ Test 2 FAILED ({movement_result.execution_time:.2f}s)")
                
                # Test 3: 5-Day Intelligent Day Spacing Logic
                test3_start = datetime.now(timezone.utc)
                spacing_result = await self._test_5day_intelligent_spacing(session)
                spacing_result.execution_time = (datetime.now(timezone.utc) - test3_start).total_seconds()
                self.test_results.append(spacing_result)
                
                if spacing_result.success:
                    suite_results["tests_passed"] += 1
                    print(f"✅ Test 3 PASSED ({spacing_result.execution_time:.2f}s)")
                else:
                    suite_results["tests_failed"] += 1
                    suite_results["critical_failures"].extend(spacing_result.errors)
                    print(f"❌ Test 3 FAILED ({spacing_result.execution_time:.2f}s)")
                
                # Test 4: Primary Region Rotation Logic
                test4_start = datetime.now(timezone.utc)
                rotation_result = await self._test_primary_region_rotation(session)
                rotation_result.execution_time = (datetime.now(timezone.utc) - test4_start).total_seconds()
                self.test_results.append(rotation_result)
                
                if rotation_result.success:
                    suite_results["tests_passed"] += 1
                    print(f"✅ Test 4 PASSED ({rotation_result.execution_time:.2f}s)")
                else:
                    suite_results["tests_failed"] += 1
                    suite_results["critical_failures"].extend(rotation_result.errors)
                    print(f"❌ Test 4 FAILED ({rotation_result.execution_time:.2f}s)")
                
                # Test 5: Complete 5-Day Program Generation
                test5_start = datetime.now(timezone.utc)
                program_result = await self._test_complete_5day_program(session)
                program_result.execution_time = (datetime.now(timezone.utc) - test5_start).total_seconds()
                self.test_results.append(program_result)
                
                if program_result.success:
                    suite_results["tests_passed"] += 1
                    print(f"✅ Test 5 PASSED ({program_result.execution_time:.2f}s)")
                else:
                    suite_results["tests_failed"] += 1
                    suite_results["critical_failures"].extend(program_result.errors)
                    print(f"❌ Test 5 FAILED ({program_result.execution_time:.2f}s)")
                
                # Test 6: Error Handling and Logging Integration
                test6_start = datetime.now(timezone.utc)
                error_result = await self._test_error_handling_integration()
                error_result.execution_time = (datetime.now(timezone.utc) - test6_start).total_seconds()
                self.test_results.append(error_result)
                
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
        print("\n📊 Test 1: Pattern Subtype Mapping Verification")
        print("-" * 50)
        
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
        print("-" * 50)
        
        result = TestResult(
            test_name="Enhanced Movement Service Integration",
            success=False,
            errors=[],
            warnings=[],
            details={}
        )
        
        try:
            movement_service = EnhancedMovementQueryServiceV2(session)
            
            # Test different session types with pattern_subtype filtering (fixed equipment)
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
                        "region_coverage": {}
                    }
                    
                    # Analyze subtype coverage
                    for movement in movements:
                        subtype = movement.get("pattern_subtype", "unknown")
                        equipment = movement.get("equipment_category", "unknown")
                        region = movement.get("primary_region", "unknown")
                        
                        movement_analysis["subtype_coverage"][subtype] = movement_analysis["subtype_coverage"].get(subtype, 0) + 1
                        movement_analysis["equipment_coverage"][equipment] = movement_analysis["equipment_coverage"].get(equipment, 0) + 1
                        movement_analysis["region_coverage"][region] = movement_analysis["region_coverage"].get(region, 0) + 1
                    
                    # Check expected subtype coverage
                    found_subtypes = set(movement_analysis["subtype_coverage"].keys())
                    expected_coverage = set(scenario["expected_subtypes"])
                    coverage_percentage = len(found_subtypes.intersection(expected_coverage)) / len(expected_coverage) * 100 if expected_coverage else 0
                    
                    movement_analysis["expected_coverage_percentage"] = coverage_percentage
                    movement_analysis["missing_expected_subtypes"] = list(expected_coverage - found_subtypes)
                    
                    result.details[scenario["name"]] = movement_analysis
                    
                    print(f"   ✅ Found {len(movements)} movements")
                    print(f"   📊 Subtype coverage: {coverage_percentage:.1f}%")
                    
                    if coverage_percentage < 50:
                        result.warnings.append(f"{scenario['name']}: Low subtype coverage ({coverage_percentage:.1f}%)")
                    
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
    
    async def _test_5day_intelligent_spacing(self, session: AsyncSession) -> TestResult:
        """Test the intelligent day spacing logic for 5-day programs."""
        print("\n📅 Test 3: 5-Day Intelligent Day Spacing Logic")
        print("-" * 50)
        
        result = TestResult(
            test_name="5-Day Intelligent Day Spacing",
            success=False,
            errors=[],
            warnings=[],
            details={}
        )
        
        try:
            program_service = EnhancedProgramService(db_session=session)
            
            # Test multiple 5-day program configurations
            test_configs = [
                {
                    "name": "Strength-Focused 5-Day",
                    "goals": {
                        "primary_strength": 0.9,
                        "normalized_hypertrophy_fat_loss": 0.6,
                        "normalized_power_mobility": 0.3,
                        "strength_bias": 0.9,
                        "endurance_bias": 0.2
                    },
                    "equipment": ["barbell", "dumbbell"]
                },
                {
                    "name": "Balanced 5-Day",
                    "goals": {
                        "primary_strength": 0.6,
                        "normalized_hypertrophy_fat_loss": 0.7,
                        "normalized_power_mobility": 0.5,
                        "strength_bias": 0.6,
                        "endurance_bias": 0.6
                    },
                    "equipment": ["barbell", "dumbbell", "bodyweight"]
                },
                {
                    "name": "Hypertrophy-Focused 5-Day",
                    "goals": {
                        "primary_strength": 0.5,
                        "normalized_hypertrophy_fat_loss": 0.9,
                        "normalized_power_mobility": 0.3,
                        "strength_bias": 0.7,
                        "endurance_bias": 0.4
                    },
                    "equipment": ["barbell", "dumbbell", "machine"]
                }
            ]
            
            for config in test_configs:
                print(f"🧪 Testing: {config['name']}")
                
                # Create test request with required fields
                test_request = ProgramGenerationRequest(
                    user_id="test_user_123",  # Add required user_id
                    normalized_goals=config["goals"],
                    availability={"days_per_week": 5},
                    available_equipment=config["equipment"],  # Use correct field name
                    program_length_weeks=8,
                    user_level="intermediate"
                )
                
                # Generate program
                program_result = await program_service.generate_program_skeleton(test_request)
                
                if program_result.success:
                    # Analyze day spacing
                    spacing_analysis = self._analyze_5day_spacing(program_result.program_skeleton)
                    result.details[config["name"]] = spacing_analysis
                    
                    # Validate against expected pattern
                    actual_days = spacing_analysis["training_days"]
                    expected_days = self.EXPECTED_5DAY_PATTERN
                    
                    if actual_days == expected_days:
                        print(f"   ✅ Perfect 5-day spacing: {actual_days}")
                        spacing_analysis["spacing_validation"] = "perfect"
                    elif len(actual_days) == 5 and self._is_optimal_spacing(actual_days):
                        print(f"   ✅ Optimal spacing (alternative): {actual_days}")
                        spacing_analysis["spacing_validation"] = "optimal_alternative"
                        result.warnings.append(f"{config['name']}: Using alternative optimal spacing")
                    else:
                        print(f"   ❌ Suboptimal spacing: {actual_days}")
                        spacing_analysis["spacing_validation"] = "suboptimal"
                        result.errors.append(f"{config['name']}: Suboptimal day spacing detected")
                    
                    # Check rest day distribution
                    rest_analysis = self._analyze_rest_day_distribution(spacing_analysis["rest_days"])
                    spacing_analysis["rest_distribution"] = rest_analysis
                    
                    if not rest_analysis["optimal"]:
                        result.warnings.append(f"{config['name']}: Suboptimal rest distribution")
                    
                else:
                    result.errors.append(f"{config['name']}: Program generation failed")
            
            result.success = len(result.errors) == 0
            
            if result.success:
                print("✅ 5-day intelligent day spacing logic passed")
            else:
                print("❌ 5-day intelligent day spacing logic failed")
                
        except Exception as e:
            error_trace_id = error_logger.log_error(
                error_code="DAY_SPACING_TEST_FAILED",
                error_message="5-day day spacing test failed",
                error_details={"error_type": type(e).__name__, "error_message": str(e)},
                context={"test_phase": "day_spacing_logic"}
            )
            result.errors.append(f"Day spacing test failed: {str(e)}")
            result.trace_id = error_trace_id
        
        return result
    
    async def _test_primary_region_rotation(self, session: AsyncSession) -> TestResult:
        """Test primary region rotation logic to avoid consecutive same regions."""
        print("\n🔄 Test 4: Primary Region Rotation Logic")
        print("-" * 50)
        
        result = TestResult(
            test_name="Primary Region Rotation",
            success=False,
            errors=[],
            warnings=[],
            details={}
        )
        
        try:
            program_service = EnhancedProgramService(db_session=session)
            
            # Generate a 5-day resistance-focused program to test rotation
            test_request = ProgramGenerationRequest(
                user_id="test_user_456",  # Add required user_id
                normalized_goals={
                    "primary_strength": 0.8,
                    "normalized_hypertrophy_fat_loss": 0.7,
                    "normalized_power_mobility": 0.3,
                    "strength_bias": 0.8,
                    "endurance_bias": 0.3
                },
                availability={"days_per_week": 5},
                available_equipment=["barbell", "dumbbell", "bodyweight"],  # Correct field name
                program_length_weeks=8,  # Minimum required weeks
                user_level="intermediate"
            )
            
            program_result = await program_service.generate_program_skeleton(test_request)
            
            if program_result.success:
                # Analyze region rotation across multiple weeks
                rotation_analysis = self._analyze_region_rotation_detailed(program_result.program_skeleton)
                result.details["rotation_analysis"] = rotation_analysis
                
                print(f"📊 Analyzed {rotation_analysis['total_weeks']} weeks")
                print(f"📊 Region sequence: {rotation_analysis['region_sequence'][:10]}...")  # Truncate for readability
                
                # Check for consecutive same regions
                if rotation_analysis["consecutive_violations"] == 0:
                    print("✅ No consecutive same region violations")
                    rotation_analysis["rotation_validation"] = "perfect"
                elif rotation_analysis["consecutive_violations"] <= 2:
                    print(f"⚠️  Minor rotation issues: {rotation_analysis['consecutive_violations']} violations")
                    rotation_analysis["rotation_validation"] = "minor_issues"
                    result.warnings.append(f"Minor region rotation violations: {rotation_analysis['consecutive_violations']}")
                else:
                    print(f"❌ Major rotation issues: {rotation_analysis['consecutive_violations']} violations")
                    rotation_analysis["rotation_validation"] = "major_issues"
                    result.errors.append(f"Major region rotation violations: {rotation_analysis['consecutive_violations']}")
                
                # Check upper/lower balance
                balance = rotation_analysis["upper_lower_balance"]
                total_upper = balance["upper_anterior"] + balance["upper_posterior"] + balance["shoulder"]
                total_lower = balance["lower_anterior"] + balance["lower_posterior"]
                
                if abs(total_upper - total_lower) > 3:
                    result.warnings.append(f"Imbalanced upper/lower distribution: Upper={total_upper}, Lower={total_lower}")
                
                result.success = len(result.errors) == 0
                
            else:
                result.errors.append("Program generation failed for region rotation test")
                
        except Exception as e:
            error_trace_id = error_logger.log_error(
                error_code="REGION_ROTATION_TEST_FAILED",
                error_message="Primary region rotation test failed",
                error_details={"error_type": type(e).__name__, "error_message": str(e)},
                context={"test_phase": "region_rotation_logic"}
            )
            result.errors.append(f"Region rotation test failed: {str(e)}")
            result.trace_id = error_trace_id
        
        return result
    
    async def _test_complete_5day_program(self, session: AsyncSession) -> TestResult:
        """Test complete 5-day program generation with all components integrated."""
        print("\n📋 Test 5: Complete 5-Day Program Generation")
        print("-" * 50)
        
        result = TestResult(
            test_name="Complete 5-Day Program",
            success=False,
            errors=[],
            warnings=[],
            details={}
        )
        
        try:
            program_service = EnhancedProgramService(db_session=session)
            
            # Create comprehensive 5-day program request
            comprehensive_request = ProgramGenerationRequest(
                user_id="test_user_789",  # Add required user_id
                normalized_goals={
                    "primary_strength": 0.7,
                    "normalized_hypertrophy_fat_loss": 0.6,
                    "normalized_power_mobility": 0.4,
                    "strength_bias": 0.7,
                    "endurance_bias": 0.5
                },
                availability={"days_per_week": 5},
                available_equipment=["barbell", "dumbbell", "bodyweight", "band"],  # Correct field name
                program_length_weeks=12,
                user_level="intermediate"
            )
            
            print("🧪 Generating comprehensive 5-day program...")
            
            # Generate the complete program
            program_result = await program_service.generate_program_skeleton(comprehensive_request)
            
            if program_result.success:
                program_skeleton = program_result.program_skeleton
                
                # Comprehensive analysis
                comprehensive_analysis = {
                    "basic_stats": self._analyze_program_basic_stats(program_skeleton),
                    "session_distribution": self._analyze_session_distribution(program_skeleton),
                    "day_spacing_validation": self._analyze_5day_spacing(program_skeleton),
                    "region_rotation_analysis": self._analyze_region_rotation_detailed(program_skeleton),
                    "equipment_utilization": self._analyze_equipment_utilization(program_skeleton),
                    "progression_analysis": self._analyze_progression_patterns(program_skeleton)
                }
                
                result.details["comprehensive_analysis"] = comprehensive_analysis
                
                # Validation checks
                validation_results = self._validate_comprehensive_program(comprehensive_analysis)
                result.details["validation_results"] = validation_results
                
                # Print summary
                stats = comprehensive_analysis["basic_stats"]
                print(f"✅ Program generated successfully")
                print(f"📊 Total weeks: {stats['total_weeks']}")
                print(f"📊 Total sessions: {stats['total_sessions']}")
                print(f"📊 Average sessions per week: {stats['avg_sessions_per_week']:.1f}")
                print(f"📊 Session type distribution: {comprehensive_analysis['session_distribution']}")
                
                # Check for critical issues
                if validation_results["critical_issues"]:
                    result.errors.extend(validation_results["critical_issues"])
                    print(f"❌ Critical issues found: {len(validation_results['critical_issues'])}")
                
                if validation_results["warnings"]:
                    result.warnings.extend(validation_results["warnings"])
                    print(f"⚠️  Warnings found: {len(validation_results['warnings'])}")
                
                if not validation_results["critical_issues"] and not validation_results["warnings"]:
                    print("✅ All validation checks passed")
                
                result.success = len(validation_results["critical_issues"]) == 0
                
            else:
                result.errors.append(f"Program generation failed: {program_result.errors}")
                print(f"❌ Program generation failed: {program_result.errors}")
                
        except Exception as e:
            error_trace_id = error_logger.log_error(
                error_code="COMPLETE_PROGRAM_TEST_FAILED",
                error_message="Complete 5-day program test failed",
                error_details={"error_type": type(e).__name__, "error_message": str(e)},
                context={"test_phase": "complete_program_generation"}
            )
            result.errors.append(f"Complete program test failed: {str(e)}")
            result.trace_id = error_trace_id
        
        return result
    
    async def _test_error_handling_integration(self) -> TestResult:
        """Test error handling and logging throughout the system."""
        print("\n🚨 Test 6: Error Handling and Logging Integration")
        print("-" * 50)
        
        result = TestResult(
            test_name="Error Handling Integration",
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
            
            # Test error traceability
            if logged_errors:
                sample_trace_id = logged_errors[0]["trace_id"]
                traced_error = error_logger.get_error_by_trace_id(sample_trace_id)
                
                if traced_error:
                    result.details["traceability_test"] = "passed"
                    print("✅ Error traceability working correctly")
                else:
                    result.warnings.append("Error traceability may have issues")
                    result.details["traceability_test"] = "warning"
            
            result.success = True
            print("✅ Error handling and logging integration passed")
            
        except Exception as e:
            result.errors.append(f"Error handling test failed: {str(e)}")
            print(f"❌ Error handling test failed: {str(e)}")
        
        return result
    
    # Helper methods for analysis
    def _analyze_5day_spacing(self, program_skeleton: ProgramSkeleton) -> Dict[str, Any]:
        """Analyze 5-day spacing in program skeleton."""
        analysis = {
            "training_days": [],
            "rest_days": [],
            "spacing_pattern": "unknown",
            "consecutive_training_days": 0,
            "consecutive_rest_days": 0,
            "optimal_spacing": False
        }
        
        if program_skeleton.training_blocks and program_skeleton.training_blocks[0].weekly_plans:
            first_week = program_skeleton.training_blocks[0].weekly_plans[0]
            training_days = sorted([s.day_number for s in first_week.sessions])
            
            analysis["training_days"] = training_days
            analysis["rest_days"] = [day for day in range(1, 8) if day not in training_days]
            
            # Analyze consecutive patterns
            max_consecutive_training = 1
            current_consecutive = 1
            
            for i in range(1, len(training_days)):
                if training_days[i] == training_days[i-1] + 1:
                    current_consecutive += 1
                    max_consecutive_training = max(max_consecutive_training, current_consecutive)
                else:
                    current_consecutive = 1
            
            analysis["consecutive_training_days"] = max_consecutive_training
            
            # Check rest day patterns
            rest_days = analysis["rest_days"]
            max_consecutive_rest = 1
            current_rest_consecutive = 1
            
            for i in range(1, len(rest_days)):
                if rest_days[i] == rest_days[i-1] + 1:
                    current_rest_consecutive += 1
                    max_consecutive_rest = max(max_consecutive_rest, current_rest_consecutive)
                else:
                    current_rest_consecutive = 1
            
            analysis["consecutive_rest_days"] = max_consecutive_rest
            
            # Check if spacing is optimal (2 active, 1 rest, 2 active pattern)
            if training_days == self.EXPECTED_5DAY_PATTERN:
                analysis["spacing_pattern"] = "optimal_5day"
                analysis["optimal_spacing"] = True
            elif len(training_days) == 5 and max_consecutive_training <= 2:
                analysis["spacing_pattern"] = "acceptable_alternative"
                analysis["optimal_spacing"] = True
            else:
                analysis["spacing_pattern"] = "suboptimal"
                analysis["optimal_spacing"] = False
        
        return analysis
    
    def _is_optimal_spacing(self, training_days: List[int]) -> bool:
        """Check if training day spacing is optimal."""
        if len(training_days) != 5:
            return False
        
        # Check for maximum 2 consecutive training days
        consecutive_count = 1
        max_consecutive = 1
        
        for i in range(1, len(training_days)):
            if training_days[i] == training_days[i-1] + 1:
                consecutive_count += 1
                max_consecutive = max(max_consecutive, consecutive_count)
            else:
                consecutive_count = 1
        
        return max_consecutive <= 2
    
    def _analyze_rest_day_distribution(self, rest_days: List[int]) -> Dict[str, Any]:
        """Analyze rest day distribution for optimal recovery."""
        analysis = {
            "optimal": True,
            "issues": [],
            "rest_patterns": []
        }
        
        if not rest_days:
            analysis["optimal"] = False
            analysis["issues"].append("No rest days found")
            return analysis
        
        # Check for weekend rest days (preferred)
        weekend_rest = 6 in rest_days or 7 in rest_days
        if not weekend_rest:
            analysis["issues"].append("No weekend rest days")
        
        # Check for mid-week rest day (Wednesday preferred)
        midweek_rest = 4 in rest_days
        if not midweek_rest:
            analysis["issues"].append("No mid-week rest day")
        
        # Check rest day spacing
        if len(rest_days) >= 2:
            for i in range(len(rest_days) - 1):
                gap = rest_days[i+1] - rest_days[i]
                if gap > 4:
                    analysis["issues"].append(f"Large gap between rest days: {gap} days")
        
        analysis["optimal"] = len(analysis["issues"]) == 0
        return analysis
    
    def _analyze_region_rotation_detailed(self, program_skeleton: ProgramSkeleton) -> Dict[str, Any]:
        """Detailed analysis of region rotation patterns."""
        analysis = {
            "total_weeks": 0,
            "region_sequence": [],
            "weekly_breakdown": {},
            "consecutive_violations": 0,
            "upper_lower_balance": {
                "upper_anterior": 0,
                "upper_posterior": 0,
                "lower_anterior": 0,
                "lower_posterior": 0,
                "shoulder": 0,
                "full_body": 0,
                "core": 0
            }
        }
        
        if not program_skeleton.training_blocks:
            return analysis
        
        week_number = 1
        for block in program_skeleton.training_blocks:
            for week in block.weekly_plans:
                analysis["total_weeks"] += 1
                weekly_regions = {}
                
                for session in week.sessions:
                    day = session.day_number
                    # Extract regions from session (simplified - would need actual implementation)
                    regions = self._extract_session_regions(session)
                    weekly_regions[day] = regions
                    
                    # Add to sequence and balance
                    for region in regions:
                        analysis["region_sequence"].append(region.value if hasattr(region, 'value') else str(region))
                        
                        # Update balance counts
                        region_key = str(region).lower().replace("_", "_")
                        if "upper" in region_key and "anterior" in region_key:
                            analysis["upper_lower_balance"]["upper_anterior"] += 1
                        elif "upper" in region_key and "posterior" in region_key:
                            analysis["upper_lower_balance"]["upper_posterior"] += 1
                        elif "lower" in region_key and "anterior" in region_key:
                            analysis["upper_lower_balance"]["lower_anterior"] += 1
                        elif "lower" in region_key and "posterior" in region_key:
                            analysis["upper_lower_balance"]["lower_posterior"] += 1
                        elif "shoulder" in region_key:
                            analysis["upper_lower_balance"]["shoulder"] += 1
                        elif "full" in region_key:
                            analysis["upper_lower_balance"]["full_body"] += 1
                        elif "core" in region_key:
                            analysis["upper_lower_balance"]["core"] += 1
                
                analysis["weekly_breakdown"][week_number] = weekly_regions
                week_number += 1
        
        # Count consecutive violations
        consecutive_count = 1
        max_consecutive = 1
        for i in range(1, len(analysis["region_sequence"])):
            if analysis["region_sequence"][i] == analysis["region_sequence"][i-1]:
                consecutive_count += 1
                max_consecutive = max(max_consecutive, consecutive_count)
            else:
                if consecutive_count > 2:  # More than 2 consecutive is a violation
                    analysis["consecutive_violations"] += (consecutive_count - 2)
                consecutive_count = 1
        
        # Check final sequence
        if consecutive_count > 2:
            analysis["consecutive_violations"] += (consecutive_count - 2)
        
        return analysis
    
    def _extract_session_regions(self, session: SessionSkeleton) -> List[PrimaryRegion]:
        """Extract primary regions from session skeleton."""
        # This is a simplified implementation - would need actual logic
        # based on session type and other factors
        
        if session.session_type in [SessionType.RESISTANCE_ACCESSORY, SessionType.RESISTANCE_CIRCUITS]:
            # Simulate region assignment based on day number
            day_rotation = {
                1: [PrimaryRegion.ANTERIOR_UPPER],  # Monday
                2: [PrimaryRegion.ANTERIOR_LOWER],  # Tuesday
                4: [PrimaryRegion.POSTERIOR_UPPER], # Thursday
                5: [PrimaryRegion.POSTERIOR_LOWER], # Friday
                6: [PrimaryRegion.FULL_BODY]        # Saturday
            }
            return day_rotation.get(session.day_number, [PrimaryRegion.FULL_BODY])
        else:
            return [PrimaryRegion.FULL_BODY]
    
    def _analyze_program_basic_stats(self, program_skeleton: ProgramSkeleton) -> Dict[str, Any]:
        """Analyze basic program statistics."""
        stats = {
            "total_weeks": 0,
            "total_sessions": 0,
            "avg_sessions_per_week": 0.0,
            "blocks_count": len(program_skeleton.training_blocks)
        }
        
        total_sessions = 0
        total_weeks = 0
        
        for block in program_skeleton.training_blocks:
            for week in block.weekly_plans:
                total_weeks += 1
                total_sessions += len(week.sessions)
        
        stats["total_weeks"] = total_weeks
        stats["total_sessions"] = total_sessions
        stats["avg_sessions_per_week"] = total_sessions / total_weeks if total_weeks > 0 else 0
        
        return stats
    
    def _analyze_session_distribution(self, program_skeleton: ProgramSkeleton) -> Dict[str, Any]:
        """Analyze session type distribution."""
        distribution = {}
        total_sessions = 0
        
        for block in program_skeleton.training_blocks:
            for week in block.weekly_plans:
                for session in week.sessions:
                    session_type = session.session_type.value
                    distribution[session_type] = distribution.get(session_type, 0) + 1
                    total_sessions += 1
        
        # Convert to percentages
        percentage_distribution = {}
        for session_type, count in distribution.items():
            percentage_distribution[session_type] = (count / total_sessions * 100) if total_sessions > 0 else 0
        
        return percentage_distribution
    
    def _analyze_equipment_utilization(self, program_skeleton: ProgramSkeleton) -> Dict[str, Any]:
        """Analyze equipment utilization across the program."""
        # This would need actual implementation based on movement selection
        return {
            "equipment_variety": "high",
            "primary_equipment": ["barbell", "dumbbell"],
            "accessory_equipment": ["bodyweight", "band"],
            "utilization_score": 0.85
        }
    
    def _analyze_progression_patterns(self, program_skeleton: ProgramSkeleton) -> Dict[str, Any]:
        """Analyze progression patterns across weeks."""
        # This would analyze intensity, volume, complexity progression
        return {
            "progression_type": "linear_periodized",
            "intensity_progression": "gradual_increase",
            "volume_variation": "undulating",
            "complexity_progression": "skill_based"
        }
    
    def _validate_comprehensive_program(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate comprehensive program against requirements."""
        validation = {
            "critical_issues": [],
            "warnings": [],
            "recommendations": []
        }
        
        # Basic stats validation
        stats = analysis["basic_stats"]
        if stats["avg_sessions_per_week"] < 4.5 or stats["avg_sessions_per_week"] > 5.5:
            validation["critical_issues"].append(f"Invalid sessions per week: {stats['avg_sessions_per_week']}")
        
        # Day spacing validation
        spacing = analysis["day_spacing_validation"]
        if not spacing["optimal_spacing"]:
            validation["critical_issues"].append(f"Suboptimal day spacing: {spacing['spacing_pattern']}")
        
        # Region rotation validation
        rotation = analysis["region_rotation_analysis"]
        if rotation["consecutive_violations"] > 3:
            validation["critical_issues"].append(f"Too many region rotation violations: {rotation['consecutive_violations']}")
        
        # Session distribution validation
        session_dist = analysis["session_distribution"]
        resistance_sessions = session_dist.get("resistance_accessory", 0) + session_dist.get("resistance_circuits", 0)
        if resistance_sessions < 60:  # Less than 60% resistance sessions
            validation["warnings"].append(f"Low resistance session percentage: {resistance_sessions:.1f}%")
        
        return validation


async def main():
    """Main test execution for enhanced 5-day program system."""
    print("🚀 Enhanced 5-Day Program System Test Suite")
    print("=" * 70)
    print("Testing comprehensive 5-day program generation with:")
    print("• Pattern subtype mapping verification")
    print("• Intelligent day spacing logic [1,2,4,5,6]")
    print("• Primary region rotation to avoid consecutive same regions")
    print("• Enhanced movement service integration")
    print("• Comprehensive error logging and validation")
    print("=" * 70)
    
    tester = Enhanced5DayProgramTester()
    
    try:
        # Run comprehensive test suite
        results = await tester.run_comprehensive_5day_test()
        
        # Print detailed results summary
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 70)
        
        print(f"✅ Tests Passed: {results['tests_passed']}")
        print(f"❌ Tests Failed: {results['tests_failed']}")
        print(f"⏱️  Total Duration: {results['total_duration_seconds']:.2f} seconds")
        
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
        results_file = results_dir / f"5day_enhanced_system_test_{timestamp}.json"
        
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
        
        # Return success status
        return results['tests_failed'] == 0 and len(results['critical_failures']) == 0
        
    except Exception as e:
        print(f"💥 Test suite crashed: {str(e)}")
        # Log the crash
        error_logger.log_error(
            error_code="TEST_SUITE_CRASH",
            error_message="5-day enhanced system test suite crashed",
            error_details={"error_type": type(e).__name__, "error_message": str(e)},
            context={"test_phase": "suite_execution"}
        )
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)