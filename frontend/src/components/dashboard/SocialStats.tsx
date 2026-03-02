/**
 * SocialStats
 * Card showing "Workouts Shared" count + "Top collaborators" avatar row.
 * Placeholder data for now — will connect to backend later.
 */

import { cn } from '../../lib/utils';
import { Card } from '../ui/card';

interface SocialStatsProps {
  sharedCount?: number;
  collaborators?: { initials: string; color: string }[];
  className?: string;
}

const DEFAULT_COLLABORATORS = [
  { initials: 'SH', color: 'bg-fuchsia-500' },
];

export function SocialStats({
  sharedCount = 1,
  collaborators = DEFAULT_COLLABORATORS,
  className,
}: SocialStatsProps) {
  return (
    <Card variant="grouped" className={cn('p-5 text-center', className)}>
      <div className="text-2xl font-bold text-amber-accent">
        {sharedCount}
      </div>
      <div className="text-xs text-surface-400 dark:text-surface-500 mt-1">
        Workouts Shared
      </div>

      {/* Collaborator avatars */}
      <div className="flex items-center justify-center gap-2 mt-3">
        {collaborators.map((c, idx) => (
          <div
            key={idx}
            className={cn(
              'w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white',
              c.color
            )}
          >
            {c.initials}
          </div>
        ))}
      </div>
      <p className="text-xs text-surface-400 dark:text-surface-500 mt-1.5">
        Top collaborators
      </p>
    </Card>
  );
}
