/**
 * ExperienceSelector
 * Three-card selector for experience level.
 */

import { cn } from '../../lib/utils';

type ExperienceLevel = 'beginner' | 'intermediate' | 'advanced';

interface ExperienceSelectorProps {
  value: ExperienceLevel;
  onChange: (value: ExperienceLevel) => void;
}

const LEVELS: {
  value: ExperienceLevel;
  label: string;
  subtitle: string;
  description: string;
}[] = [
  {
    value: 'beginner',
    label: 'Beginner',
    subtitle: '< 1 year',
    description:
      'New to structured training. Programs emphasise fundamentals, form, and habit-building.',
  },
  {
    value: 'intermediate',
    label: 'Intermediate',
    subtitle: '1–3 years',
    description:
      'Comfortable with core movements. Programs use progressive overload and periodisation.',
  },
  {
    value: 'advanced',
    label: 'Advanced',
    subtitle: '3+ years',
    description:
      'High training age. Programs include complex programming, Olympic lifts, and autoregulation.',
  },
];

export function ExperienceSelector({ value, onChange }: ExperienceSelectorProps) {
  return (
    <div className="space-y-3">
      {LEVELS.map((level) => {
        const isSelected = value === level.value;

        return (
          <button
            key={level.value}
            type="button"
            onClick={() => onChange(level.value)}
            className={cn(
              'w-full text-left p-4 rounded-xl border-2 transition-all',
              isSelected
                ? 'bg-primary-50 border-primary-500 dark:bg-primary-900/20 dark:border-primary-500'
                : 'bg-white dark:bg-surface-900 border-surface-200 dark:border-surface-700 hover:border-surface-300 dark:hover:border-surface-600'
            )}
          >
            <div className="flex items-baseline gap-2 mb-1">
              <span
                className={cn(
                  'font-semibold text-sm',
                  isSelected
                    ? 'text-primary-700 dark:text-primary-300'
                    : 'text-surface-800 dark:text-surface-200'
                )}
              >
                {level.label}
              </span>
              <span className="text-xs text-surface-400">{level.subtitle}</span>
            </div>
            <p className="text-xs text-surface-500 dark:text-surface-400 leading-relaxed">
              {level.description}
            </p>
          </button>
        );
      })}
    </div>
  );
}
