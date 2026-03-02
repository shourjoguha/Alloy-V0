/**
 * Alloy Fitness - Program Types
 * TypeScript equivalents of backend models/program.py
 */

import {
  SessionType,
  BlockType,
  EquipmentType,
  PrimaryRegion,
  SpinalCompression,
  DisciplineType,
  MetricType,
} from './enums';
import type { NormalizedGoals } from './onboarding';

/** Movement constraints for a session block */
export interface BlockConstraints {
  /** Whether compound movements are allowed */
  compound?: boolean;
  /** Allowed spinal compression levels */
  spinal_compression?: SpinalCompression[];
  /** Allowed discipline types */
  disciplines?: DisciplineType[];
  /** Required equipment types */
  equipment_types?: EquipmentType[];
  /** Target muscle regions */
  muscle_regions?: PrimaryRegion[];
  /** Allowed metric types */
  metric_types?: MetricType[];
  /** Minimum block duration in minutes */
  min_duration: number;
  /** Maximum block duration in minutes */
  max_duration: number;
}

/** A single block within a session (warmup, main, cooldown) */
export interface SessionBlock {
  /** Type of session block */
  block_type: BlockType;
  /** Session type for main blocks */
  session_type?: SessionType;
  /** Block duration in minutes (5-120) */
  duration_minutes: number;
  /** Movement constraints for this block */
  constraints: BlockConstraints;
  /** Target number of sets (1-10) */
  target_sets?: number;
  /** Target rep range (e.g., '8-12') */
  target_reps?: string;
  /** Target rest between sets in seconds (0-300) */
  target_rest_seconds?: number;
  /** Additional notes for this block */
  notes?: string;
}

/** Complete session skeleton with all blocks */
export interface SessionSkeleton {
  /** Unique session identifier */
  session_id: string;
  /** Day of week (1=Monday, 7=Sunday) */
  day_number: number;
  /** Primary focus of this session */
  session_focus: string;
  /** Total session duration in minutes (15-180) */
  total_duration_minutes: number;
  /** Session blocks in order */
  blocks: SessionBlock[];
  /** Primary muscle groups to target */
  target_muscle_groups?: PrimaryRegion[];
  /** Main session type */
  session_type: SessionType;
  /** Session difficulty level */
  difficulty_level: 'beginner' | 'intermediate' | 'advanced';
  /** ID of attached Hyrox workout from hyrox_workouts table */
  hyrox_workout_id?: number;
  /** Name of attached Hyrox workout for display */
  hyrox_workout_name?: string;
}

/** Weekly training plan with session skeletons */
export interface WeeklyPlan {
  /** Week number in program */
  week_number: number;
  /** Sessions for this week */
  sessions: SessionSkeleton[];
  /** Number of sessions this week (1-7) */
  total_sessions: number;
  /** Primary focus for this week */
  weekly_focus: string;
  /** Total weekly training time in minutes (60-840) */
  total_training_time: number;
  /** Days of week that are rest days (1-7) */
  rest_days: number[];
}

/** A training block within the program (e.g., strength focus phase) */
export interface ProgramBlock {
  /** Name of training block */
  block_name: string;
  /** Block number in sequence */
  block_number: number;
  /** Duration of block in weeks (1-6) */
  weeks_duration: number;
  /** Primary training goal for this block */
  primary_goal: string;
  /** Weekly plans for this block */
  weekly_plans: WeeklyPlan[];
  /** Specific focus for this training block */
  block_focus: string;
  /** How intensity progresses through block */
  intensity_progression: string;
}

/** Complete program skeleton with all training blocks */
export interface ProgramSkeleton {
  /** Unique program identifier */
  program_id: string;
  /** User identifier */
  user_id: string;
  /** Program name */
  program_name: string;
  /** Total program duration in weeks (8-12) */
  total_weeks: number;
  /** Total number of sessions (8-84) */
  total_sessions: number;
  /** Training blocks in sequence */
  training_blocks: ProgramBlock[];
  /** Primary training goal */
  primary_goal: string;
  /** Secondary training goals */
  secondary_goals: string[];
  /** Program creation timestamp */
  created_at: string;
}

/** Request for program skeleton generation */
export interface ProgramGenerationRequest {
  /** User identifier */
  user_id: string;
  /** Normalized goal weights from onboarding */
  normalized_goals: NormalizedGoals;
  /** User availability configuration */
  availability: {
    days_per_week: number;
    time_allocation: {
      default_time_per_day: number;
      delegate_to_system: boolean;
    };
  };
  /** Available equipment */
  available_equipment: EquipmentType[];
  /** Program length in weeks (8-12) */
  program_length_weeks: number;
  /** User experience level */
  experience_level: 'beginner' | 'intermediate' | 'advanced';
}

/** Response from program skeleton generation */
export interface ProgramGenerationResponse {
  /** Whether generation was successful */
  success: boolean;
  /** Generated program skeleton */
  program_skeleton?: ProgramSkeleton;
  /** Generation errors if any */
  errors?: string[];
  /** Generation warnings */
  warnings?: string[];
  /** Count of each session type */
  session_breakdown?: Partial<Record<SessionType, number>>;
}

/** Utility type for computed program metrics */
export interface ProgramMetrics {
  /** Total training time across all sessions (in minutes) */
  total_training_time: number;
  /** Average session duration (in minutes) */
  average_session_duration: number;
  /** Average weekly training frequency */
  weekly_training_frequency: number;
}

/** Helper function to calculate program metrics */
export function calculateProgramMetrics(
  program: ProgramSkeleton
): ProgramMetrics {
  let totalTime = 0;
  let totalSessions = 0;

  for (const block of program.training_blocks) {
    for (const week of block.weekly_plans) {
      totalTime += week.total_training_time;
      totalSessions += week.sessions.length;
    }
  }

  return {
    total_training_time: totalTime,
    average_session_duration: totalSessions > 0 ? totalTime / totalSessions : 0,
    weekly_training_frequency:
      program.total_weeks > 0 ? totalSessions / program.total_weeks : 0,
  };
}
