/**
 * /onboarding/:step
 * Dynamic step route for the full onboarding flow.
 * Steps: 1 Goals | 2 Availability | 3 Equipment | 4 Experience | 5 Review
 *
 * All state is held in useAppStore.onboardingDraft (persisted).
 * Each step reads draft, mutates locally, and flushes on "Next".
 */

import { createFileRoute, useNavigate } from '@tanstack/react-router';
import { AnimatePresence, motion } from 'framer-motion';
import { ArrowLeft, Loader2, Sparkles, ChevronRight } from 'lucide-react';
import { useState } from 'react';
import { toast } from 'sonner';

import { OnboardingStepper, ONBOARDING_STEPS } from '../../components/onboarding/OnboardingStepper';
import { GoalSliders } from '../../components/onboarding/GoalSliders';
import { AvailabilityPicker } from '../../components/onboarding/AvailabilityPicker';
import { EquipmentSelector } from '../../components/onboarding/EquipmentSelector';
import { ExperienceSelector } from '../../components/onboarding/ExperienceSelector';
import { useGenerateProgram } from '../../api/mutations/onboarding';
import { useAppStore } from '../../stores/app.store';
import { cn } from '../../lib/utils';

import {
  DEFAULT_HIERARCHICAL_GOALS,
  DEFAULT_AVAILABILITY,
} from '../../types/onboarding';
import type {
  HierarchicalGoalSliders,
  AvailabilityConfig,
} from '../../types/onboarding';
import type { EquipmentType } from '../../types/enums';

const TOTAL_STEPS = ONBOARDING_STEPS.length;

export const Route = createFileRoute('/onboarding/$step')({
  component: OnboardingStep,
});

// ─── Step page-level animation ───────────────────────────────────────────────

const stepVariants = {
  initial: { opacity: 0, x: 24 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: -24 },
};

// ─── Step meta ───────────────────────────────────────────────────────────────

const STEP_META: Record<number, { title: string; subtitle: string }> = {
  1: {
    title: 'Define your goals',
    subtitle: 'Set your primary objective and how you want to balance your training.',
  },
  2: {
    title: 'Your schedule',
    subtitle: 'Tell us how many days and how long you can train each week.',
  },
  3: {
    title: 'Available equipment',
    subtitle: 'Select everything you have regular access to.',
  },
  4: {
    title: 'Training experience',
    subtitle: 'How long have you been training with structured programming?',
  },
  5: {
    title: 'Review & generate',
    subtitle: 'Confirm your setup and we\'ll build your personalised program.',
  },
};

// ─── Review Step ─────────────────────────────────────────────────────────────

interface ReviewStepProps {
  goals: HierarchicalGoalSliders;
  availability: AvailabilityConfig;
  equipment: EquipmentType[];
  experience: 'beginner' | 'intermediate' | 'advanced';
  programLengthWeeks: number;
}

function ReviewStep({
  goals,
  availability,
  equipment,
  experience,
  programLengthWeeks,
}: ReviewStepProps) {
  const primaryPct = Math.round(goals.primary_slider.value * 100);

  return (
    <div className="space-y-4">
      <ReviewRow
        label="Goals"
        value={`${primaryPct}% Strength / ${100 - primaryPct}% Endurance`}
      />
      <ReviewRow
        label="Availability"
        value={`${availability.days_per_week} days/week · ${
          availability.time_allocation.delegate_to_system
            ? 'AI-optimised'
            : `${availability.time_allocation.default_time_per_day}min sessions`
        }`}
      />
      <ReviewRow
        label="Equipment"
        value={
          equipment.length
            ? equipment.join(', ')
            : 'None selected'
        }
      />
      <ReviewRow label="Experience" value={experience} />
      <ReviewRow label="Program length" value={`${programLengthWeeks} weeks`} />
    </div>
  );
}

function ReviewRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between items-start gap-4 p-3 rounded-lg bg-white dark:bg-surface-900 border border-surface-100 dark:border-surface-800">
      <span className="text-sm text-surface-500 dark:text-surface-400 shrink-0">
        {label}
      </span>
      <span className="text-sm font-medium text-surface-800 dark:text-surface-200 text-right capitalize">
        {value}
      </span>
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────

