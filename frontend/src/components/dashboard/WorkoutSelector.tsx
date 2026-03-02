/**
 * WorkoutSelector
 * Large amber CTA: "Select a Workout" that expands to show DayPills.
 * When a day is selected, changes to "Start {Day Name}".
 */

import { Play, ChevronRight, ChevronDown } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useUIStore } from '../../stores/ui.store';
import { DayPills } from './DayPills';
import { cn, capitalise } from '../../lib/utils';
import type { SessionSkeleton } from '../../types/program';

interface WorkoutSelectorProps {
  sessions: SessionSkeleton[];
  className?: string;
}

export function WorkoutSelector({ sessions, className }: WorkoutSelectorProps) {
  const expanded = useUIStore((s) => s.workoutSelectorExpanded);
  const toggleExpanded = useUIStore((s) => s.toggleWorkoutSelector);
  const selectedDay = useUIStore((s) => s.selectedDayIndex);

  const selectedSession = selectedDay !== null ? sessions[selectedDay] : null;
  const label = selectedSession
    ? `Start ${capitalise(selectedSession.session_focus)}`
    : 'Select a Workout';

  return (
    <div className={cn('space-y-2', className)}>
      {/* Main CTA button */}
      <button
        type="button"
        onClick={toggleExpanded}
        className={cn(
          'w-full flex items-center justify-center gap-3 py-4 rounded-xl',
          'font-semibold text-base transition-all',
          'bg-amber-accent hover:bg-amber-accent-hover text-surface-950',
          'shadow-[0_4px_0_0_rgba(0,0,0,0.15)] active:shadow-none active:translate-y-[2px]',
          selectedSession && 'bg-emerald-500 hover:bg-emerald-600'
        )}
      >
        <Play className="w-4 h-4" />
        <span>{label}</span>
        {expanded ? (
          <ChevronDown className="w-4 h-4" />
        ) : (
          <ChevronRight className="w-4 h-4" />
        )}
      </button>

      {/* Expandable day pills */}
      <AnimatePresence>
        {expanded && sessions.length > 0 && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2, ease: 'easeInOut' }}
            className="overflow-hidden"
          >
            <DayPills sessions={sessions} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
