/**
 * Error Fallback
 * Branded fallback UI for ErrorBoundary.
 * Also used as a standalone component for widget-level errors.
 */

import { AlertTriangle, RefreshCw } from 'lucide-react';
import { cn } from '../../lib/utils';

interface ErrorFallbackProps {
  error?: Error | null;
  onReset?: () => void;
  /** Compact variant for widget containers */
  compact?: boolean;
  scope?: string;
}

export function ErrorFallback({
  error,
  onReset,
  compact = false,
  scope,
}: ErrorFallbackProps) {
  const IS_DEV = import.meta.env.DEV;

  return (
    <div
      className={cn(
        'flex flex-col items-center justify-center gap-3 rounded-xl border border-error/20 bg-error/5 text-center',
        compact ? 'p-4 min-h-[120px]' : 'p-8 min-h-[240px]'
      )}
    >
      <AlertTriangle
        className={cn(
          'text-error',
          compact ? 'w-6 h-6' : 'w-10 h-10'
        )}
      />

      <div className="space-y-1">
        <p
          className={cn(
            'font-semibold text-surface-700 dark:text-surface-200',
            compact ? 'text-sm' : 'text-base'
          )}
        >
          {scope ? `${scope} failed to load` : 'Something went wrong'}
        </p>
        {!compact && (
          <p className="text-sm text-surface-400">
            An unexpected error occurred. You can try refreshing this section.
          </p>
        )}
        {IS_DEV && error?.message && (
          <p className="mt-2 font-mono text-xs text-error/70 max-w-xs break-all">
            {error.message}
          </p>
        )}
      </div>

      {onReset && (
        <button
          onClick={onReset}
          className={cn(
            'flex items-center gap-2 rounded-lg border border-surface-200 dark:border-surface-700',
            'px-3 py-1.5 text-sm font-medium text-surface-600 dark:text-surface-300',
            'hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors',
            compact ? 'text-xs px-2 py-1' : ''
          )}
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Try again
        </button>
      )}
    </div>
  );
}
