/**
 * HamburgerMenu
 * Dropdown menu anchored to the hamburger icon in TopNav.
 * Shows: Exercises, Historical Programs, Settings, Friends, Logout.
 */

import { useRef, useEffect } from 'react';
import { Link, useRouterState } from '@tanstack/react-router';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Star,
  Dumbbell,
  Users,
  LogOut,
  Settings,
  History,
} from 'lucide-react';
import { NAV_ITEMS } from '../../config/navigation.config';
import { useUIStore } from '../../stores/ui.store';
import { cn } from '../../lib/utils';

interface UtilityItem {
  label: string;
  icon: typeof Star;
  action: 'favorites' | 'exercises' | 'history' | 'settings' | 'friends' | 'logout';
  disabled?: boolean;
  variant?: 'default' | 'danger';
}

const UTILITY_ITEMS: UtilityItem[] = [
  { label: 'Favorites', icon: Star, action: 'favorites' },
  { label: 'Exercises', icon: Dumbbell, action: 'exercises' },
  { label: 'History', icon: History, action: 'history', disabled: true },
  { label: 'Settings', icon: Settings, action: 'settings' },
  { label: 'Friends', icon: Users, action: 'friends', disabled: true },
  { label: 'Logout', icon: LogOut, action: 'logout', disabled: true, variant: 'danger' },
];

export function HamburgerMenu() {
  const isOpen = useUIStore((s) => s.hamburgerMenuOpen);
  const setOpen = useUIStore((s) => s.setHamburgerMenuOpen);
  const openModal = useUIStore((s) => s.openModal);
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const menuRef = useRef<HTMLDivElement>(null);

  // Close on click outside
  useEffect(() => {
    if (!isOpen) return;
    function handleClickOutside(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen, setOpen]);

  // Close on Escape
  useEffect(() => {
    if (!isOpen) return;
    function handleEscape(e: KeyboardEvent) {
      if (e.key === 'Escape') setOpen(false);
    }
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, setOpen]);

  function handleUtilityClick(item: UtilityItem) {
    if (item.disabled) return;

    switch (item.action) {
      case 'favorites':
        openModal('exercise-browser');
        setOpen(false);
        break;
      case 'exercises':
        openModal('exercise-browser');
        setOpen(false);
        break;
      case 'settings':
        setOpen(false);
        break;
      default:
        setOpen(false);
        break;
    }
  }

  // Filter out Settings from nav items (it's in utility section)
  const navItems = NAV_ITEMS.filter((item) => item.label !== 'Settings');

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          ref={menuRef}
          initial={{ opacity: 0, y: -8, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -8, scale: 0.95 }}
          transition={{ duration: 0.15, ease: 'easeOut' }}
          className={cn(
            'absolute top-12 left-0 z-50 min-w-[200px]',
            'bg-white dark:bg-surface-900 rounded-xl',
            'border border-surface-200 dark:border-surface-700',
            'shadow-lg overflow-hidden'
          )}
        >
          {/* Navigation links */}
          <div className="py-1.5">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname.startsWith(item.path);

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setOpen(false)}
                >
                  <div
                    className={cn(
                      'flex items-center gap-3 px-4 py-2.5 text-sm transition-colors cursor-pointer',
                      isActive
                        ? 'bg-amber-accent-muted text-amber-accent-hover font-medium'
                        : 'text-surface-700 dark:text-surface-300 hover:bg-surface-50 dark:hover:bg-surface-800'
                    )}
                  >
                    <Icon className="w-4 h-4 shrink-0" />
                    <span>{item.label}</span>
                  </div>
                </Link>
              );
            })}
          </div>

          {/* Divider */}
          <div className="h-px bg-surface-200 dark:bg-surface-700" />

          {/* Utility items */}
          <div className="py-1.5">
            {UTILITY_ITEMS.map((item) => {
              const Icon = item.icon;
              const isDisabled = item.disabled;

              const content = (
                <div
                  className={cn(
                    'flex items-center gap-3 px-4 py-2.5 text-sm transition-colors',
                    isDisabled
                      ? 'text-surface-300 dark:text-surface-600 cursor-not-allowed'
                      : item.variant === 'danger'
                        ? 'text-error hover:bg-red-50 dark:hover:bg-red-900/20 cursor-pointer'
                        : 'text-surface-700 dark:text-surface-300 hover:bg-surface-50 dark:hover:bg-surface-800 cursor-pointer'
                  )}
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span>{item.label}</span>
                </div>
              );

              if (item.action === 'settings' && !isDisabled) {
                return (
                  <Link
                    key={item.label}
                    to="/settings"
                    onClick={() => setOpen(false)}
                  >
                    {content}
                  </Link>
                );
              }

              return (
                <button
                  key={item.label}
                  type="button"
                  disabled={isDisabled}
                  onClick={() => handleUtilityClick(item)}
                  className="w-full text-left"
                >
                  {content}
                </button>
              );
            })}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
