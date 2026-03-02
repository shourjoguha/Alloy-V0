/**
 * WidgetWrapper
 * Shared container for all dashboard widgets.
 * Handles: loading skeleton, localized error state, remove button.
 */

import { X, RefreshCw, AlertCircle } from 'lucide-react';
import type { ReactNode } from 'react';
import { useAppStore } from '../../../stores/app.store';

interface WidgetWrapperProps {
  id: string;
  title: string;
  loading?: boolean;
  error?: string | null;
  onRetry?: () => void;
  children: ReactNode;
}

export function WidgetWrapper({
  id,
  title,
  loading = false,
  error = null,
  onRetry,
  children,
}: WidgetWrapperProps) {
  const dashboardLayout = useAppStore((s) => s.dashboardLayout);
  const setDashboardLayout = useAppStore((s) => s.setDashboardLayout);

  function removeWidget() {
    setDashboardLayout(dashboardLayout.filter((wId) => wId !== id));
  }

  return (
    <div className="bg-white dark:bg-surface-900 rounded-2xl border border-surface-100 dark:border-surface-800 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-surface-100 dark:border-surface-800">
        <h3 className="text-sm font-semibold text-surface-700 dark:text-surface-300">
          {title}
        </h3>
        <button
          type="button"
          onClick={removeWidget}
          className="flex items-center justify-center w-7 h-7 rounded-lg text-surface-400 hover:text-surface-600 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
          aria-label={`Remove ${title} widget`}
        >
          <X className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Body */}
      <div className="flex-1 p-4 h-[220px]">
        {loading ? (
          <WidgetSkeleton />
        ) : error ? (
          <WidgetError message={error} onRetry={onRetry} />
        ) : (
          children
        )}
      </div>
    </div>
  );
}

function WidgetSkeleton() {
  return (
    <div className="h-full flex flex-col gap-3 animate-pulse">
      <div className="h-3 bg-surface-100 dark:bg-surface-800 rounded-full w-2/3" />
      <div className="flex-1 bg-surface-100 dark:bg-surface-800 rounded-xl" />
    </div>
  );
}

function WidgetError({
  message,
  onRetry,
}: {
  message: string;
  onRetry?: () => void;
}) {
  return (
    <div className="h-full flex flex-col items-center justify-center gap-3 text-center">
      <AlertCircle className="w-8 h-8 text-surface-300 dark:text-surface-600" />
      <p className="text-xs text-surface-400 max-w-[160px] leading-relaxed">{message}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="flex items-center gap-1.5 text-xs text-primary-600 dark:text-primary-400 hover:underline"
        >
          <RefreshCw className="w-3 h-3" />
          Retry
        </button>
      )}
    </div>
  );
}
