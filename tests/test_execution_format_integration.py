"""
Execution format integration tests.

Tests for execution_format parameter integration across service methods.
Verifies that execution_format is properly passed and used in rest time calculations.
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.config_loader import ConfigLoader
from services.enhanced_program_service import EnhancedProgramService


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def config_loader() -> ConfigLoader:
    """Create a ConfigLoader instance for testing."""
    config_path = Path(__file__).parent.parent / "config" / "program_building_config.yaml"
    return ConfigLoader(config_path=config_path, environment="production")


@pytest.fixture
def program_service(config_loader: ConfigLoader) -> EnhancedProgramService:
    """Create an EnhancedProgramService instance for testing."""
    return EnhancedProgramService(config_loader=config_loader)


# ============================================================================
# EXECUTION FORMAT REST TIME TESTS
# ============================================================================

class TestExecutionFormatRestTime:
    """Test execution_format in rest time calculations."""
    
    def test_standalone_sets_rest_time(self, config_loader: ConfigLoader):
        """Test standalone_sets execution format rest time."""
        rest_time = config_loader.get_rest_time(
            execution_format="standalone_sets",
            goal="strength",
            movement_type="compound",
            block_type="main",
            day_type="resistance"
        )
        
        # Baseline 90s * 2.0 (strength) * 1.5 (compound) = 270s
        # But override gives 300s
        assert rest_time == 300, f"Expected 300s for standalone_sets, got {rest_time}s"
    
    def test_supersets_rest_time(self, config_loader: ConfigLoader):
        """Test supersets execution format rest time."""
        rest_time = config_loader.get_rest_time(
            execution_format="supersets",
            goal="hypertrophy",
            movement_type="accessory",
            block_type="main",
            day_type="resistance"
        )
        
        # Baseline 60s * 1.0 (hypertrophy) * 1.0 (accessory) = 60s
        assert 50 <= rest_time <= 70, f"Expected ~60s for supersets, got {rest_time}s"
    
    def test_circuits_rest_time(self, config_loader: ConfigLoader):
        """Test circuits execution format rest time."""
        rest_time = config_loader.get_rest_time(
            execution_format="circuits",
            goal="endurance",
            movement_type="isolation",
            block_type="main",
            day_type="cardio"
        )
        
        # Baseline 45s * 0.67 (endurance) * 0.67 (isolation) * 0.0 (cardio) = 0s
        assert 0 <= rest_time <= 30, f"Expected 0-30s for circuits cardio, got {rest_time}s"
    
    def test_intervals_rest_time(self, config_loader: ConfigLoader):
        """Test intervals execution format rest time."""
        rest_time = config_loader.get_rest_time(
            execution_format="intervals",
            goal="endurance",
            movement_type="interval",
            block_type="main",
            day_type="hyrox"
        )
        
        # Baseline 30s * 0.67 (endurance) * 0.5 (interval) * 0.75 (hyrox) = ~7.5s
        # Or override might give 45s
        assert 0 <= rest_time <= 60, f"Expected reasonable rest for intervals, got {rest_time}s"
    
    def test_execution_format_comparison(self, config_loader: ConfigLoader):
        """Test that different execution formats produce different rest times."""
        # Use same parameters, different execution formats
        standalone = config_loader.get_rest_time(
            execution_format="standalone_sets",
            goal="hypertrophy",
            movement_type="accessory",
            block_type="main",
            day_type="resistance"
        )
        
        supersets = config_loader.get_rest_time(
            execution_format="supersets",
            goal="hypertrophy",
            movement_type="accessory",
            block_type="main",
            day_type="resistance"
        )
        
        circuits = config_loader.get_rest_time(
            execution_format="circuits",
            goal="hypertrophy",
            movement_type="accessory",
            block_type="main",
            day_type="resistance"
        )
        
        intervals = config_loader.get_rest_time(
            execution_format="intervals",
            goal="hypertrophy",
            movement_type="accessory",
            block_type="main",
            day_type="resistance"
        )
        
        # standalone should have longest rest, intervals shortest
        assert standalone >= supersets >= circuits >= intervals, (
            f"Rest times should decrease: {standalone}s >= {supersets}s >= "
            f"{circuits}s >= {intervals}s"
        )


# ============================================================================
# EXECUTION FORMAT MATRIX TESTS
# ============================================================================

class TestExecutionFormatMatrix:
    """Test execution_format across various parameter combinations."""
    
    def test_all_execution_formats_with_strength(self, config_loader: ConfigLoader):
        """Test all execution formats with strength goal."""
        execution_formats = ["standalone_sets", "supersets", "circuits", "intervals"]
        
        rest_times = []
        for execution_format in execution_formats:
            rest_time = config_loader.get_rest_time(
                execution_format=execution_format,
                goal="strength",
                movement_type="compound",
                block_type="main",
                day_type="resistance"
            )
            rest_times.append(rest_time)
            assert rest_time > 0, f"Rest time should be positive for {execution_format}"
        
        # Check ordering (standalone should be highest)
        assert rest_times[0] > rest_times[1], "standalone_sets > supersets"
        assert rest_times[1] > rest_times[2], "supersets > circuits"
    
    def test_all_execution_formats_with_endurance(self, config_loader: ConfigLoader):
        """Test all execution formats with endurance goal."""
        execution_formats = ["standalone_sets", "supersets", "circuits", "intervals"]
        
        for execution_format in execution_formats:
            rest_time = config_loader.get_rest_time(
                execution_format=execution_format,
                goal="endurance",
                movement_type="isolation",
                block_type="main",
                day_type="cardio"
            )
            
            # Cardio day type gives 0.0 multiplier, so rest should be minimal
            assert 0 <= rest_time <= 60, (
                f"Endurance cardio should have minimal rest for {execution_format}"
            )
    
    def test_all_execution_formats_with_all_movement_types(self, config_loader: ConfigLoader):
        """Test all execution formats with all movement types."""
        execution_formats = ["standalone_sets", "supersets", "circuits", "intervals"]
        movement_types = ["compound", "accessory", "isolation", "superset", "interval"]
        
        for execution_format in execution_formats:
            for movement_type in movement_types:
                rest_time = config_loader.get_rest_time(
                    execution_format=execution_format,
                    goal="hypertrophy",
                    movement_type=movement_type,
                    block_type="main",
                    day_type="resistance"
                )
                
                assert rest_time >= 0, (
                    f"Rest time should be non-negative for {execution_format}_{movement_type}"
                )
    
    def test_all_execution_formats_with_all_block_types(self, config_loader: ConfigLoader):
        """Test all execution formats with all block types."""
        execution_formats = ["standalone_sets", "supersets", "circuits", "intervals"]
        block_types = ["warmup", "main", "cooldown"]
        
        for execution_format in execution_formats:
            for block_type in block_types:
                rest_time = config_loader.get_rest_time(
                    execution_format=execution_format,
                    goal="hypertrophy",
                    movement_type="accessory",
                    block_type=block_type,
                    day_type="resistance"
                )
                
                assert rest_time >= 0, (
                    f"Rest time should be non-negative for {execution_format}_{block_type}"
                )
                
                # Cooldown should have less rest than main
                if block_type == "cooldown":
                    main_rest = config_loader.get_rest_time(
                        execution_format=execution_format,
                        goal="hypertrophy",
                        movement_type="accessory",
                        block_type="main",
                        day_type="resistance"
                    )
                    assert rest_time < main_rest, "Cooldown should have less rest than main"
    
    def test_all_execution_formats_with_all_day_types(self, config_loader: ConfigLoader):
        """Test all execution formats with all day types."""
        execution_formats = ["standalone_sets", "supersets", "circuits", "intervals"]
        day_types = ["resistance", "hyrox", "cardio", "mobility"]
        
        for execution_format in execution_formats:
            for day_type in day_types:
                rest_time = config_loader.get_rest_time(
                    execution_format=execution_format,
                    goal="hypertrophy",
                    movement_type="accessory",
                    block_type="main",
                    day_type=day_type
                )
                
                assert rest_time >= 0, (
                    f"Rest time should be non-negative for {execution_format}_{day_type}"
                )
                
                # Cardio should have minimal rest
                if day_type == "cardio":
                    assert rest_time == 0, (
                        f"Cardio should have 0 rest for {execution_format}"
                    )
    
    def test_all_execution_formats_with_all_goals(self, config_loader: ConfigLoader):
        """Test all execution formats with all goal types."""
        execution_formats = ["standalone_sets", "supersets", "circuits", "intervals"]
        goals = ["strength", "hypertrophy", "endurance", "fat_loss", "general_fitness"]
        
        for execution_format in execution_formats:
            for goal in goals:
                rest_time = config_loader.get_rest_time(
                    execution_format=execution_format,
                    goal=goal,
                    movement_type="accessory",
                    block_type="main",
                    day_type="resistance"
                )
                
                assert rest_time >= 0, (
                    f"Rest time should be non-negative for {execution_format}_{goal}"
                )


# ============================================================================
# EXECUTION FORMAT EDGE CASES
# ============================================================================

class TestExecutionFormatEdgeCases:
    """Test execution_format edge cases."""
    
    def test_invalid_execution_format(self, config_loader: ConfigLoader):
        """Test that invalid execution format raises validation error."""
        from utils.config_loader import ConfigValidationError
        
        with pytest.raises(ConfigValidationError):
            config_loader.get_rest_time(
                execution_format="invalid_format",
                goal="strength",
                movement_type="compound",
                block_type="main",
                day_type="resistance"
            )
    
    def test_execution_format_case_sensitivity(self, config_loader: ConfigLoader):
        """Test execution format case sensitivity (should be case-sensitive)."""
        from utils.config_loader import ConfigValidationError
        
        # Lowercase "standalone_sets" should work (correct)
        rest_time = config_loader.get_rest_time(
            execution_format="standalone_sets",
            goal="strength",
            movement_type="compound",
            block_type="main",
            day_type="resistance"
        )
        assert rest_time > 0, "Valid lowercase execution format should work"
        
        # Mixed case "Standalone_Sets" should fail
        with pytest.raises(ConfigValidationError):
            config_loader.get_rest_time(
                execution_format="Standalone_Sets",
                goal="strength",
                movement_type="compound",
                block_type="main",
                day_type="resistance"
            )
        
        # Uppercase "STANDALONE_SETS" should fail
        with pytest.raises(ConfigValidationError):
            config_loader.get_rest_time(
                execution_format="STANDALONE_SETS",
                goal="strength",
                movement_type="compound",
                block_type="main",
                day_type="resistance"
            )
    
    def test_execution_format_with_equipment_load(self, config_loader: ConfigLoader):
        """Test execution format with equipment load."""
        execution_formats = ["standalone_sets", "supersets", "circuits"]
        equipment_loads = ["heavy", "moderate", "light"]
        
        for execution_format in execution_formats:
            heavy_rest = config_loader.get_rest_time(
                execution_format=execution_format,
                goal="strength",
                movement_type="compound",
                block_type="main",
                day_type="resistance",
                equipment_load="heavy"
            )
            
            moderate_rest = config_loader.get_rest_time(
                execution_format=execution_format,
                goal="strength",
                movement_type="compound",
                block_type="main",
                day_type="resistance",
                equipment_load="moderate"
            )
            
            light_rest = config_loader.get_rest_time(
                execution_format=execution_format,
                goal="strength",
                movement_type="compound",
                block_type="main",
                day_type="resistance",
                equipment_load="light"
            )
            
            assert heavy_rest >= moderate_rest >= light_rest, (
                f"Heavy >= moderate >= light for {execution_format}"
            )
    
    def test_execution_format_zero_rest_scenario(self, config_loader: ConfigLoader):
        """Test execution format that results in zero rest."""
        # Cardio day type with 0.0 multiplier should give 0 rest
        rest_time = config_loader.get_rest_time(
            execution_format="standalone_sets",
            goal="endurance",
            movement_type="isolation",
            block_type="cooldown",
            day_type="cardio"
        )
        
        assert rest_time == 0, "Cardio cooldown should have 0 rest"
    
    def test_execution_format_override_priority(self, config_loader: ConfigLoader):
        """Test that overrides take priority over execution_format calculation."""
        # Test strength_resistance_compound_main_standalone_sets override
        override_rest = config_loader.get_rest_time(
            execution_format="standalone_sets",
            goal="strength",
            movement_type="compound",
            block_type="main",
            day_type="resistance"
        )
        
        # Should return 300s from override, not calculated value
        assert override_rest == 300, "Override should take priority"


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
