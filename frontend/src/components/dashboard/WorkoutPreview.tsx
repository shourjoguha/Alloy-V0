/**
 * WorkoutPreview
 * Shows the selected day's workout detail: title, focus, total duration,
 * and all blocks (Warm-Up, Main Training, Conditioning) inline within
 * a single card. Sections are differentiated by typography and subtle dividers.
 */

import { Clock } from 'lucide-react';
import { cn, formatDuration, toTitleCase } from '../../lib/utils';
import { Card } from '../ui/card';
import type { SessionSkeleton, SessionBlock } from '../../types/program';

interface WorkoutPreviewProps {
  session: SessionSkeleton;
  className?: string;
}

const BLOCK_TYPE_LABELS: Record<string, string> = {
  warmup: 'Warm-Up',
  main: 'Main Training',
  cooldown: 'Cool-Down',
};

export function WorkoutPreview({ session, className }: WorkoutPreviewProps) {
  return (
    <Card className={cn('p-5 animate-slide-up', className)}>
      {/* Header */}
      <div className="flex items-start justify-between gap-3 mb-5">
        <div>
          <h3 className="text-lg font-semibold text-surface-800 dark:text-surface-200 capitalize">
            {session.session_focus}
          </h3>
          <p className="text-xs text-surface-400 mt-0.5 capitalize">
            {session.session_type.replace(/_/g, ' ')}
          </p>
        </div>
        <div className="flex items-center gap-1.5 text-sm text-surface-400 shrink-0">
          <Clock className="w-3.5 h-3.5" />
          {formatDuration(session.total_duration_minutes)}
        </div>
      </div>

      {/* All blocks rendered inline */}
      <div className="space-y-0">
        {session.blocks.map((block, idx) => (
          <BlockSection
            key={`${block.block_type}-${idx}`}
            block={block}
            isLast={idx === session.blocks.length - 1}
          />
        ))}
      </div>
    </Card>
  );
}

// ─── Block Section (flat, no accordion) ─────────────────────────────────────

interface BlockSectionProps {
  block: SessionBlock;
  isLast: boolean;
}

function BlockSection({ block, isLast }: BlockSectionProps) {
  const label = BLOCK_TYPE_LABELS[block.block_type] ?? toTitleCase(block.block_type);
  const isMain = block.block_type === 'main';

  return (
    <div className={cn(!isLast && 'pb-4 mb-4 border-b border-surface-100 dark:border-surface-800/60')}>
      {/* Section header */}
      <div className="flex items-center justify-between mb-2">
        <h4 className={cn(
          'text-xs font-semibold uppercase tracking-wider',
          isMain
            ? 'text-amber-accent'
            : 'text-surface-400 dark:text-surface-500'
        )}>
          {label}
        </h4>
        <span className="text-xs text-surface-400">
          {formatDuration(block.duration_minutes)}
        </span>
      </div>

      {/* Movements list */}
      {block.movements && block.movements.length > 0 ? (
        <div className="space-y-1">
          {block.movements.map((movement, mIdx) => (
            <div
              key={mIdx}
              className="flex items-center justify-between py-1.5"
            >
              <div className="min-w-0">
                <p className={cn(
                  'truncate',
                  isMain
                    ? 'text-sm font-medium text-surface-800 dark:text-surface-200'
                    : 'text-sm text-surface-600 dark:text-surface-400'
                )}>
                  {movement.movement_name}
                </p>
              </div>
              <div className="text-right shrink-0 ml-3">
                <p className={cn(
                  'text-xs',
                  isMain
                    ? 'font-medium text-surface-700 dark:text-surface-300'
                    : 'text-surface-400'
                )}>
                  {movement.sets} × {movement.reps}
                  {movement.rpe != null && (
                    <span className="text-surface-400 ml-1">@ RPE {movement.rpe}</span>
                  )}
                </p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className={cn(
          'text-xs py-1',
          isMain ? 'text-surface-400' : 'text-surface-300 dark:text-surface-600'
        )}>
          No movements populated yet
        </p>
      )}
    </div>
  );
}
