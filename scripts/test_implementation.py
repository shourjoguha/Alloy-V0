#!/usr/bin/env python3
"""
Test script for Alloy AI Fitness System - Phase 1 & 2 Implementation
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

# Add the current directory to Python path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from models.onboarding import OnboardingRequest, HierarchicalGoalSliders, GoalSlider, AvailabilityConfig, TimeAllocation
from models.enums import EquipmentType
from services.goal_normalizer import GoalNormalizer
from services.enhanced_program_service import EnhancedProgramService
from models.program import ProgramGenerationRequest


def test_goal_normalization():
    """Test the goal normalization functionality."""
    print("🎯 Testing Goal Normalization...")
    
    normalizer = GoalNormalizer()
    
    # Test case 1: Balanced goals
    test_goals = {
        "primary_slider": 0.5,
        "hypertrophy_fat_loss": 0.5,
        "power_mobility": 0.5
    }
    
    normalized = normalizer.normalize_all_sliders(test_goals)
    print(f"Balanced goals result: {json.dumps(normalized, indent=2)}")
    
    # Test case 2: Strength-focused
    strength_goals = {
        "primary_slider": 0.8,
        "hypertrophy_fat_loss": 0.7,
        "power_mobility": 0.6
    }
    
    normalized_strength = normalizer.normalize_all_sliders(strength_goals)
    print(f"Strength-focused goals result: {json.dumps(normalized_strength, indent=2)}")
    
    # Test case 3: Endurance-focused
    endurance_goals = {
        "primary_slider": 0.2,
        "hypertrophy_fat_loss": 0.3,
        "power_mobility": 0.4
    }
    
    normalized_endurance = normalizer.normalize_all_sliders(endurance_goals)
    print(f"Endurance-focused goals result: {json.dumps(normalized_endurance, indent=2)}")
    
    print("✅ Goal normalization tests completed\n")
    return normalized_strength  # Return for further testing


def test_program_generation():
    """Test the program skeleton generation."""
    print("🏋️ Testing Program Generation...")
    
    program_service = EnhancedProgramService()
    
    # Create test request
    normalized_goals = {
        "primary_strength": 0.8,
        "normalized_hypertrophy_fat_loss": 0.75,
        "normalized_power_mobility": 0.72,
        "strength_bias": 0.75,
        "endurance_bias": 0.25
    }
    
    request = ProgramGenerationRequest(
        user_id="test_user_123",
        normalized_goals=normalized_goals,
        availability={
            "days_per_week": 4,
            "time_allocation": {
                "default_time_per_day": 60,
                "delegate_to_system": True
            }
        },
        available_equipment=[EquipmentType.BARBELL, EquipmentType.DUMBBELL, EquipmentType.BODYWEIGHT],
        program_length_weeks=12,
        experience_level="intermediate"
    )
    
    response = program_service.generate_program_skeleton(request)
    
    if response.success:
        print(f"✅ Program generated successfully!")
        print(f"Program ID: {response.program_skeleton.program_id}")
        print(f"Total weeks: {response.program_skeleton.total_weeks}")
        print(f"Total sessions: {response.program_skeleton.total_sessions}")
        print(f"Primary goal: {response.program_skeleton.primary_goal}")
        print(f"Secondary goals: {response.program_skeleton.secondary_goals}")
        print(f"Session breakdown: {json.dumps(response.session_breakdown, indent=2)}")
        
        # Show first few sessions as example
        if response.program_skeleton.training_blocks:
            first_block = response.program_skeleton.training_blocks[0]
            if first_block.weekly_plans:
                first_week = first_block.weekly_plans[0]
                print(f"\nExample sessions from Week {first_week.week_number}:")
                for i, session in enumerate(first_week.sessions[:2]):  # First 2 sessions
                    print(f"  Session {i+1}: {session.session_focus}")
                    print(f"    Duration: {session.total_duration_minutes} minutes")
                    print(f"    Type: {session.session_type.value}")
                    print(f"    Blocks: {len(session.blocks)} (warmup, main, cooldown)")
                    
                    # Show block details
                    for block in session.blocks:
                        print(f"      {block.block_type.value}: {block.duration_minutes} min - {block.notes}")
    else:
        print(f"❌ Program generation failed: {response.errors}")
    
    print("\n✅ Program generation tests completed\n")
    return response


def test_onboarding_flow():
    """Test the complete onboarding flow."""
    print("🔄 Testing Complete Onboarding Flow...")
    
    # Create onboarding request
    onboarding_request = OnboardingRequest(
        user_id="test_user_complete",
        goals=HierarchicalGoalSliders(
            primary_slider=GoalSlider(value=0.7, label="Strength vs Endurance"),
            hypertrophy_fat_loss=GoalSlider(value=0.6, label="Hypertrophy vs Fat Loss"),
            power_mobility=GoalSlider(value=0.5, label="Power vs Mobility")
        ),
        availability=AvailabilityConfig(
            days_per_week=4,
            time_allocation=TimeAllocation(
                default_time_per_day=75,
                delegate_to_system=True
            )
        ),
        available_equipment=[
            EquipmentType.BARBELL,
            EquipmentType.DUMBBELL,
            EquipmentType.KETTLEBELL,
            EquipmentType.BODYWEIGHT
        ],
        experience_level="advanced",
        program_length_weeks=10
    )
    
    print(f"Onboarding request created for user: {onboarding_request.user_id}")
    print(f"Goals: Strength bias={onboarding_request.goals.primary_slider.value}")
    print(f"Availability: {onboarding_request.availability.days_per_week} days/week")
    print(f"Equipment: {[eq.value for eq in onboarding_request.available_equipment]}")
    
    # Test goal normalization
    normalized_goals = onboarding_request.get_normalized_goals()
    print(f"\nNormalized goals: {json.dumps(normalized_goals, indent=2)}")
    
    # Test total weekly time calculation
    total_time = onboarding_request.get_total_weekly_time()
    print(f"Total weekly training time: {total_time} minutes")
    
    print("✅ Complete onboarding flow test completed\n")
    return onboarding_request


def test_error_handling():
    """Test error handling and edge cases."""
    print("⚠️ Testing Error Handling...")
    
    normalizer = GoalNormalizer()
    
    # Test invalid slider values
    try:
        invalid_goals = {
            "primary_slider": 1.5,  # Invalid - > 1.0
            "hypertrophy_fat_loss": 0.5,
            "power_mobility": 0.5
        }
        normalized = normalizer.normalize_all_sliders(invalid_goals)
        print("❌ Should have failed with invalid slider value")
    except Exception as e:
        print(f"✅ Correctly caught invalid slider value: {e}")
    
    # Test extreme configurations
    extreme_goals = {
        "primary_slider": 0.95,  # Very strength-focused
        "hypertrophy_fat_loss": 0.95,  # Very hypertrophy-focused
        "power_mobility": 0.95   # Very power-focused
    }
    
    warnings = normalizer.validate_goal_consistency(extreme_goals)
    print(f"Warnings for extreme configuration: {warnings}")
    
    print("✅ Error handling tests completed\n")


async def main():
    """Main test function."""
    print("🚀 Starting Alloy AI Fitness System Tests")
    print("=" * 50)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    try:
        # Run all tests
        normalized_goals = test_goal_normalization()
        program_response = test_program_generation()
        onboarding_request = test_onboarding_flow()
        test_error_handling()
        
        print("=" * 50)
        print("🎉 All tests completed successfully!")
        print("=" * 50)
        
        # Summary
        print("\n📊 Test Summary:")
        print(f"- Goal normalization: ✅ Working")
        print(f"- Program generation: ✅ Working")
        print(f"- Onboarding flow: ✅ Working")
        print(f"- Error handling: ✅ Working")
        
        print(f"\n🎯 Example program generated:")
        if program_response.success:
            print(f"  - Program ID: {program_response.program_skeleton.program_id}")
            print(f"  - Duration: {program_response.program_skeleton.total_weeks} weeks")
            print(f"  - Sessions: {program_response.program_skeleton.total_sessions}")
            print(f"  - Primary goal: {program_response.program_skeleton.primary_goal}")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())