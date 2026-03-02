/**
 * ActionRow
 * Two primary action buttons (Adapt Session, New Program) plus utility icon buttons.
 * Responsive: wraps on small screens.
 */

import { useNavigate } from '@tanstack/react-router';
import { MessageSquare, RefreshCw } from 'lucide-react';
import { cn } from '../../lib/utils';

interface ActionRowProps {
  className?: string;
}

export function ActionRow({ className }: ActionRowProps) {
  const navigate = useNavigate();

  return (
    <div className={cn('flex flex-wrap items-center gap-2', className)}>
      {/* Adapt Session (placeholder) */}
      <button
        type="button"
        className={cn(
          'flex-1 min-w-[140px] flex items-center justify-center gap-2 py-2.5 rounded-xl',
          'text-sm font-medium transition-colors',
          'bg-white dark:bg-surface-900 border border-surface-200 dark:border-surface-700',
          'text-surface-600 dark:text-surface-400',
          'hover:bg-surface-50 dark:hover:bg-surface-800'
        )}
      >
        <MessageSquare className="w-4 h-4" />
        <span>Adapt Session</span>
      </button>

      {/* New Program */}
      <button
        type="button"
        onClick={() => navigate({ to: '/onboarding' })}
        className={cn(
          'flex-1 min-w-[140px] flex items-center justify-center gap-2 py-2.5 rounded-xl',
          'text-sm font-medium transition-colors',
          'bg-white dark:bg-surface-900 border border-surface-200 dark:border-surface-700',
          'text-surface-600 dark:text-surface-400',
          'hover:bg-surface-50 dark:hover:bg-surface-800'
        )}
      >
        <RefreshCw className="w-4 h-4" />
        <span>New Program</span>
      </button>
    </div>
  );
}
