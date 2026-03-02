/**
 * Alloy Fitness - Hyrox Workout Types
 * TypeScript equivalents of backend models/hyrox.py
 */

/** Workout structure types from hyrox_workout_type enum */
export const HyroxWorkoutType = {
  AMRAP: 'amrap',
  EMOM: 'emom',
  FOR_TIME: 'for_time',
  ROUNDS_FOR_TIME: 'rounds_for_time',
  FOR_LOAD: 'for_load',
  BUY_IN: 'buy_in',
  CASH_OUT: 'cash_out',
  TIME_CAP: 'time_cap',
  LADDER: 'ladder',
  MINI_CIRCUIT: 'mini_circuit',
  EXPLICIT_TIME_GUIDANCE: 'explicit_time_guidance',
  UNKNOWN: 'unknown',
} as const;
export type HyroxWorkoutType =
  (typeof HyroxWorkoutType)[keyof typeof HyroxWorkoutType];

/** Workout goal types (display only, not used for selection) */
export const HyroxWorkoutGoal = {
  MAX_ROUNDS_REPS: 'max_rounds_reps',
  FINISH_QUICKLY: 'finish_quickly',
  COMPLETE_ROUNDS: 'complete_rounds',
  MAX_LOAD: 'max_load',
  PACE_WORK: 'pace_work',
  ENDURANCE: 'endurance',
  STRENGTH: 'strength',
  MIXED: 'mixed',
  UNKNOWN: 'unknown',
} as const;
export type HyroxWorkoutGoal =
  (typeof HyroxWorkoutGoal)[keyof typeof HyroxWorkoutGoal];

/** Workflow status for scraped workouts */
export const HyroxStatus = {
  PENDING_REVIEW: 'pending_review',
  REVIEWED: 'reviewed',
  APPROVED: 'approved',
  REJECTED: 'rejected',
} as const;
export type HyroxStatus = (typeof HyroxStatus)[keyof typeof HyroxStatus];

// ---------------------------------------------------------------------------
// Table models
// ---------------------------------------------------------------------------

/** Single movement line within a Hyrox workout */
export interface HyroxWorkoutLine {
  id: number;
  workout_id: number;
  line_number: number;
  line_text: string;
  is_rest: boolean;
  is_buy_in: boolean;
  is_cash_out: boolean;
  movement_name?: string | null;
  reps?: number | null;
  distance_meters?: number | null;
  duration_seconds?: number | null;
  weight_male?: number | null;
  weight_female?: number | null;
  calories?: number | null;
  is_max_effort: boolean;
  notes?: string | null;
  mini_circuit_id?: number | null;
  created_at?: string | null;
}

/** Sub-circuit within a Hyrox workout (mirrors hyrox_mini_circuits_staging) */
export interface HyroxMiniCircuit {
  id: number;
  workout_id: number;
  circuit_number: number;
  circuit_type: HyroxWorkoutType;
  rounds?: number | null;
  start_time?: string | null;
  end_time?: string | null;
  duration_minutes?: number | null;
  rest_after_minutes?: number | null;
  notes?: string | null;
  created_at?: string | null;
}

/** Hyrox workout metadata */
export interface HyroxWorkout {
  id: number;
  wod_id?: string | null;
  name: string;
  url: string;
  badge?: string | null;
  workout_type: HyroxWorkoutType;
  workout_goal?: HyroxWorkoutGoal | null;
  time_specification?: string | null;
  total_time_minutes?: number | null;
  time_cap_minutes?: number | null;
  total_rounds?: number | null;
  has_buy_in: boolean;
  has_cash_out: boolean;
  is_complex: boolean;
  has_mini_circuit: boolean;
  full_description?: string | null;
  scraped_at?: string | null;
  source_page?: string | null;
  status: HyroxStatus;
  notes?: string | null;
}

/** Full Hyrox workout with lines and mini circuits for UI rendering */
export interface HyroxWorkoutDetail {
  workout: HyroxWorkout;
  lines: HyroxWorkoutLine[];
  mini_circuits: HyroxMiniCircuit[];
}

// ---------------------------------------------------------------------------
// Search / Recommend
// ---------------------------------------------------------------------------

/** Paginated search results */
export interface HyroxSearchResponse {
  workouts: HyroxWorkout[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

// ---------------------------------------------------------------------------
// Display helpers
// ---------------------------------------------------------------------------

/** Human-readable labels for workout types */
export const HYROX_WORKOUT_TYPE_LABELS: Record<HyroxWorkoutType, string> = {
  [HyroxWorkoutType.AMRAP]: 'AMRAP',
  [HyroxWorkoutType.EMOM]: 'EMOM',
  [HyroxWorkoutType.FOR_TIME]: 'For Time',
  [HyroxWorkoutType.ROUNDS_FOR_TIME]: 'Rounds For Time',
  [HyroxWorkoutType.FOR_LOAD]: 'For Load',
  [HyroxWorkoutType.BUY_IN]: 'Buy-In',
  [HyroxWorkoutType.CASH_OUT]: 'Cash-Out',
  [HyroxWorkoutType.TIME_CAP]: 'Time Cap',
  [HyroxWorkoutType.LADDER]: 'Ladder',
  [HyroxWorkoutType.MINI_CIRCUIT]: 'Mini Circuit',
  [HyroxWorkoutType.EXPLICIT_TIME_GUIDANCE]: 'Timed',
  [HyroxWorkoutType.UNKNOWN]: 'Workout',
};

/** Color classes for workout type badges */
export const HYROX_WORKOUT_TYPE_COLORS: Record<HyroxWorkoutType, string> = {
  [HyroxWorkoutType.AMRAP]: 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300',
  [HyroxWorkoutType.EMOM]: 'bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-300',
  [HyroxWorkoutType.FOR_TIME]: 'bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300',
  [HyroxWorkoutType.ROUNDS_FOR_TIME]: 'bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300',
  [HyroxWorkoutType.FOR_LOAD]: 'bg-purple-100 text-purple-700 dark:bg-purple-900/40 dark:text-purple-300',
  [HyroxWorkoutType.BUY_IN]: 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300',
  [HyroxWorkoutType.CASH_OUT]: 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300',
  [HyroxWorkoutType.TIME_CAP]: 'bg-teal-100 text-teal-700 dark:bg-teal-900/40 dark:text-teal-300',
  [HyroxWorkoutType.LADDER]: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300',
  [HyroxWorkoutType.MINI_CIRCUIT]: 'bg-cyan-100 text-cyan-700 dark:bg-cyan-900/40 dark:text-cyan-300',
  [HyroxWorkoutType.EXPLICIT_TIME_GUIDANCE]: 'bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300',
  [HyroxWorkoutType.UNKNOWN]: 'bg-surface-100 text-surface-600 dark:bg-surface-800 dark:text-surface-400',
};
