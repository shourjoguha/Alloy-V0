/**
 * Navigation Configuration
 * Defines all primary nav items. Change labels/icons/routes here only.
 * Consumed by both Sidebar (desktop) and BottomNav (mobile).
 */

import type { LucideIcon } from 'lucide-react';
import {
  LayoutDashboard,
  Dumbbell,
  ClipboardList,
  Activity,
  Settings,
} from 'lucide-react';
import { ROUTES } from './routes.config';

export interface NavItem {
  label: string;
  path: string;
  icon: LucideIcon;
  /** Show in bottom nav on mobile */
  showInBottomNav: boolean;
}

export const NAV_ITEMS: NavItem[] = [
  {
    label: 'Dashboard',
    path: ROUTES.DASHBOARD,
    icon: LayoutDashboard,
    showInBottomNav: true,
  },
  {
    label: 'Program',
    path: ROUTES.PROGRAM,
    icon: ClipboardList,
    showInBottomNav: true,
  },
  {
    label: 'Workout',
    path: '/workout',
    icon: Dumbbell,
    showInBottomNav: true,
  },
  {
    label: 'Readiness',
    path: ROUTES.READINESS,
    icon: Activity,
    showInBottomNav: true,
  },
  {
    label: 'Settings',
    path: ROUTES.SETTINGS,
    icon: Settings,
    showInBottomNav: false,
  },
] as const;
