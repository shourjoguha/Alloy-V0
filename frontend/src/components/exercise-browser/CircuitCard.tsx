/**
 * CircuitCard
 * Compact card for a Hyrox circuit/workout in the exercise browser.
 * Shows name, type badge, duration, and round count.
 */

import { Clock, Repeat, Star } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Card } from '../ui/card';
import { useAppStore } from '../../stores/app.store';
import type { HyroxWorkout } from '../../types/hyrox';
import { HYROX_WORKOUT_TYPE_LABELS, HYROX_WORKOUT_TYPE_COLORS } from '../../types/hyrox';

interface CircuitCardProps {
  workout: HyroxWorkout;
  className?: string;
  onClick?: () => void;
}

export function CircuitCard({ workout, className, onClick }: CircuitCardProps) {
  const isFavorite = useAppStore((s) => s.favoriteCircuits.some((c) => c.id === workout.id));
  const toggleFavorite = useAppStore((s) => s.toggleFavoriteCircuit);
  const typeLabel = HYROX_WORKOUT_TYPE_LABELS[workout.workout_type] ?? workout.workout_type;
  const typeColor = HYROX_WORKOUT_TYPE_COLORS[workout.workout_type] ??
    'bg-surface-100 text-surface-600 dark:bg-surface-800 dark:text-surface-400';

  return (
    <Card variant={onClick ? 'interactive' : 'grouped'} className={cn('p-3', className)} onClick={onClick}>
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0 flex-1">
          <p className="text-sm font-medium text-surface-800 dark:text-surface-200 truncate">
            {workout.name}
          </p>
          <div className="flex flex-wrap items-center gap-2 mt-1.5">
            <span className={cn('text-xs font-medium px-2 py-0.5 rounded-full', typeColor)}>
              {typeLabel}
            </span>
            {workout.total_time_minutes != null && (
              <span className="flex items-center gap-1 text-xs text-surface-400">
                <Clock className="w-3 h-3" />
                {workout.total_time_minutes}m
              </span>
            )}
            {workout.total_rounds != null && (
              <span className="flex items-center gap-1 text-xs text-surface-400">
                <Repeat className="w-3 h-3" />
                {workout.total_rounds} rds
              </span>
            )}
          </div>
        </div>

        <div className="flex items-center gap-1.5 shrink-0">
          {/* Complexity indicator */}
          {workout.is_complex && (
            <span className="text-xs px-1.5 py-0.5 rounded bg-amber-50 dark:bg-amber-900/20 text-amber-600 dark:text-amber-400">
              Complex
            </span>
          )}

          {/* Favorite toggle */}
          <button
            type="button"
            onClick={(e) => { e.stopPropagation(); toggleFavorite(workout.id, workout.name); }}
            className={cn(
              'p-1 rounded-md transition-colors',
              isFavorite
                ? 'text-amber-accent hover:text-amber-accent-hover'
                : 'text-surface-300 dark:text-surface-600 hover:text-amber-accent'
            )}
            aria-label={isFavorite ? 'Remove from favorites' : 'Add to favorites'}
          >
            <Star className={cn('w-3.5 h-3.5', isFavorite && 'fill-current')} />
          </button>
        </div>
      </div>
    </Card>
  );
}
