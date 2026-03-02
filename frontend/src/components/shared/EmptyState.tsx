/**
 * Empty State
 * Generic empty state placeholder for lists/sections with no data.
 */

import type { LucideIcon } from 'lucide-react';
import { Inbox } from 'lucide-react';
import { cn } from '../../lib/utils';

interface EmptyStateProps {
  icon?: LucideIcon;
  title: string;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
  compact?: boolean;
  className?: string;
}

export function EmptyState({
  icon: Icon = Inbox,
  title,
  description,
  action,
  compact = false,
  className,
}: EmptyStateProps) {
  return (
    <div
      className={cn(
        'flex flex-col items-center justify-center gap-3 text-center',
        compact ? 'py-6' : 'py-12',
        className
      )}
    >
      <Icon
        className={cn(
          'text-surface-300 dark:text-surface-600',
          compact ? 'w-8 h-8' : 'w-12 h-12'
        )}
      />
      <div className="space-y-1">
        <p
          className={cn(
            'font-medium text-surface-500 dark:text-surface-400',
            compact ? 'text-sm' : 'text-base'
          )}
        >
          {title}
        </p>
        {description && (
          <p className="text-sm text-surface-400 dark:text-surface-500 max-w-xs">
            {description}
          </p>
        )}
      </div>
      {action && (
        <button
          onClick={action.onClick}
          className="mt-1 text-sm font-medium text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 transition-colors"
        >
          {action.label}
        </button>
      )}
    </div>
  );
}
