/**
 * Alloy Fitness - Onboarding Types
 * TypeScript equivalents of backend models/onboarding.py
 */

import { EquipmentType } from './enums';
import type { DayOfWeek } from './enums';

/** Individual goal slider configuration */
export interface GoalSlider {
  /** Slider value from 0.0 to 1.0 */
  value: number;
  /** Human-readable label for the slider */
  label: string;
}

/** Hierarchical goal slider configuration with normalization */
export interface HierarchicalGoalSliders {
  /** Primary goal: 0.0 = pure endurance, 1.0 = pure strength */
  primary_slider: GoalSlider;
  /** Secondary goal: 0.0 = fat loss focus, 1.0 = hypertrophy focus */
  hypertrophy_fat_loss: GoalSlider;
  /** Secondary goal: 0.0 = mobility focus, 1.0 = power focus */
  power_mobility: GoalSlider;
  /** Normalized hypertrophy/fat loss weight (computed) */
  normalized_hypertrophy_fat_loss?: number;
  /** Normalized power/mobility weight (computed) */
  normalized_power_mobility?: number;
}

/** Normalized goal weights returned from backend */
export interface NormalizedGoals {
  /** Primary strength value (0.0 to 1.0) */
  primary_strength: number;
  /** Normalized hypertrophy/fat loss weight */
  normalized_hypertrophy_fat_loss: number;
  /** Normalized power/mobility weight */
  normalized_power_mobility: number;
  /** Computed strength bias (0.0 to 1.0) */
  strength_bias: number;
  /** Computed endurance bias (0.0 to 1.0) */
  endurance_bias: number;
}

/** Time allocation configuration for sessions */
export interface TimeAllocation {
  /** Default session time in minutes (15-180) */
  default_time_per_day: number;
  /** Whether to apply default time to all days */
  apply_to_all_days: boolean;
  /** Custom times for specific days (day_name: minutes) */
  custom_times_per_day?: Partial<Record<DayOfWeek, number>>;
  /** Let system optimize time allocation */
  delegate_to_system: boolean;
}

/** User availability configuration */
export interface AvailabilityConfig {
  /** Number of days available per week (1-7) */
  days_per_week: number;
  /** Preferred workout days (optional) */
  preferred_days?: DayOfWeek[];
  /** Time allocation settings */
  time_allocation: TimeAllocation;
}

/** Complete onboarding request */
export interface OnboardingRequest {
  /** User identifier */
  user_id: string;
  /** Hierarchical goal configuration */
  goals: HierarchicalGoalSliders;
  /** Availability and time configuration */
  availability: AvailabilityConfig;
  /** Equipment available to user */
  available_equipment: EquipmentType[];
  /** User fitness experience level */
  experience_level: 'beginner' | 'intermediate' | 'advanced';
  /** Desired program length in weeks (8-12) */
  program_length_weeks: number;
}

/** Response from onboarding validation */
export interface OnboardingResponse {
  /** Whether onboarding configuration is valid */
  success: boolean;
  /** Normalized goal weights */
  normalized_goals?: NormalizedGoals;
  /** Recommended program length in weeks */
  recommended_program_length?: number;
  /** Suggested time allocation per day */
  time_allocation_suggestion?: Partial<Record<DayOfWeek, number>>;
  /** Validation errors if any */
  errors?: string[];
  /** Configuration warnings */
  warnings?: string[];
}

/** Default values for creating new onboarding requests */
export const DEFAULT_GOAL_SLIDER: GoalSlider = {
  value: 0.5,
  label: '',
};

export const DEFAULT_HIERARCHICAL_GOALS: HierarchicalGoalSliders = {
  primary_slider: { value: 0.5, label: 'Strength vs Endurance' },
  hypertrophy_fat_loss: { value: 0.5, label: 'Hypertrophy vs Fat Loss' },
  power_mobility: { value: 0.5, label: 'Power vs Mobility' },
};

export const DEFAULT_TIME_ALLOCATION: TimeAllocation = {
  default_time_per_day: 60,
  apply_to_all_days: true,
  delegate_to_system: false,
};

export const DEFAULT_AVAILABILITY: AvailabilityConfig = {
  days_per_week: 3,
  time_allocation: DEFAULT_TIME_ALLOCATION,
};
