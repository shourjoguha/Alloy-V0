/**
 * TopNav
 * Top header bar. Visible on mobile/tablet.
 * On desktop the sidebar handles branding, so TopNav is minimal.
 */

import { useRouterState } from '@tanstack/react-router';
import { Zap, Settings } from 'lucide-react';
import { Link } from '@tanstack/react-router';
import { NAV_ITEMS } from '../../config/navigation.config';
import { ThemeToggle } from './ThemeToggle';
import { cn } from '../../lib/utils';

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

  return (
    <header
      className={cn(
        'sticky top-0 z-20 h-14 flex items-center justify-between px-4',
        'bg-white/80 dark:bg-surface-950/80 backdrop-blur-sm',
        'border-b border-surface-200 dark:border-surface-800',
        // On desktop, sidebar already shows branding — hide TopNav brand
        'md:pl-4'
      )}
    >
      {/* Mobile brand */}
      <div className="flex items-center gap-2 md:hidden">
        <div className="flex items-center justify-center w-7 h-7 rounded-lg bg-primary-600">
          <Zap className="w-3.5 h-3.5 text-white" />
        </div>
        <span className="font-bold text-sm text-surface-900 dark:text-white">
          Alloy
        </span>
      </div>

      {/* Desktop: show page title */}
      <h1 className="hidden md:block text-sm font-semibold text-surface-900 dark:text-surface-50">
        {title}
      </h1>

      {/* Right actions */}
      <div className="flex items-center gap-1">
        <div className="hidden md:block">
          <ThemeToggle />
        </div>
        <Link to="/settings" aria-label="Settings">
          <button className="flex items-center justify-center w-9 h-9 rounded-lg text-surface-500 hover:text-surface-700 dark:hover:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors">
            <Settings className="w-4 h-4" />
          </button>
        </Link>
      </div>
    </header>
  );
}
