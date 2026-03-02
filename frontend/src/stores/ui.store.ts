/**
 * UI Store — Volatile (NOT persisted to localStorage)
 *
 * Holds transient UI state that should reset on page refresh:
 * - Sidebar open/closed
 * - Active modal
 * - Mobile menu state
 *
 * DO NOT add user preferences or draft data here — use app.store.ts instead.
 */

import { create } from 'zustand';

// ─── Types ──────────────────────────────────────────────────────────────────

export type ModalId =
  | 'add-widget'
  | 'swap-exercise'
  | 'confirm-discard'
  | 'region-soreness'
  | 'exercise-browser'
  | null;

type DashboardTab = 'personal' | 'squads';

interface UIState {
  /** Desktop sidebar expanded or collapsed */
  sidebarOpen: boolean;
  /** Mobile navigation menu open */
  mobileMenuOpen: boolean;
  /** Currently open modal — null means no modal is open */
  activeModal: ModalId;
  /** Data payload passed to the active modal */
  modalPayload: unknown;
  /** Hamburger menu open state */
  hamburgerMenuOpen: boolean;
  /** Dashboard bottom tab: personal or squads */
  selectedDashboardTab: DashboardTab;
  /** Currently viewed week index (0-based within flattened weeks) */
  selectedWeekIndex: number;
  /** Currently selected day index within the week (null = none) */
  selectedDayIndex: number | null;
  /** Whether the workout selector CTA is expanded to show day pills */
  workoutSelectorExpanded: boolean;
}

interface UIActions {
  setSidebarOpen: (open: boolean) => void;
  toggleSidebar: () => void;
  setMobileMenuOpen: (open: boolean) => void;
  toggleMobileMenu: () => void;
  openModal: (id: ModalId, payload?: unknown) => void;
  closeModal: () => void;
  setHamburgerMenuOpen: (open: boolean) => void;
  toggleHamburgerMenu: () => void;
  setSelectedDashboardTab: (tab: DashboardTab) => void;
  setSelectedWeekIndex: (index: number) => void;
  setSelectedDayIndex: (index: number | null) => void;
  setWorkoutSelectorExpanded: (expanded: boolean) => void;
  toggleWorkoutSelector: () => void;
}

// ─── Store ───────────────────────────────────────────────────────────────────

export const useUIStore = create<UIState & UIActions>((set) => ({
  // Initial state
  sidebarOpen: true,
  mobileMenuOpen: false,
  activeModal: null,
  modalPayload: null,
  hamburgerMenuOpen: false,
  selectedDashboardTab: 'personal',
  selectedWeekIndex: 0,
  selectedDayIndex: null,
  workoutSelectorExpanded: false,

  // Actions
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),

  setMobileMenuOpen: (open) => set({ mobileMenuOpen: open }),
  toggleMobileMenu: () => set((s) => ({ mobileMenuOpen: !s.mobileMenuOpen })),

  openModal: (id, payload = null) =>
    set({ activeModal: id, modalPayload: payload }),
  closeModal: () => set({ activeModal: null, modalPayload: null }),

  setHamburgerMenuOpen: (open) => set({ hamburgerMenuOpen: open }),
  toggleHamburgerMenu: () => set((s) => ({ hamburgerMenuOpen: !s.hamburgerMenuOpen })),

  setSelectedDashboardTab: (tab) => set({ selectedDashboardTab: tab }),
  setSelectedWeekIndex: (index) => set({ selectedWeekIndex: index, selectedDayIndex: null, workoutSelectorExpanded: false }),
  setSelectedDayIndex: (index) => set({ selectedDayIndex: index }),
  setWorkoutSelectorExpanded: (expanded) => set({ workoutSelectorExpanded: expanded }),
  toggleWorkoutSelector: () => set((s) => ({ workoutSelectorExpanded: !s.workoutSelectorExpanded })),
}));
