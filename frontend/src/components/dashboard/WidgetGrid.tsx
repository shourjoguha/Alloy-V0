/**
 * WidgetGrid
 * Renders the dashboard widget grid from the persisted layout.
 * Each widget is lazily loaded and wrapped in an ErrorBoundary.
 */

import { Suspense } from 'react';
import { Plus } from 'lucide-react';
import { useAppStore } from '../../stores/app.store';
import { useUIStore } from '../../stores/ui.store';
import { WIDGET_REGISTRY } from './widgets/WidgetRegistry';
import { ErrorBoundary } from '../shared/ErrorBoundary';
import { cn } from '../../lib/utils';

export function WidgetGrid() {
  const dashboardLayout = useAppStore((s) => s.dashboardLayout);
  const openModal = useUIStore((s) => s.openModal);

  return (
    <div className="space-y-4">
      {/* Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {dashboardLayout.map((widgetId) => {
          const def = WIDGET_REGISTRY[widgetId];
          if (!def) return null;

          const WidgetComponent = def.component;

          return (
            <div
              key={widgetId}
              className={cn(
                def.defaultSize === 'lg' && 'sm:col-span-2'
              )}
            >
              <ErrorBoundary scope={`Widget:${def.name}`}>
                <Suspense fallback={<WidgetLoadingFallback title={def.name} />}>
                  <WidgetComponent />
                </Suspense>
              </ErrorBoundary>
            </div>
          );
        })}
      </div>

      {/* Add Widget button */}
      <button
        type="button"
        onClick={() => openModal('add-widget')}
        className="w-full flex items-center justify-center gap-2 py-3 rounded-2xl border-2 border-dashed border-surface-200 dark:border-surface-700 text-sm text-surface-400 hover:border-primary-300 hover:text-primary-500 dark:hover:border-primary-700 dark:hover:text-primary-400 transition-colors"
      >
        <Plus className="w-4 h-4" />
        Add widget
      </button>
    </div>
  );
}

/** Shown while the lazy widget bundle is loading */
function WidgetLoadingFallback({ title }: { title: string }) {
  return (
    <div className="bg-white dark:bg-surface-900 rounded-2xl border border-surface-100 dark:border-surface-800">
      <div className="flex items-center justify-between px-4 py-3 border-b border-surface-100 dark:border-surface-800">
        <div className="h-3.5 w-24 skeleton rounded-full" />
        <span className="sr-only">{title}</span>
      </div>
      <div className="p-4 h-[220px]">
        <div className="h-full skeleton rounded-xl" />
      </div>
    </div>
  );
}
