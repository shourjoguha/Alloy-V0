/**
 * TopNav
 * Top header bar. Context-aware:
 *   Dashboard: "{user}'s Dashboard" + notification bell + hamburger menu
 *   Other pages: page title + settings
 */

import { useRouterState } from '@tanstack/react-router';
import { Zap, Bell, Menu, Settings } from 'lucide-react';
import { Link } from '@tanstack/react-router';
import { NAV_ITEMS } from '../../config/navigation.config';
import { HamburgerMenu } from './HamburgerMenu';
import { useUIStore } from '../../stores/ui.store';
import { cn } from '../../lib/utils';

function useIsDashboard(): boolean {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  return pathname === '/dashboard' || pathname === '/';
}

/** Derive a page title from the current pathname */
function usePageTitle(): string {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const match = NAV_ITEMS.find((item) => pathname.startsWith(item.path));
  if (match) return match.label;
  if (pathname.startsWith('/onboarding')) return 'Get Started';
  return 'Alloy';
}

export function TopNav() {
  const title = usePageTitle();
  const isDashboard = useIsDashboard();
  const toggleHamburger = useUIStore((s) => s.toggleHamburgerMenu);

  return (
    <header
      className={cn(
        'sticky top-0 z-20 h-14 flex items-center justify-between px-4',
        'bg-white/80 dark:bg-surface-950/80 backdrop-blur-sm',
        'border-b border-surface-200 dark:border-surface-800'
      )}
    >
      {/* Left side: hamburger + brand */}
      <div className="flex items-center gap-2">
        {/* Hamburger menu — always visible */}
        <div className="relative">
          <button
            onClick={toggleHamburger}
            className="flex items-center justify-center w-9 h-9 rounded-lg text-surface-500 hover:text-surface-700 dark:hover:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
            aria-label="Menu"
          >
            <Menu className="w-4 h-4" />
          </button>
          <HamburgerMenu />
        </div>
        <Link to="/dashboard" className="flex items-center gap-2">
          <div className={cn(
            'flex items-center justify-center w-7 h-7 rounded-lg',
            isDashboard ? 'bg-amber-accent' : 'bg-primary-600'
          )}>
            <Zap className={cn('w-3.5 h-3.5', isDashboard ? 'text-surface-950' : 'text-white')} />
          </div>
          <span className="font-bold text-sm text-surface-900 dark:text-white">
            {isDashboard ? 'Dashboard' : title}
          </span>
        </Link>
      </div>

      {/* Right actions */}
      <div className="flex items-center gap-1">
        {/* Notification bell (placeholder) */}
        <button
          className="flex items-center justify-center w-9 h-9 rounded-lg text-surface-500 hover:text-surface-700 dark:hover:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
          aria-label="Notifications"
        >
          <Bell className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
}
