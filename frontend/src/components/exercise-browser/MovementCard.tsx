/**
 * MovementCard
 * Compact card for a single movement in the exercise browser.
 * Shows name, muscle, region, equipment badges, and a favorite toggle.
 */

import { Star } from 'lucide-react';
import { cn, toTitleCase } from '../../lib/utils';
import { Card } from '../ui/card';
import { useAppStore } from '../../stores/app.store';
import type { Movement } from '../../types/movement';

interface MovementCardProps {
  movement: Movement;
  className?: string;
}

const EQUIPMENT_LABELS: Record<string, string> = {
  bodyweight_possible: 'BW',
  dumbbell_possible: 'DB',
  kettlebell_possible: 'KB',
  barbell_possible: 'BB',
  machine_possible: 'MC',
  band_possible: 'BD',
  plate_or_med_ball_possible: 'PL',
};

export function MovementCard({ movement, className }: MovementCardProps) {
  const isFavorite = useAppStore((s) => s.favoriteMovementIds.includes(movement.id));
  const toggleFavorite = useAppStore((s) => s.toggleFavoriteMovement);

  const equipmentBadges = Object.entries(EQUIPMENT_LABELS)
    .filter(([key]) => movement[key as keyof Movement] === true)
    .map(([, label]) => label);

  return (
    <Card variant="grouped" className={cn('p-3', className)}>
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0 flex-1">
          <p className="text-sm font-medium text-surface-800 dark:text-surface-200 truncate">
            {movement.name}
          </p>
          <div className="flex items-center gap-2 mt-0.5">
            <span className="text-xs text-surface-400 capitalize">
              {toTitleCase(movement.primary_muscle)}
            </span>
            <span className="text-xs text-surface-300 dark:text-surface-600">·</span>
            <span className="text-xs text-surface-400 capitalize">
              {toTitleCase(movement.primary_region)}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-1.5 shrink-0">
          {/* Compound badge */}
          {movement.compound && (
            <span className="text-xs px-1.5 py-0.5 rounded bg-primary-50 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400">
              C
            </span>
          )}

          {/* Favorite toggle */}
          <button
            type="button"
            onClick={(e) => { e.stopPropagation(); toggleFavorite(movement.id); }}
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

      {/* Equipment badges */}
      {equipmentBadges.length > 0 && (
        <div className="flex flex-wrap gap-1 mt-2">
          {equipmentBadges.map((badge) => (
            <span
              key={badge}
              className="text-xs px-1.5 py-0.5 rounded bg-surface-100 dark:bg-surface-800 text-surface-500 dark:text-surface-400"
            >
              {badge}
            </span>
          ))}
        </div>
      )}
    </Card>
  );
}
