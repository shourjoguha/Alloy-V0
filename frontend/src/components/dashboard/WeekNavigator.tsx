/**
 * WeekNavigator
 * Shows "Week N · {phase}" with left/right arrows to cycle through weeks.
 * Reads from activeProgram in app store, controlled via selectedWeekIndex in UI store.
 */

import { ChevronLeft, ChevronRight } from 'lucide-react';
import { useUIStore } from '../../stores/ui.store';
import { cn } from '../../lib/utils';
import type { ProgramSkeleton } from '../../types/program';

interface WeekNavigatorProps {
  program: ProgramSkeleton;
  className?: string;
}

/** Flatten all weekly plans across training blocks into a single indexed list */
function flattenWeeks(program: ProgramSkeleton) {
  const weeks: { weekNumber: number; blockName: string; focus: string }[] = [];
  for (const block of program.training_blocks) {
    for (const week of block.weekly_plans) {
      weeks.push({
        weekNumber: week.week_number,
        blockName: block.block_name,
        focus: week.weekly_focus,
      });
    }
  }
  return weeks;
}

export function WeekNavigator({ program, className }: WeekNavigatorProps) {
  const selectedIndex = useUIStore((s) => s.selectedWeekIndex);
  const setIndex = useUIStore((s) => s.setSelectedWeekIndex);
  const weeks = flattenWeeks(program);
  const current = weeks[selectedIndex];
  const canGoBack = selectedIndex > 0;
  const canGoForward = selectedIndex < weeks.length - 1;

  if (!current) return null;

  return (
    <div
      className={cn(
        'flex items-center justify-between px-4 py-3',
        'bg-white dark:bg-surface-900 rounded-xl',
        'border border-surface-200 dark:border-surface-800',
        className
      )}
    >
      <button
        type="button"
        onClick={() => canGoBack && setIndex(selectedIndex - 1)}
        disabled={!canGoBack}
        className={cn(
          'p-1.5 rounded-lg transition-colors',
          canGoBack
            ? 'text-surface-500 hover:text-surface-700 dark:hover:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-800'
            : 'text-surface-200 dark:text-surface-700 cursor-not-allowed'
        )}
        aria-label="Previous week"
      >
        <ChevronLeft className="w-4 h-4" />
      </button>

      <div className="text-center min-w-0">
        <span className="text-sm font-semibold text-surface-800 dark:text-surface-200">
          Week {current.weekNumber}
        </span>
        <span className="text-sm text-surface-400 ml-2 capitalize">
          {current.blockName}
        </span>
      </div>

      <button
        type="button"
        onClick={() => canGoForward && setIndex(selectedIndex + 1)}
        disabled={!canGoForward}
        className={cn(
          'p-1.5 rounded-lg transition-colors',
          canGoForward
            ? 'text-surface-500 hover:text-surface-700 dark:hover:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-800'
            : 'text-surface-200 dark:text-surface-700 cursor-not-allowed'
        )}
        aria-label="Next week"
      >
        <ChevronRight className="w-4 h-4" />
      </button>
    </div>
  );
}
