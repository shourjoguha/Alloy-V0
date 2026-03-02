/**
 * BottomNav
 * Mobile-only bottom tab navigation.
 * Context-aware:
 *   Dashboard: Personal / Teams tabs with dot indicators
 *   Other pages: standard nav items
 */

import { Link, useRouterState } from '@tanstack/react-router';
import { User, Users } from 'lucide-react';
import { NAV_ITEMS } from '../../config/navigation.config';
import { useUIStore } from '../../stores/ui.store';
import { cn } from '../../lib/utils';

function useIsDashboard(): boolean {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  return pathname === '/dashboard' || pathname === '/';
}

export function BottomNav() {
  const location = useRouterState({ select: (s) => s.location });
  const isDashboard = useIsDashboard();
  const selectedTab = useUIStore((s) => s.selectedDashboardTab);
  const setTab = useUIStore((s) => s.setSelectedDashboardTab);
  const items = NAV_ITEMS.filter((item) => item.showInBottomNav);

  if (isDashboard) {
    return (
      <nav
        className={cn(
        'fixed bottom-0 left-0 right-0 z-30',
          'bg-white dark:bg-surface-950 border-t border-surface-200 dark:border-surface-800',
          'flex items-center justify-center h-16 safe-area-pb gap-8'
        )}
      >
        {/* Personal tab */}
        <button
          type="button"
          onClick={() => setTab('personal')}
          className={cn(
            'flex flex-col items-center justify-center gap-1 py-2 px-6 rounded-xl transition-colors',
            selectedTab === 'personal'
              ? 'bg-amber-accent-muted text-amber-accent'
              : 'text-surface-400 dark:text-surface-600 hover:text-surface-700 dark:hover:text-surface-300'
          )}
        >
          <User className="w-5 h-5" />
          <span className="text-xs font-medium">Personal</span>
        </button>

        {/* Dot indicators */}
        <div className="flex items-center gap-1.5">
          <div className={cn(
            'w-1.5 h-1.5 rounded-full transition-colors',
            selectedTab === 'personal' ? 'bg-amber-accent' : 'bg-surface-300 dark:bg-surface-600'
          )} />
          <div className={cn(
            'w-1.5 h-1.5 rounded-full transition-colors',
            selectedTab === 'squads' ? 'bg-amber-accent' : 'bg-surface-300 dark:bg-surface-600'
          )} />
        </div>

        {/* Squads tab */}
        <button
          type="button"
          onClick={() => setTab('squads')}
          className={cn(
            'flex flex-col items-center justify-center gap-1 py-2 px-6 rounded-xl transition-colors',
            selectedTab === 'squads'
              ? 'bg-amber-accent-muted text-amber-accent'
              : 'text-surface-400 dark:text-surface-600 hover:text-surface-700 dark:hover:text-surface-300'
          )}
        >
          <Users className="w-5 h-5" />
          <span className="text-xs font-medium">Squads</span>
        </button>
      </nav>
    );
  }

  return (
    <nav
      className={cn(
        'fixed bottom-0 left-0 right-0 z-30',
        'bg-white dark:bg-surface-950 border-t border-surface-200 dark:border-surface-800',
        'flex items-stretch h-16 safe-area-pb'
      )}
    >
      {items.map((item) => {
        const Icon = item.icon;
        const isActive = location.pathname.startsWith(item.path);

        return (
          <Link
            key={item.path}
            to={item.path}
            className={cn(
              'flex flex-1 flex-col items-center justify-center gap-1 py-2',
              'text-xs font-medium transition-colors',
              'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-primary-500',
              isActive
                ? 'text-primary-600 dark:text-primary-400'
                : 'text-surface-400 dark:text-surface-600 hover:text-surface-700 dark:hover:text-surface-300'
            )}
          >
            <Icon
              className={cn(
                'w-5 h-5 transition-transform',
                isActive && 'scale-110'
              )}
            />
            <span>{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
