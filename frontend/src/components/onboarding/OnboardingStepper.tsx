/**
 * OnboardingStepper
 * Step progress indicator. Stateless — driven by currentStep prop.
 */

import { Check } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface OnboardingStep {
  number: number;
  label: string;
}

export const ONBOARDING_STEPS: OnboardingStep[] = [
  { number: 1, label: 'Goals' },
  { number: 2, label: 'Availability' },
  { number: 3, label: 'Equipment' },
  { number: 4, label: 'Experience' },
  { number: 5, label: 'Review' },
];

interface OnboardingStepperProps {
  currentStep: number;
  totalSteps?: number;
}

export function OnboardingStepper({
  currentStep,
  totalSteps = ONBOARDING_STEPS.length,
}: OnboardingStepperProps) {
  return (
    <div className="flex items-center justify-center gap-0">
      {ONBOARDING_STEPS.slice(0, totalSteps).map((step, idx) => {
        const isCompleted = step.number < currentStep;
        const isCurrent = step.number === currentStep;
        const isLast = idx === totalSteps - 1;

        return (
          <div key={step.number} className="flex items-center">
            {/* Step circle */}
            <div className="flex flex-col items-center gap-1.5">
              <div
                className={cn(
                  'flex items-center justify-center w-8 h-8 rounded-full text-xs font-semibold border-2 transition-all',
                  isCompleted &&
                    'bg-primary-600 border-primary-600 text-white',
                  isCurrent &&
                    'bg-white border-primary-600 text-primary-600 dark:bg-surface-900',
                  !isCompleted &&
                    !isCurrent &&
                    'bg-surface-100 border-surface-200 text-surface-400 dark:bg-surface-800 dark:border-surface-700'
                )}
              >
                {isCompleted ? <Check className="w-4 h-4" /> : step.number}
              </div>
              <span
                className={cn(
                  'text-xs font-medium hidden sm:block',
                  isCurrent
                    ? 'text-primary-600 dark:text-primary-400'
                    : isCompleted
                      ? 'text-surface-500'
                      : 'text-surface-400'
                )}
              >
                {step.label}
              </span>
            </div>

            {/* Connector line */}
            {!isLast && (
              <div
                className={cn(
                  'h-0.5 w-12 sm:w-16 mx-1 transition-colors',
                  isCompleted ? 'bg-primary-600' : 'bg-surface-200 dark:bg-surface-700'
                )}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}
