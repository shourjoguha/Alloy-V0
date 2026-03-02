/**
 * Loading Spinner
 * Used for component-level and page-level loading states.
 */

import { cn } from '../../lib/utils';

interface LoadingSpinnerProps {
  /** Size variant */
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function LoadingSpinner({ size = 'md', className }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-4 h-4 border-2',
    md: 'w-6 h-6 border-2',
    lg: 'w-10 h-10 border-3',
  };

  return (
    <div
      role="status"
      aria-label="Loading"
      className={cn(
        'rounded-full border-surface-200 border-t-primary-500 animate-spin',
        sizeClasses[size],
        className
      )}
    />
  );
}

/** Full-page loading overlay — used during route transitions */
export function PageLoader() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-surface-50 dark:bg-surface-950">
      <div className="flex flex-col items-center gap-3">
        <LoadingSpinner size="lg" />
        <p className="text-sm text-surface-400">Loading...</p>
      </div>
    </div>
  );
}
