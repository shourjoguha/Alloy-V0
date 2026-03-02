/**
 * BottomNav
 * Mobile-only bottom tab navigation.
 * Renders items where showInBottomNav === true.
 */

import { Link, useRouterState } from '@tanstack/react-router';
import { NAV_ITEMS } from '../../config/navigation.config';
import { cn } from '../../lib/utils';

export function BottomNav() {
  const location = useRouterState({ select: (s) => s.location });
  const items = NAV_ITEMS.filter((item) => item.showInBottomNav);

  return (
    <nav
      className={cn(
        'md:hidden fixed bottom-0 left-0 right-0 z-30',
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
