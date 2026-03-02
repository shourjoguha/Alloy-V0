/**
 * /workout/:sessionId — Session detail view with block breakdown
 */

import { createFileRoute, useNavigate } from '@tanstack/react-router';
import { ArrowLeft, Clock, Target, ChevronDown } from 'lucide-react';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { PageContainer } from '../../../components/layout/PageContainer';
import { ErrorBoundary } from '../../../components/shared/ErrorBoundary';
import { EmptyState } from '../../../components/shared/EmptyState';
import { cn, formatDuration } from '../../../lib/utils';
import { BlockType } from '../../../types/enums';
import type { SessionSkeleton } from '../../../types/program';
import { useAppStore } from '../../../stores/app.store';

export const Route = createFileRoute('/_app/workout/$sessionId')({
  component: () => (
    <ErrorBoundary scope="WorkoutDetail">
      <WorkoutDetailPage />
    </ErrorBoundary>
  ),
});

/** Find a session by ID across all training blocks and weekly plans */
function findSessionById(programBlocks: { weekly_plans: { sessions: SessionSkeleton[] }[] }[], id: string): SessionSkeleton | undefined {
  for (const block of programBlocks) {
    for (const week of block.weekly_plans) {
      const match = week.sessions.find((s) => s.session_id === id);
      if (match) return match;
    }
  }
  return undefined;
}

const BLOCK_LABELS: Record<string, string> = {
  [BlockType.WARMUP]: 'Warm-up',
  [BlockType.MAIN]: 'Main Work',
  [BlockType.COOLDOWN]: 'Cool-down',
};

const BLOCK_COLORS: Record<string, string> = {
  [BlockType.WARMUP]: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400',
  [BlockType.MAIN]:
    'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-400',
  [BlockType.COOLDOWN]:
    'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400',
};

function WorkoutDetailPage() {
  const { sessionId } = Route.useParams();
  const navigate = useNavigate();
  const activeProgram = useAppStore((s) => s.activeProgram);
  const [expandedBlocks, setExpandedBlocks] = useState<Set<string>>(
    new Set([BlockType.MAIN])
  );

  const session = activeProgram
    ? findSessionById(activeProgram.training_blocks, sessionId)
    : undefined;

  if (!session) {
    return (
      <PageContainer>
        <button
          type="button"
          onClick={() => navigate({ to: '/program' })}
          className="flex items-center gap-2 text-sm text-surface-500 hover:text-surface-700 dark:hover:text-surface-300 mb-5 -ml-1"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to program
        </button>
        <EmptyState
          icon={Target}
          title="Session not found"
          description="This workout session doesn't exist in your current program."
          action={{
            label: 'Back to program',
            onClick: () => navigate({ to: '/program' }),
          }}
        />
      </PageContainer>
    );
  }

  function toggleBlock(blockType: string) {
    setExpandedBlocks((prev) => {
      const next = new Set(prev);
      if (next.has(blockType)) next.delete(blockType);
      else next.add(blockType);
      return next;
    });
  }

  return (
    <PageContainer>
      {/* Back nav */}
      <button
        type="button"
        onClick={() => navigate({ to: '/program' })}
        className="flex items-center gap-2 text-sm text-surface-500 hover:text-surface-700 dark:hover:text-surface-300 mb-5 -ml-1"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to program
      </button>

      {/* Session header */}
      <div className="mb-6">
        <h1 className="text-lg font-semibold text-surface-900 dark:text-surface-50 capitalize">
          {session.session_focus}
        </h1>
        <div className="flex items-center gap-4 mt-1.5">
          <span className="flex items-center gap-1.5 text-xs text-surface-500">
            <Clock className="w-3.5 h-3.5" />
            {formatDuration(session.total_duration_minutes)}
          </span>
          <span className="flex items-center gap-1.5 text-xs text-surface-500">
            <Target className="w-3.5 h-3.5" />
            {session.blocks.length} blocks
          </span>
          <span className="text-xs px-2 py-0.5 rounded-full bg-surface-100 dark:bg-surface-800 text-surface-500 capitalize">
            {session.difficulty_level}
          </span>
        </div>
      </div>

      {/* Blocks */}
      <div className="space-y-3">
        {session.blocks.map((block, idx) => {
          const isExpanded = expandedBlocks.has(block.block_type);
          const colorClass =
            BLOCK_COLORS[block.block_type] ??
            'bg-surface-100 text-surface-600 dark:bg-surface-800 dark:text-surface-400';

          return (
            <div
              key={`${block.block_type}-${idx}`}
              className="bg-white dark:bg-surface-900 rounded-2xl border border-surface-100 dark:border-surface-800 overflow-hidden"
            >
              <button
                type="button"
                onClick={() => toggleBlock(block.block_type)}
                className="w-full flex items-center justify-between px-5 py-4"
              >
                <div className="flex items-center gap-3">
                  <span className={cn('text-xs font-medium px-2.5 py-1 rounded-full', colorClass)}>
                    {BLOCK_LABELS[block.block_type] ?? block.block_type}
                  </span>
                  <span className="text-xs text-surface-400">
                    {formatDuration(block.duration_minutes)}
                  </span>
                </div>
                <ChevronDown
                  className={cn(
                    'w-4 h-4 text-surface-400 transition-transform',
                    isExpanded && 'rotate-180'
                  )}
                />
              </button>

              <AnimatePresence>
                {isExpanded && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.15, ease: 'easeInOut' }}
                    className="overflow-hidden"
                  >
                    <div className="px-5 pb-4 border-t border-surface-100 dark:border-surface-800 pt-3 space-y-3">
                      {/* Sets/reps if main block */}
                      {block.target_sets && (
                        <div className="flex gap-4">
                          <div className="text-center">
                            <p className="text-lg font-bold text-surface-800 dark:text-surface-200">
                              {block.target_sets}
                            </p>
                            <p className="text-xs text-surface-400">sets</p>
                          </div>
                          {block.target_reps && (
                            <div className="text-center">
                              <p className="text-lg font-bold text-surface-800 dark:text-surface-200">
                                {block.target_reps}
                              </p>
                              <p className="text-xs text-surface-400">reps</p>
                            </div>
                          )}
                          {block.target_rest_seconds && (
                            <div className="text-center">
                              <p className="text-lg font-bold text-surface-800 dark:text-surface-200">
                                {block.target_rest_seconds}s
                              </p>
                              <p className="text-xs text-surface-400">rest</p>
                            </div>
                          )}
                        </div>
                      )}

                      {/* Notes */}
                      {block.notes && (
                        <p className="text-xs text-surface-500 dark:text-surface-400 leading-relaxed">
                          {block.notes}
                        </p>
                      )}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          );
        })}
      </div>
    </PageContainer>
  );
}
