/**
 * Alloy Fitness - Core Enums
 * TypeScript equivalents of backend models/enums.py
 * Using const objects for erasableSyntaxOnly compatibility
 */

/** Primary goal types for the hierarchical sliders */
export const GoalType = {
  STRENGTH: 'strength',
  ENDURANCE: 'endurance',
  HYPERTROPHY: 'hypertrophy',
  FAT_LOSS: 'fat_loss',
  POWER: 'power',
  MOBILITY: 'mobility',
} as const;
export type GoalType = (typeof GoalType)[keyof typeof GoalType];

/** Mutually exclusive main block session types */
export const SessionType = {
  RESISTANCE_ACCESSORY: 'resistance_accessory',
  RESISTANCE_CIRCUITS: 'resistance_circuits',
  HYROX_STYLE: 'hyrox_style',
  MOBILITY_ONLY: 'mobility_only',
  CARDIO_ONLY: 'cardio_only',
} as const;
export type SessionType = (typeof SessionType)[keyof typeof SessionType];

/** Session block types */
export const BlockType = {
  WARMUP: 'warmup',
  MAIN: 'main',
  COOLDOWN: 'cooldown',
} as const;
export type BlockType = (typeof BlockType)[keyof typeof BlockType];

/** Equipment types from existing database schema */
export const EquipmentType = {
  BODYWEIGHT: 'bodyweight',
  DUMBBELL: 'dumbbell',
  KETTLEBELL: 'kettlebell',
  BARBELL: 'barbell',
  MACHINE: 'machine',
  BAND: 'band',
  PLATE_MED_BALL: 'plate_or_med_ball',
} as const;
export type EquipmentType = (typeof EquipmentType)[keyof typeof EquipmentType];

/** Primary muscle regions from actual database schema */
export const PrimaryRegion = {
  ANTERIOR_LOWER: 'anterior lower',
  POSTERIOR_LOWER: 'posterior lower',
  SHOULDER: 'shoulder',
  ANTERIOR_UPPER: 'anterior upper',
  POSTERIOR_UPPER: 'posterior upper',
  FULL_BODY: 'full body',
  LOWER_BODY: 'lower body',
  UPPER_BODY: 'upper body',
  CORE: 'core',
} as const;
export type PrimaryRegion = (typeof PrimaryRegion)[keyof typeof PrimaryRegion];

/** Spinal compression levels from existing database */
export const SpinalCompression = {
  NONE: 'none',
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
} as const;
export type SpinalCompression =
  (typeof SpinalCompression)[keyof typeof SpinalCompression];

/** Discipline types from existing database */
export const DisciplineType = {
  RESISTANCE_TRAINING: 'resistance training',
  ENDURANCE: 'endurance',
  POWER: 'power',
  MOBILITY: 'mobility',
  MIXED: 'mixed',
  HYPERTROPHY: 'hypertrophy',
  OLYMPIC: 'olympic',
  CROSSFIT: 'crossfit',
  ATHLETIC: 'athletic',
  STRETCH: 'stretch',
  CARDIO: 'cardio',
} as const;
export type DisciplineType =
  (typeof DisciplineType)[keyof typeof DisciplineType];

/** Metric types from existing database */
export const MetricType = {
  REPS: 'reps',
  TIME: 'time',
  DISTANCE: 'distance',
  WEIGHT: 'weight',
} as const;
export type MetricType = (typeof MetricType)[keyof typeof MetricType];

/** Primary muscle groups from existing database schema */
export const PrimaryMuscle = {
  QUADRICEPS: 'quadriceps',
  HAMSTRINGS: 'hamstrings',
  GLUTES: 'glutes',
  CALVES: 'calves',
  CHEST: 'chest',
  LATS: 'lats',
  UPPER_BACK: 'upper_back',
  REAR_DELTS: 'rear_delts',
  FRONT_DELTS: 'front_delts',
  SIDE_DELTS: 'side_delts',
  BICEPS: 'biceps',
  TRICEPS: 'triceps',
  FOREARMS: 'forearms',
  CORE: 'core',
  OBLIQUES: 'obliques',
  LOWER_BACK: 'lower_back',
  HIP_FLEXORS: 'hip_flexors',
  ADDUCTORS: 'adductors',
  ABDUCTORS: 'abductors',
  FULL_BODY: 'full_body',
} as const;
export type PrimaryMuscle = (typeof PrimaryMuscle)[keyof typeof PrimaryMuscle];

/** Movement pattern types from existing database schema */
export const PatternType = {
  SQUAT: 'squat',
  HINGE: 'hinge',
  LUNGE: 'lunge',
  CARRY: 'carry',
  ROTATION: 'rotation',
  CORE: 'core',
  MOBILITY: 'mobility',
  HORIZONTAL_PUSH: 'horizontal_push',
  HORIZONTAL_PULL: 'horizontal_pull',
  VERTICAL_PUSH: 'vertical_push',
  VERTICAL_PULL: 'vertical_pull',
} as const;
export type PatternType = (typeof PatternType)[keyof typeof PatternType];

/** Region mapping for internal logic */
export const REGION_MAPPING: Record<string, string> = {
  'anterior lower': 'legs',
  'posterior lower': 'legs',
  shoulder: 'arms',
  'anterior upper': 'upper_body',
  'posterior upper': 'upper_body',
  'full body': 'full_body',
  'lower body': 'lower_body',
  'upper body': 'upper_body',
  core: 'core',
};

/** Valid days of the week */
export const VALID_DAYS = [
  'monday',
  'tuesday',
  'wednesday',
  'thursday',
  'friday',
  'saturday',
  'sunday',
] as const;

export type DayOfWeek = (typeof VALID_DAYS)[number];