function OnboardingStep() {
  const { step: stepParam } = Route.useParams();
  const navigate = useNavigate();
  const generateProgram = useGenerateProgram();

  const stepNumber = Math.max(1, Math.min(TOTAL_STEPS, parseInt(stepParam, 10) || 1));

  const onboardingDraft = useAppStore((s) => s.onboardingDraft);
  const setOnboardingDraft = useAppStore((s) => s.setOnboardingDraft);
  const clearOnboardingDraft = useAppStore((s) => s.clearOnboardingDraft);
  const setActiveProgram = useAppStore((s) => s.setActiveProgram);

  // Local copies to avoid triggering re-renders on every slider drag
  const [goals, setGoals] = useState<HierarchicalGoalSliders>(
    () => onboardingDraft?.goals ?? DEFAULT_HIERARCHICAL_GOALS
  );
  const [availability, setAvailability] = useState<AvailabilityConfig>(
    () => onboardingDraft?.availability ?? DEFAULT_AVAILABILITY
  );
  const [equipment, setEquipment] = useState<EquipmentType[]>(
    () => onboardingDraft?.availableEquipment ?? []
  );
  const [experience, setExperience] = useState<'beginner' | 'intermediate' | 'advanced'>(
    () => onboardingDraft?.experienceLevel ?? 'intermediate'
  );

  const programLengthWeeks = onboardingDraft?.programLengthWeeks ?? 10;
  const meta = STEP_META[stepNumber]!;

  // ── Validation per step ──────────────────────────────────────────────────

  function canProceed(): boolean {
    if (stepNumber === 3) return equipment.length > 0;
    return true;
  }

  // ── Navigation ────────────────────────────────────────────────────────────

  function goBack() {
    if (stepNumber === 1) {
      navigate({ to: '/' });
    } else {
      navigate({ to: '/onboarding/$step', params: { step: String(stepNumber - 1) } });
    }
  }

  async function handleNext() {
    // Persist current step data to draft
    setOnboardingDraft({
      currentStep: stepNumber,
      goals,
      availability,
      availableEquipment: equipment,
      experienceLevel: experience,
    });

    if (stepNumber === TOTAL_STEPS) {
      // ── Final step: generate ─────────────────────────────────────────────
      await handleGenerate();
    } else {
      navigate({
        to: '/onboarding/$step',
        params: { step: String(stepNumber + 1) },
      });
    }
  }

  async function handleGenerate() {
    try {
      const result = await generateProgram.mutateAsync({
        user_id: useAppStore.getState().userId, // Anonymous session ID until real auth
        goals,
        availability,
        available_equipment: equipment,
        experience_level: experience,
        program_length_weeks: programLengthWeeks,
      });

      if (result.success && result.program_skeleton) {
        setActiveProgram(result.program_skeleton);
        clearOnboardingDraft();
        toast.success('Program generated! Welcome to Alloy.');
        navigate({ to: '/program' });
      } else {
        // Log detailed error for debugging
        console.error('[Onboarding] Program generation failed:', {
          errors: result.errors,
          warnings: result.warnings,
        });
        
        const errorMessage = result.errors?.[0] ?? 'Failed to generate program';
        toast.error(errorMessage, {
          description: 'Please try again or contact support if the issue persists.',
          duration: 5000,
        });
      }
    } catch (error) {
      // Log full error details for debugging
      console.error('[Onboarding] Unexpected error during program generation:', error);
      
      // Detect network-level errors (backend not reachable)
      const isNetworkError = 
        error instanceof TypeError && 
        (error.message === 'Failed to fetch' || error.message.includes('NetworkError'));
      
      if (isNetworkError) {
        toast.error('Unable to connect to server', {
          description: 'Please check that the backend is running and try again.',
          duration: 6000,
        });
        return;
      }
      
      // Extract error details if available (from ApiClientError)
      const apiError = error as { apiError?: { message?: string; code?: string; trace_id?: string } };
      const errorMessage = apiError?.apiError?.message ?? 'An unexpected error occurred';
      const traceId = apiError?.apiError?.trace_id;
      
      // Show user-friendly error with trace ID for support
      toast.error(errorMessage, {
        description: traceId 
          ? `Error reference: ${traceId}` 
          : 'Please try again or contact support.',
        duration: 6000,
      });
    }
  }

  // ── Render ────────────────────────────────────────────────────────────────

  const isFinal = stepNumber === TOTAL_STEPS;
  const isLoading = generateProgram.isPending;

  return (
    <div className="flex flex-col flex-1">
      {/* Top bar */}
      <header className="sticky top-0 z-10 bg-surface-50/95 dark:bg-surface-950/95 backdrop-blur-sm border-b border-surface-100 dark:border-surface-800">
        <div className="max-w-xl mx-auto px-4 py-3">
          <div className="flex items-center gap-4 mb-3">
            <button
              type="button"
              onClick={goBack}
              className="flex items-center justify-center w-9 h-9 rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
              aria-label="Go back"
            >
              <ArrowLeft className="w-4 h-4 text-surface-600 dark:text-surface-400" />
            </button>

            <div className="flex-1">
              <OnboardingStepper currentStep={stepNumber} />
            </div>

            <span className="text-sm text-surface-400 tabular-nums">
              {stepNumber}/{TOTAL_STEPS}
            </span>
          </div>

          {/* Linear progress bar */}
          <div className="h-1 bg-surface-200 dark:bg-surface-800 rounded-full overflow-hidden">
            <div
              className={cn(
                'h-full transition-all duration-300 rounded-full',
                stepNumber === TOTAL_STEPS
                  ? 'bg-success'
                  : 'bg-primary-500'
              )}
              style={{ width: `${(stepNumber / TOTAL_STEPS) * 100}%` }}
            />
          </div>

          {/* Current step label */}
          <p className="text-xs text-surface-400 text-center mt-2">
            {meta.title}
          </p>
        </div>
      </header>

      {/* Step content */}
      <main className="flex-1 max-w-xl mx-auto w-full px-4 py-8">
        <AnimatePresence mode="wait">
          <motion.div
            key={stepNumber}
            variants={stepVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            transition={{ duration: 0.2, ease: 'easeInOut' }}
            className="space-y-6"
          >
            {/* Step header */}
            <div>
              <h1 className="text-xl font-semibold text-surface-900 dark:text-surface-50">
                {meta.title}
              </h1>
              <p className="mt-1 text-sm text-surface-500 dark:text-surface-400">
                {meta.subtitle}
              </p>
            </div>

            {/* Step body */}
            {stepNumber === 1 && (
              <GoalSliders value={goals} onChange={setGoals} />
            )}
            {stepNumber === 2 && (
              <AvailabilityPicker value={availability} onChange={setAvailability} />
            )}
            {stepNumber === 3 && (
              <EquipmentSelector value={equipment} onChange={setEquipment} />
            )}
            {stepNumber === 4 && (
              <ExperienceSelector value={experience} onChange={setExperience} />
            )}
            {stepNumber === 5 && (
              <ReviewStep
                goals={goals}
                availability={availability}
                equipment={equipment}
                experience={experience}
                programLengthWeeks={programLengthWeeks}
              />
            )}
          </motion.div>
        </AnimatePresence>
      </main>

      {/* Footer CTA */}
      <footer className="sticky bottom-0 bg-surface-50/80 dark:bg-surface-950/80 backdrop-blur-sm border-t border-surface-100 dark:border-surface-800">
        <div className="max-w-xl mx-auto px-4 py-4">
          <button
            type="button"
            onClick={handleNext}
            disabled={!canProceed() || isLoading}
            className={cn(
              'w-full flex items-center justify-center gap-2 rounded-xl px-6 py-3 text-sm font-semibold transition-all',
              canProceed() && !isLoading
                ? 'bg-primary-600 hover:bg-primary-700 text-white shadow-sm'
                : 'bg-surface-200 dark:bg-surface-800 text-surface-400 cursor-not-allowed'
            )}
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Generating your program…
              </>
            ) : isFinal ? (
              <>
                <Sparkles className="w-4 h-4" />
                Generate my program
              </>
            ) : (
              <>
                Continue
                <ChevronRight className="w-4 h-4" />
              </>
            )}
          </button>

          {/* Skip option — only for step 2 (availability has safe defaults).
              Step 3 (equipment) is required, so skip is not offered. */}
          {!isFinal && stepNumber === 2 && (
            <button
              type="button"
              onClick={handleNext}
              className="w-full text-center text-sm text-surface-400 hover:text-surface-600 dark:hover:text-surface-300 mt-2 py-1 transition-colors"
            >
              Skip this step
            </button>
          )}
        </div>
      </footer>
    </div>
  );
}
