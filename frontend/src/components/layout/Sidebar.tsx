/**
 * Sidebar
 * Desktop navigation panel. Collapsible via UIStore.
 * Shows icon + label when expanded, icon only when collapsed.
 */

import { Link, useRouterState } from '@tanstack/react-router';
import { motion, AnimatePresence } from 'framer-motion';
import { PanelLeftClose, PanelLeftOpen, Zap } from 'lucide-react';
import { NAV_ITEMS } from '../../config/navigation.config';
import { useUIStore } from '../../stores/ui.store';
import { cn } from '../../lib/utils';
import { ThemeToggle } from './ThemeToggle';
import { Tooltip } from '../ui/tooltip';
import { Separator } from '../ui/separator';

export function Sidebar() {
  const sidebarOpen = useUIStore((s) => s.sidebarOpen);
  const toggleSidebar = useUIStore((s) => s.toggleSidebar);
  const location = useRouterState({ select: (s) => s.location });

  return (
    <motion.aside
      animate={{ width: sidebarOpen ? 220 : 64 }}
      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      className={cn(
        'hidden md:flex flex-col shrink-0 h-screen sticky top-0',
        'border-r border-surface-200 dark:border-surface-800',
        'bg-white dark:bg-surface-950 overflow-hidden z-20'
      )}
    >
      {/* Brand */}
      <div className="flex items-center gap-3 h-14 px-3.5 shrink-0">
        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-primary-600 shrink-0">
          <Zap className="w-4 h-4 text-white" />
        </div>
        <AnimatePresence>
          {sidebarOpen && (
            <motion.span
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -8 }}
              transition={{ duration: 0.15 }}
              className="font-bold text-base text-surface-900 dark:text-white whitespace-nowrap"
            >
              Alloy
            </motion.span>
          )}
        </AnimatePresence>
      </div>

      <Separator />

      {/* Nav Items */}
      <nav className="flex flex-col gap-1 flex-1 p-2 overflow-y-auto">
        {NAV_ITEMS.filter((item) => item.label !== 'Settings').map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname.startsWith(item.path);

          const linkContent = (
            <Link
              to={item.path}
              className={cn(
                'flex items-center gap-3 rounded-lg px-2.5 py-2 text-sm font-medium transition-colors',
                'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500',
                isActive
                  ? 'bg-primary-50 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300'
                  : 'text-surface-600 dark:text-surface-400 hover:bg-surface-100 dark:hover:bg-surface-800 hover:text-surface-900 dark:hover:text-surface-100'
              )}
            >
              <Icon className="w-4.5 h-4.5 shrink-0" />
              <AnimatePresence>
                {sidebarOpen && (
                  <motion.span
                    initial={{ opacity: 0, x: -6 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -6 }}
                    transition={{ duration: 0.12 }}
                    className="whitespace-nowrap overflow-hidden"
                  >
                    {item.label}
                  </motion.span>
                )}
              </AnimatePresence>
            </Link>
          );

          return sidebarOpen ? (
            <div key={item.path}>{linkContent}</div>
          ) : (
            <Tooltip key={item.path} content={item.label} side="right">
              <div>{linkContent}</div>
            </Tooltip>
          );
        })}
      </nav>

      <Separator />

      {/* Bottom actions */}
      <div className="flex flex-col gap-1 p-2">
        <ThemeToggle />

        {/* Collapse toggle */}
        <Tooltip
          content={sidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
          side="right"
        >
          <button
            onClick={toggleSidebar}
            className={cn(
              'flex items-center justify-center w-9 h-9 rounded-lg',
              'text-surface-500 hover:text-surface-700 dark:hover:text-surface-300',
              'hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors'
            )}
            aria-label={sidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
          >
            {sidebarOpen ? (
              <PanelLeftClose className="w-4 h-4" />
            ) : (
              <PanelLeftOpen className="w-4 h-4" />
            )}
          </button>
        </Tooltip>
      </div>
    </motion.aside>
  );
}
