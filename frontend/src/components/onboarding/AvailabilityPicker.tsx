/**
 * AvailabilityPicker
 * Select days per week and time per session.
 */

import * as SwitchPrimitive from '@radix-ui/react-switch';
import { cn } from '../../lib/utils';
import { VALID_DAYS } from '../../types/enums';
import type { AvailabilityConfig } from '../../types/onboarding';

interface AvailabilityPickerProps {
  value: AvailabilityConfig;
  onChange: (value: AvailabilityConfig) => void;
}

const TIME_OPTIONS = [30, 45, 60, 75, 90, 120] as const;

export function AvailabilityPicker({ value, onChange }: AvailabilityPickerProps) {
  const { days_per_week, time_allocation } = value;

  return (
    <div className="space-y-8">
      {/* Days per week */}
      <div className="space-y-3">
        <label className="text-sm font-medium text-surface-700 dark:text-surface-300">
          Training days per week
        </label>
        <div className="flex gap-2 flex-wrap">
          {([1, 2, 3, 4, 5, 6, 7] as const).map((n) => (
            <button
              key={n}
              type="button"
              onClick={() => onChange({ ...value, days_per_week: n })}
              className={cn(
                'w-12 h-12 rounded-xl text-sm font-semibold transition-all border-2',
                days_per_week === n
                  ? 'bg-primary-600 border-primary-600 text-white shadow-sm'
                  : 'bg-white dark:bg-surface-900 border-surface-200 dark:border-surface-700 text-surface-600 dark:text-surface-400 hover:border-primary-400'
              )}
            >
              {n}
            </button>
          ))}
        </div>
        <p className="text-xs text-surface-400">
          {days_per_week === 7 ? 'Every day' : `${days_per_week} day${days_per_week > 1 ? 's' : ''} per week`}
        </p>
      </div>

      {/* Preferred days (optional) */}
      <div className="space-y-3">
        <label className="text-sm font-medium text-surface-700 dark:text-surface-300">
          Preferred days{' '}
          <span className="font-normal text-surface-400">(optional)</span>
        </label>
        <div className="flex gap-2 flex-wrap">
          {VALID_DAYS.map((day) => {
            const isSelected = value.preferred_days?.includes(day) ?? false;
            return (
              <button
                key={day}
                type="button"
                onClick={() => {
                  const current = value.preferred_days ?? [];
                  const updated = isSelected
                    ? current.filter((d) => d !== day)
                    : [...current, day];
                  onChange({ ...value, preferred_days: updated.length ? updated : undefined });
                }}
                className={cn(
                  'px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-all border',
                  isSelected
                    ? 'bg-primary-100 border-primary-300 text-primary-700 dark:bg-primary-900/40 dark:border-primary-700 dark:text-primary-300'
                    : 'bg-white dark:bg-surface-900 border-surface-200 dark:border-surface-700 text-surface-500 hover:border-surface-300'
                )}
              >
                {day.slice(0, 3)}
              </button>
            );
          })}
        </div>
      </div>

      {/* Session duration */}
      <div className="space-y-3">
        <label className="text-sm font-medium text-surface-700 dark:text-surface-300">
          Session duration
        </label>
        <div className="flex gap-2 flex-wrap">
          {TIME_OPTIONS.map((mins) => (
            <button
              key={mins}
              type="button"
              onClick={() =>
                onChange({
                  ...value,
                  time_allocation: {
                    ...time_allocation,
                    default_time_per_day: mins,
                    delegate_to_system: false,
                  },
                })
              }
              className={cn(
                'px-3 py-2 rounded-lg text-sm font-medium border-2 transition-all',
                !time_allocation.delegate_to_system &&
                  time_allocation.default_time_per_day === mins
                  ? 'bg-primary-600 border-primary-600 text-white'
                  : 'bg-white dark:bg-surface-900 border-surface-200 dark:border-surface-700 text-surface-600 dark:text-surface-400 hover:border-primary-400'
              )}
            >
              {mins}m
            </button>
          ))}
        </div>
      </div>

      {/* Delegate to system */}
      <div className="flex items-center justify-between p-4 rounded-xl border border-surface-200 dark:border-surface-700">
        <div>
          <p className="text-sm font-medium text-surface-700 dark:text-surface-300">
            Let system optimise
          </p>
          <p className="text-xs text-surface-400 mt-0.5">
            AI will allocate session times based on your goals
          </p>
        </div>
        <SwitchPrimitive.Root
          checked={time_allocation.delegate_to_system}
          onCheckedChange={(checked) =>
            onChange({
              ...value,
              time_allocation: {
                ...time_allocation,
                delegate_to_system: checked,
              },
            })
          }
          className="w-11 h-6 bg-surface-200 dark:bg-surface-700 rounded-full relative transition-colors data-[state=checked]:bg-primary-600 outline-none"
        >
          <SwitchPrimitive.Thumb className="block w-5 h-5 bg-white rounded-full shadow-sm transition-transform translate-x-0.5 data-[state=checked]:translate-x-[22px]" />
        </SwitchPrimitive.Root>
      </div>
    </div>
  );
}
