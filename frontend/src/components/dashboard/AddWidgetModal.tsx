/**
 * AddWidgetModal
 * Dialog to add or remove widgets from the dashboard.
 * Uses Radix Dialog; controlled by useUIStore.
 */

import * as Dialog from '@radix-ui/react-dialog';
import { X, Check, Plus } from 'lucide-react';
import { useUIStore } from '../../stores/ui.store';
import { useAppStore } from '../../stores/app.store';
import { WIDGET_REGISTRY, ALL_WIDGET_IDS } from './widgets/WidgetRegistry';
import { cn } from '../../lib/utils';

export function AddWidgetModal() {
  const activeModal = useUIStore((s) => s.activeModal);
  const closeModal = useUIStore((s) => s.closeModal);

  const dashboardLayout = useAppStore((s) => s.dashboardLayout);
  const setDashboardLayout = useAppStore((s) => s.setDashboardLayout);

  const isOpen = activeModal === 'add-widget';

  function toggleWidget(id: string) {
    if (dashboardLayout.includes(id)) {
      setDashboardLayout(dashboardLayout.filter((wId) => wId !== id));
    } else {
      setDashboardLayout([...dashboardLayout, id]);
    }
  }

  return (
    <Dialog.Root open={isOpen} onOpenChange={(open) => !open && closeModal()}>
      <Dialog.Portal>
        {/* Overlay */}
        <Dialog.Overlay className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />

        {/* Content */}
        <Dialog.Content className="fixed left-1/2 top-1/2 z-50 -translate-x-1/2 -translate-y-1/2 w-full max-w-sm max-h-[80vh] bg-white dark:bg-surface-900 rounded-2xl shadow-xl border border-surface-100 dark:border-surface-800 flex flex-col data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95">
          {/* Header */}
          <div className="flex items-center justify-between px-5 py-4 border-b border-surface-100 dark:border-surface-800 shrink-0">
            <Dialog.Title className="text-sm font-semibold text-surface-800 dark:text-surface-200">
              Manage Widgets
            </Dialog.Title>
            <Dialog.Close asChild>
              <button
                type="button"
                className="flex items-center justify-center w-7 h-7 rounded-lg text-surface-400 hover:text-surface-600 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
                aria-label="Close"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </Dialog.Close>
          </div>

          {/* Widget list */}
          <div className="flex-1 overflow-y-auto p-3 space-y-2">
            {ALL_WIDGET_IDS.map((id) => {
              const def = WIDGET_REGISTRY[id];
              if (!def) return null;

              const isAdded = dashboardLayout.includes(id);

              return (
                <button
                  key={id}
                  type="button"
                  onClick={() => toggleWidget(id)}
                  className={cn(
                    'w-full flex items-center gap-3 p-3 rounded-xl text-left transition-all border',
                    isAdded
                      ? 'bg-primary-50 border-primary-200 dark:bg-primary-900/20 dark:border-primary-800'
                      : 'bg-surface-50 dark:bg-surface-800/50 border-surface-100 dark:border-surface-800 hover:border-surface-200 dark:hover:border-surface-700'
                  )}
                >
                  {/* Status icon */}
                  <div
                    className={cn(
                      'flex-shrink-0 flex items-center justify-center w-7 h-7 rounded-full border-2',
                      isAdded
                        ? 'bg-primary-600 border-primary-600'
                        : 'bg-white dark:bg-surface-900 border-surface-200 dark:border-surface-700'
                    )}
                  >
                    {isAdded ? (
                      <Check className="w-3.5 h-3.5 text-white" />
                    ) : (
                      <Plus className="w-3.5 h-3.5 text-surface-400" />
                    )}
                  </div>

                  {/* Widget info */}
                  <div className="flex-1 min-w-0">
                    <p
                      className={cn(
                        'text-sm font-medium',
                        isAdded
                          ? 'text-primary-700 dark:text-primary-300'
                          : 'text-surface-700 dark:text-surface-300'
                      )}
                    >
                      {def.name}
                    </p>
                    <p className="text-xs text-surface-400 dark:text-surface-500 mt-0.5 leading-snug">
                      {def.description}
                    </p>
                  </div>
                </button>
              );
            })}
          </div>

          {/* Footer */}
          <div className="px-5 py-4 border-t border-surface-100 dark:border-surface-800 shrink-0">
            <Dialog.Close asChild>
              <button
                type="button"
                className="w-full py-2 rounded-xl bg-primary-600 hover:bg-primary-700 text-white text-sm font-semibold transition-colors"
              >
                Done
              </button>
            </Dialog.Close>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
