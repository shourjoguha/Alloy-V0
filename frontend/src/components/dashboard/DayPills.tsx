/**
 * DayPills
 * Horizontal scrollable row of day cards derived from the current week's sessions.
 * Each card has a fixed min-width with text wrapping so content stays within bounds.
 * Active card highlighted with amber accent.
 */

import { Clock } from 'lucide-react';
import { useUIStore } from '../../stores/ui.store';
import { cn, capitalise, formatDuration } from '../../lib/utils';
import type { SessionSkeleton } from '../../types/program';

/** Map session index → weekday label (Mon–Sun) */
const DAY_LABELS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] as const;

interface DayPillsProps {
  sessions: SessionSkeleton[];
  className?: string;
}

export function DayPills({ sessions, className }: DayPillsProps) {
  const selectedDay = useUIStore((s) => s.selectedDayIndex);
  const setSelectedDay = useUIStore((s) => s.setSelectedDayIndex);

  if (sessions.length === 0) return null;

  return (
    <div
      className={cn(
        'flex gap-3 overflow-x-auto scrollbar-hide pb-2 snap-x snap-mandatory',
        className
      )}
    >
      {sessions.map((session, idx) => {
        const isActive = selectedDay === idx;
        const dayLabel = DAY_LABELS[idx] ?? `Day ${idx + 1}`;
        const focusLabel = capitalise(session.session_focus);
        const blockCount = session.blocks?.length ?? 0;

        return (
          <button
            key={session.session_id}
            type="button"
            onClick={() => setSelectedDay(isActive ? null : idx)}
            className={cn(
              'shrink-0 snap-start w-[140px] min-w-[140px] p-3 rounded-xl text-left transition-all',
              'border flex flex-col gap-1.5',
              isActive
                ? 'bg-amber-accent text-surface-950 border-amber-accent shadow-md'
                : 'bg-white dark:bg-surface-900 text-surface-600 dark:text-surface-400 border-surface-200 dark:border-surface-700 hover:border-surface-400 dark:hover:border-surface-500'
            )}
          >
            {/* Day label */}
            <span className={cn(
              'text-[10px] font-bold uppercase tracking-wider',
              isActive ? 'text-surface-950/70' : 'text-surface-400 dark:text-surface-500'
            )}>
              {dayLabel}
            </span>

            {/* Session focus — wraps within card */}
            <span className="text-sm font-semibold leading-tight break-words">
              {focusLabel}
            </span>

            {/* Meta row */}
            <div className={cn(
              'flex items-center gap-1.5 text-[10px] mt-auto',
              isActive ? 'text-surface-950/60' : 'text-surface-400'
            )}>
              <Clock className="w-3 h-3" />
              <span>{formatDuration(session.total_duration_minutes)}</span>
              {blockCount > 0 && (
                <span className="ml-1">· {blockCount} blocks</span>
              )}
            </div>
          </button>
        );
      })}
    </div>
  );
}
