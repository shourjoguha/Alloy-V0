/**
 * ExerciseList
 * Sortable list of exercises with drag handles and inline swap trigger.
 */

import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { GripVertical, ArrowRightLeft, Trash2 } from 'lucide-react';
import { useBuilder, type BuilderExercise } from './BuilderContext';
import { SwapPanel } from './SwapPanel';
import { cn } from '../../lib/utils';

export function ExerciseList() {
  const { exercises, expandedSwapId } = useBuilder();

  if (exercises.length === 0) {
    return (
      <div className="py-8 text-center text-sm text-surface-400">
        No exercises in this session yet.
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {exercises.map((exercise) => (
        <div key={exercise.id}>
          <ExerciseItem exercise={exercise} />
          {expandedSwapId === exercise.id && (
            <SwapPanel exerciseId={exercise.id} />
          )}
        </div>
      ))}
    </div>
  );
}

// ─── Single Exercise Item ─────────────────────────────────────────────────

function ExerciseItem({ exercise }: { exercise: BuilderExercise }) {
  const { removeExercise, setExpandedSwapId, expandedSwapId } = useBuilder();

  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: exercise.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={cn(
        'flex items-center gap-3 px-4 py-3 rounded-xl bg-white dark:bg-surface-900 border border-surface-100 dark:border-surface-800',
        isDragging && 'opacity-50 shadow-lg z-10'
      )}
    >
      {/* Drag handle */}
      <button
        type="button"
        className="cursor-grab active:cursor-grabbing text-surface-300 dark:text-surface-600 hover:text-surface-500 touch-none"
        {...attributes}
        {...listeners}
      >
        <GripVertical className="w-4 h-4" />
      </button>

      {/* Exercise info */}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-surface-800 dark:text-surface-200 truncate">
          {exercise.name}
        </p>
        <p className="text-xs text-surface-400">
          {exercise.sets} × {exercise.reps}
          {exercise.equipment && ` · ${exercise.equipment}`}
          {exercise.restSeconds > 0 && ` · ${exercise.restSeconds}s rest`}
        </p>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-1 shrink-0">
        <button
          type="button"
          onClick={() =>
            setExpandedSwapId(
              expandedSwapId === exercise.id ? null : exercise.id
            )
          }
          className={cn(
            'flex items-center justify-center w-7 h-7 rounded-lg transition-colors',
            expandedSwapId === exercise.id
              ? 'bg-primary-100 text-primary-600 dark:bg-primary-900/40 dark:text-primary-400'
              : 'text-surface-400 hover:bg-surface-100 dark:hover:bg-surface-800 hover:text-surface-600'
          )}
          aria-label="Swap exercise"
        >
          <ArrowRightLeft className="w-3.5 h-3.5" />
        </button>
        <button
          type="button"
          onClick={() => removeExercise(exercise.id)}
          className="flex items-center justify-center w-7 h-7 rounded-lg text-surface-400 hover:bg-red-50 hover:text-red-500 dark:hover:bg-red-900/20 dark:hover:text-red-400 transition-colors"
          aria-label="Remove exercise"
        >
          <Trash2 className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}
