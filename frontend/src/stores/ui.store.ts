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
  | null;

interface UIState {
  /** Desktop sidebar expanded or collapsed */
  sidebarOpen: boolean;
  /** Mobile navigation menu open */
  mobileMenuOpen: boolean;
  /** Currently open modal — null means no modal is open */
  activeModal: ModalId;
  /** Data payload passed to the active modal */
  modalPayload: unknown;
}

interface UIActions {
  setSidebarOpen: (open: boolean) => void;
  toggleSidebar: () => void;
  setMobileMenuOpen: (open: boolean) => void;
  toggleMobileMenu: () => void;
  openModal: (id: ModalId, payload?: unknown) => void;
  closeModal: () => void;
}

// ─── Store ───────────────────────────────────────────────────────────────────

export const useUIStore = create<UIState & UIActions>((set) => ({
  // Initial state
  sidebarOpen: true,
  mobileMenuOpen: false,
  activeModal: null,
  modalPayload: null,

  // Actions
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),

  setMobileMenuOpen: (open) => set({ mobileMenuOpen: open }),
  toggleMobileMenu: () => set((s) => ({ mobileMenuOpen: !s.mobileMenuOpen })),

  openModal: (id, payload = null) =>
    set({ activeModal: id, modalPayload: payload }),
  closeModal: () => set({ activeModal: null, modalPayload: null }),
}));
