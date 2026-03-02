/**
 * Zod Validation Schemas
 * Mirror of backend Pydantic validation logic.
 * Used by React Hook Form for form validation.
 */

import { z } from 'zod';
import { EquipmentType, VALID_DAYS } from '../types/enums';

// ─── Primitives ───────────────────────────────────────────────────────────────

export const sliderValueSchema = z
  .number()
  .min(0, 'Value must be at least 0')
  .max(1, 'Value must be at most 1');

export const goalSliderSchema = z.object({
  value: sliderValueSchema,
  label: z.string().min(1, 'Label is required'),
});

// ─── Onboarding Schemas ───────────────────────────────────────────────────────

export const hierarchicalGoalSlidersSchema = z.object({
  primary_slider: goalSliderSchema,
  hypertrophy_fat_loss: goalSliderSchema,
  power_mobility: goalSliderSchema,
});

export const timeAllocationSchema = z
  .object({
    default_time_per_day: z
      .number()
      .int()
      .min(15, 'Minimum 15 minutes')
      .max(180, 'Maximum 180 minutes'),
    apply_to_all_days: z.boolean(),
    custom_times_per_day: z
      .record(z.enum(VALID_DAYS), z.number().int().min(15).max(180))
      .optional(),
    delegate_to_system: z.boolean(),
  })
  .refine(
    (data) => {
      if (!data.apply_to_all_days && !data.delegate_to_system) {
        return data.custom_times_per_day !== undefined;
      }
      return true;
    },
    {
      message: 'Custom times are required when not applying to all days',
      path: ['custom_times_per_day'],
    }
  );

export const availabilityConfigSchema = z.object({
  days_per_week: z
    .number()
    .int()
    .min(1, 'At least 1 day required')
    .max(7, 'Maximum 7 days'),
  preferred_days: z.array(z.enum(VALID_DAYS)).optional(),
  time_allocation: timeAllocationSchema,
});

export const onboardingRequestSchema = z.object({
  user_id: z.string().min(1, 'User ID is required'),
  goals: hierarchicalGoalSlidersSchema,
  availability: availabilityConfigSchema,
  available_equipment: z.array(
    z.enum(Object.values(EquipmentType) as [string, ...string[]])
  ),
  experience_level: z.enum(['beginner', 'intermediate', 'advanced']),
  program_length_weeks: z
    .number()
    .int()
    .min(8, 'Minimum 8 weeks')
    .max(12, 'Maximum 12 weeks'),
});

// ─── Inferred Types ───────────────────────────────────────────────────────────

export type GoalSliderFormValues = z.infer<typeof goalSliderSchema>;
export type HierarchicalGoalSlidersFormValues = z.infer<typeof hierarchicalGoalSlidersSchema>;
export type TimeAllocationFormValues = z.infer<typeof timeAllocationSchema>;
export type AvailabilityConfigFormValues = z.infer<typeof availabilityConfigSchema>;
export type OnboardingRequestFormValues = z.infer<typeof onboardingRequestSchema>;
