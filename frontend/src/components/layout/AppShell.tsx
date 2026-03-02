/**
 * AppShell
 * Root layout for authenticated pages.
 * Composes: Sidebar (desktop) | TopNav | BottomNav (mobile) | animated Outlet
 *
 * Responsive layout:
 *   Mobile  : TopNav (top) + full-width content + BottomNav (bottom)
 *   Desktop : Sidebar (left) + TopNav (top of content) + scrollable content
 */

import { Outlet, useRouterState } from '@tanstack/react-router';
import { AnimatePresence } from 'framer-motion';
import { Sidebar } from './Sidebar';
import { TopNav } from './TopNav';
import { BottomNav } from './BottomNav';
import { PageTransition } from './PageTransition';
import { TooltipProvider } from '../ui/tooltip';

export function AppShell() {
  const pathname = useRouterState({ select: (s) => s.location.pathname });

  return (
    <TooltipProvider>
      <div className="flex h-screen overflow-hidden bg-surface-50 dark:bg-surface-950">
        {/* Desktop sidebar */}
        <Sidebar />

        {/* Main content area */}
        <div className="flex flex-col flex-1 min-w-0 overflow-hidden">
          <TopNav />

          {/* Animated page outlet */}
          <div className="flex flex-col flex-1 min-h-0 overflow-hidden">
            <AnimatePresence mode="wait" initial={false}>
              <PageTransition routeKey={pathname}>
                <Outlet />
              </PageTransition>
            </AnimatePresence>
          </div>
        </div>

        {/* Mobile bottom navigation */}
        <BottomNav />
      </div>
    </TooltipProvider>
  );
}
