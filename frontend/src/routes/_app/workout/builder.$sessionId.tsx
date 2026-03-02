/**
 * /workout/builder/:sessionId
 * Workout builder with DnD reordering and exercise swap.
 */

import { createFileRoute, useNavigate } from '@tanstack/react-router';
import { ArrowLeft, RotateCcw, Save } from 'lucide-react';
import { toast } from 'sonner';
import { PageContainer } from '../../../components/layout/PageContainer';
import { ErrorBoundary } from '../../../components/shared/ErrorBoundary';
import {
  BuilderProvider,
  useBuilder,
  type BuilderExercise,
} from '../../../components/workout-builder/BuilderContext';
import { ExerciseList } from '../../../components/workout-builder/ExerciseList';
import { cn } from '../../../lib/utils';

export const Route = createFileRoute('/_app/workout/builder/$sessionId')({
  component: () => (
    <ErrorBoundary scope="WorkoutBuilder">
      <WorkoutBuilderPage />
    </ErrorBoundary>
  ),
});

// Mock exercises — to be replaced by actual session data from the program
const MOCK_EXERCISES: BuilderExercise[] = [
  { id: 'ex-1', name: 'Back Squat',       sets: 4, reps: '5-8',  restSeconds: 180, equipment: 'barbell' },
  { id: 'ex-2', name: 'Romanian Deadlift', sets: 3, reps: '8-10', restSeconds: 120, equipment: 'barbell' },
  { id: 'ex-3', name: 'Walking Lunges',    sets: 3, reps: '10',   restSeconds: 90,  equipment: 'dumbbell' },
  { id: 'ex-4', name: 'Leg Curl',          sets: 3, reps: '10-12', restSeconds: 60, equipment: 'machine' },
  { id: 'ex-5', name: 'Calf Raises',       sets: 3, reps: '15',   restSeconds: 45,  equipment: 'machine' },
];

function WorkoutBuilderPage() {
  return (
    <BuilderProvider initialExercises={MOCK_EXERCISES}>
      <BuilderContent />
    </BuilderProvider>
  );
}

function BuilderContent() {
  const { sessionId } = Route.useParams();
  const navigate = useNavigate();
  const { isDirty, reset } = useBuilder();

  function handleSave() {
    // TODO: Persist changes to API / store
    toast.success('Workout saved');
    navigate({
      to: '/workout/$sessionId',
      params: { sessionId },
    });
  }

  return (
    <PageContainer>
      {/* Header */}
      <div className="flex items-center justify-between gap-4 mb-6">
        <button
          type="button"
          onClick={() => {
            if (isDirty) {
              // TODO: Could add confirm-discard modal
              navigate({
                to: '/workout/$sessionId',
                params: { sessionId },
              });
            } else {
              navigate({
                to: '/workout/$sessionId',
                params: { sessionId },
              });
            }
          }}
          className="flex items-center gap-2 text-sm text-surface-500 hover:text-surface-700 dark:hover:text-surface-300 -ml-1"
        >
          <ArrowLeft className="w-4 h-4" />
          Back
        </button>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={reset}
            disabled={!isDirty}
            className={cn(
              'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors',
              isDirty
                ? 'border-surface-200 dark:border-surface-700 text-surface-600 dark:text-surface-400 hover:bg-surface-100 dark:hover:bg-surface-800'
                : 'border-surface-100 dark:border-surface-800 text-surface-300 cursor-not-allowed'
            )}
          >
            <RotateCcw className="w-3 h-3" />
            Reset
          </button>
          <button
            type="button"
            onClick={handleSave}
            className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg text-xs font-semibold bg-primary-600 hover:bg-primary-700 text-white transition-colors"
          >
            <Save className="w-3 h-3" />
            Save
          </button>
        </div>
      </div>

      <div className="mb-4">
        <h1 className="text-lg font-semibold text-surface-900 dark:text-surface-50">
          Edit Workout
        </h1>
        <p className="text-xs text-surface-400 mt-0.5">
          Drag to reorder · Tap swap to find alternatives
        </p>
      </div>

      <ExerciseList />
    </PageContainer>
  );
}
