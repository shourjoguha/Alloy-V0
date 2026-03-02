/**
 * SessionCard
 * Displays a single training session with type, duration, and muscle groups.
 */

import { Clock, Target } from 'lucide-react';
import { cn, dayNumberToName, formatDuration } from '../../lib/utils';
import { Card } from '../ui/card';
import type { SessionSkeleton } from '../../types/program';
import { SessionType } from '../../types/enums';

interface SessionCardProps {
  session: SessionSkeleton;
  /** When true, renders in compact form for week view */
  compact?: boolean;
  onClick?: () => void;
}

const SESSION_TYPE_COLORS: Record<string, string> = {
  [SessionType.RESISTANCE_ACCESSORY]:
    'bg-primary-100 text-primary-700 dark:bg-primary-900/40 dark:text-primary-300',
  [SessionType.RESISTANCE_CIRCUITS]:
    'bg-secondary-100 text-secondary-700 dark:bg-secondary-900/40 dark:text-secondary-300',
  [SessionType.HYROX_STYLE]:
    'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300',
  [SessionType.MOBILITY_ONLY]:
    'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300',
  [SessionType.CARDIO_ONLY]:
    'bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-300',
};

const SESSION_TYPE_LABELS: Record<string, string> = {
  [SessionType.RESISTANCE_ACCESSORY]: 'Resistance',
  [SessionType.RESISTANCE_CIRCUITS]: 'Circuits',
  [SessionType.HYROX_STYLE]: 'Hyrox',
  [SessionType.MOBILITY_ONLY]: 'Mobility',
  [SessionType.CARDIO_ONLY]: 'Cardio',
};

export function SessionCard({ session, compact = false, onClick }: SessionCardProps) {
  const colorClass =
    SESSION_TYPE_COLORS[session.session_type] ??
    'bg-surface-100 text-surface-600 dark:bg-surface-800 dark:text-surface-400';
  const typeLabel =
    SESSION_TYPE_LABELS[session.session_type] ?? session.session_type;

  const hasHyroxWorkout = !!session.hyrox_workout_name;

  if (compact) {
    return (
      <Card
        variant="interactive"
        className="w-full text-left p-3 animate-fade-in"
        onClick={onClick}
        role="button"
        tabIndex={0}
      >
        <div className="flex items-center justify-between gap-2 mb-1.5">
          <span className={cn('text-xs font-medium px-2 py-0.5 rounded-full', colorClass)}>
            {typeLabel}
          </span>
          <span className="text-xs text-text-muted flex items-center gap-1">
            <Clock className="w-3 h-3" />
            {formatDuration(session.total_duration_minutes)}
          </span>
        </div>
        <p className="text-xs text-surface-600 dark:text-surface-400 capitalize">
          {hasHyroxWorkout ? session.hyrox_workout_name : session.session_focus}
        </p>
      </Card>
    );
  }

  return (
    <Card
      variant={onClick ? 'interactive' : 'default'}
      className="p-5 animate-fade-in"
      onClick={onClick}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-3 mb-3">
        <div>
          <p className="text-xs text-text-muted mb-0.5">
            Day {session.day_number} · {dayNumberToName(session.day_number)}
          </p>
          <h4 className="text-sm font-semibold text-surface-800 dark:text-surface-200 capitalize">
            {session.session_focus}
          </h4>
          {hasHyroxWorkout && (
            <p className="text-xs text-amber-600 dark:text-amber-400 mt-0.5">
              {session.hyrox_workout_name}
            </p>
          )}
        </div>
        <span className={cn('text-xs font-medium px-2.5 py-1 rounded-full shrink-0', colorClass)}>
          {typeLabel}
        </span>
      </div>

      {/* Metrics */}
      <div className="flex items-center gap-4 mb-3">
        <div className="flex items-center gap-1.5 text-xs text-text-muted">
          <Clock className="w-3.5 h-3.5" />
          {formatDuration(session.total_duration_minutes)}
        </div>
        <div className="flex items-center gap-1.5 text-xs text-text-muted">
          <Target className="w-3.5 h-3.5" />
          {session.blocks.length} blocks
        </div>
      </div>

      {/* Target muscles */}
      {session.target_muscle_groups && session.target_muscle_groups.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {session.target_muscle_groups.slice(0, 4).map((muscle) => (
            <span
              key={muscle}
              className="text-xs px-2 py-0.5 rounded-md bg-surface-100 dark:bg-surface-800 text-text-muted capitalize"
            >
              {muscle}
            </span>
          ))}
          {session.target_muscle_groups.length > 4 && (
            <span className="text-xs px-2 py-0.5 rounded-md bg-surface-100 dark:bg-surface-800 text-text-muted">
              +{session.target_muscle_groups.length - 4}
            </span>
          )}
        </div>
      )}
    </Card>
  );
}
