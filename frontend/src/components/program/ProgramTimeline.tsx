/**
 * ProgramTimeline
 * Vertical timeline of training blocks with expandable week views.
 */

import { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn, formatDuration } from '../../lib/utils';
import { WeekView } from './WeekView';
import type { ProgramSkeleton } from '../../types/program';

interface ProgramTimelineProps {
  program: ProgramSkeleton;
  onSessionClick?: (sessionId: string) => void;
}

export function ProgramTimeline({ program, onSessionClick }: ProgramTimelineProps) {
  const [expandedBlocks, setExpandedBlocks] = useState<Set<number>>(
    new Set([1]) // expand block 1 by default
  );

  function toggleBlock(blockNum: number) {
    setExpandedBlocks((prev) => {
      const next = new Set(prev);
      if (next.has(blockNum)) {
        next.delete(blockNum);
      } else {
        next.add(blockNum);
      }
      return next;
    });
  }

  return (
    <div className="space-y-4">
      {program.training_blocks.map((block) => {
        const isExpanded = expandedBlocks.has(block.block_number);
        const totalTime = block.weekly_plans.reduce(
          (sum, w) => sum + w.total_training_time,
          0
        );

        return (
          <div
            key={block.block_number}
            className="bg-white dark:bg-surface-900 rounded-2xl border border-surface-100 dark:border-surface-800 overflow-hidden"
          >
            {/* Block header */}
            <button
              type="button"
              onClick={() => toggleBlock(block.block_number)}
              className="w-full flex items-center justify-between px-5 py-4 text-left"
            >
              <div>
                <div className="flex items-center gap-2 mb-0.5">
                  <span className="flex items-center justify-center w-5 h-5 rounded-full bg-primary-100 dark:bg-primary-900/40 text-xs font-bold text-primary-700 dark:text-primary-300">
                    {block.block_number}
                  </span>
                  <h3 className="text-sm font-semibold text-surface-800 dark:text-surface-200">
                    {block.block_name}
                  </h3>
                </div>
                <p className="text-xs text-surface-400 capitalize">
                  {block.primary_goal} · {block.weeks_duration}w ·{' '}
                  {formatDuration(totalTime)} total
                </p>
              </div>

              <ChevronDown
                className={cn(
                  'w-4 h-4 text-surface-400 transition-transform shrink-0',
                  isExpanded && 'rotate-180'
                )}
              />
            </button>

            {/* Week views */}
            <AnimatePresence>
              {isExpanded && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.2, ease: 'easeInOut' }}
                  className="overflow-hidden"
                >
                  <div className="px-5 pb-5 space-y-6 border-t border-surface-100 dark:border-surface-800 pt-4">
                    {block.weekly_plans.map((week) => (
                      <WeekView
                        key={week.week_number}
                        plan={week}
                        onSessionClick={onSessionClick}
                      />
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        );
      })}
    </div>
  );
}
