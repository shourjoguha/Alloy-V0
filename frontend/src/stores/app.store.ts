/**
 * App Store — Persistent (synced to localStorage via zustand/middleware)
 *
 * Holds state that should survive a page refresh:
 * - User preferences (theme, units, defaults)
 * - Draft states (onboarding progress, workout builder)
 *
 * DO NOT add volatile UI state here — use ui.store.ts instead.
 */

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { HierarchicalGoalSliders, AvailabilityConfig } from '../types/onboarding';
import type { EquipmentType } from '../types/enums';
import type { ProgramSkeleton } from '../types/program';

/** Current store schema version — bump when persisted shape changes */
const STORE_VERSION = 1;

// ─── Types ──────────────────────────────────────────────────────────────────

type Theme = 'light' | 'dark';
type WeightUnit = 'kg' | 'lbs';
type DistanceUnit = 'km' | 'miles';
type BodyMapView = 'front' | 'back';

interface UserPreferences {
  theme: Theme;
  weightUnit: WeightUnit;
  distanceUnit: DistanceUnit;
  defaultBodyMapView: BodyMapView;
}

/** In-progress onboarding data — cleared on completion */
interface OnboardingDraft {
  currentStep: number;
  goals?: HierarchicalGoalSliders;
  availability?: AvailabilityConfig;
  availableEquipment: EquipmentType[];
  experienceLevel: 'beginner' | 'intermediate' | 'advanced';
  programLengthWeeks: number;
}

/** Active widget IDs on the dashboard, in display order */
type DashboardLayout = string[];

/** Lightweight reference to a favorited circuit */
interface FavoriteCircuit {
  id: number;
  name: string;
}

interface AppState {
  /** Anonymous session ID — generated once, persisted to localStorage */
  userId: string;
  preferences: UserPreferences;
  onboardingDraft: OnboardingDraft | null;
  dashboardLayout: DashboardLayout;
  /** The most recently generated program — persisted to localStorage */
  activeProgram: ProgramSkeleton | null;
  /** Favorite movement IDs — persisted */
  favoriteMovementIds: number[];
  /** Favorite circuit references — persisted */
  favoriteCircuits: FavoriteCircuit[];
  /** User profile: age */
  age: number | null;
  /** User profile: gender */
  gender: 'male' | 'female' | null;
}

interface AppActions {
  // Preferences
  setTheme: (theme: Theme) => void;
  setWeightUnit: (unit: WeightUnit) => void;
  setDistanceUnit: (unit: DistanceUnit) => void;
  setDefaultBodyMapView: (view: BodyMapView) => void;

  // Onboarding draft
  setOnboardingDraft: (draft: Partial<OnboardingDraft>) => void;
  clearOnboardingDraft: () => void;

  // Dashboard layout
  setDashboardLayout: (layout: DashboardLayout) => void;

  // Program
  setActiveProgram: (program: ProgramSkeleton) => void;
  clearActiveProgram: () => void;

  // Favorites
  toggleFavoriteMovement: (id: number) => void;
  toggleFavoriteCircuit: (id: number, name: string) => void;

  // Profile
  setAge: (age: number | null) => void;
  setGender: (gender: 'male' | 'female' | null) => void;

  // Full reset
  resetPreferences: () => void;
}

// ─── Defaults ────────────────────────────────────────────────────────────────

const DEFAULT_PREFERENCES: UserPreferences = {
  theme: 'light',
  weightUnit: 'kg',
  distanceUnit: 'km',
  defaultBodyMapView: 'front',
};

const DEFAULT_ONBOARDING_DRAFT: OnboardingDraft = {
  currentStep: 1,
  availableEquipment: [],
  experienceLevel: 'intermediate',
  programLengthWeeks: 10,
};

const DEFAULT_DASHBOARD_LAYOUT: DashboardLayout = [
  'volume-load',
  'one-rm-trend',
  'session-completion',
];

// ─── Store ───────────────────────────────────────────────────────────────────

export const useAppStore = create<AppState & AppActions>()(
  persist(
    (set) => ({
      // Initial state
      userId: crypto.randomUUID(),
      preferences: DEFAULT_PREFERENCES,
      onboardingDraft: null,
      dashboardLayout: DEFAULT_DASHBOARD_LAYOUT,
      activeProgram: null,
      favoriteMovementIds: [],
      favoriteCircuits: [],
      age: null,
      gender: null,

      // Preference actions
      setTheme: (theme) =>
        set((s) => ({ preferences: { ...s.preferences, theme } })),
      setWeightUnit: (weightUnit) =>
        set((s) => ({ preferences: { ...s.preferences, weightUnit } })),
      setDistanceUnit: (distanceUnit) =>
        set((s) => ({ preferences: { ...s.preferences, distanceUnit } })),
      setDefaultBodyMapView: (defaultBodyMapView) =>
        set((s) => ({ preferences: { ...s.preferences, defaultBodyMapView } })),

      // Onboarding draft actions
      setOnboardingDraft: (draft) =>
        set((s) => ({
          onboardingDraft: {
            ...(s.onboardingDraft ?? DEFAULT_ONBOARDING_DRAFT),
            ...draft,
          },
        })),
      clearOnboardingDraft: () => set({ onboardingDraft: null }),

      // Dashboard layout actions
      setDashboardLayout: (dashboardLayout) => set({ dashboardLayout }),

      // Program actions
      setActiveProgram: (activeProgram) => set({ activeProgram }),
      clearActiveProgram: () => set({ activeProgram: null }),

      // Favorites
      toggleFavoriteMovement: (id) =>
        set((s) => ({
          favoriteMovementIds: s.favoriteMovementIds.includes(id)
            ? s.favoriteMovementIds.filter((fid) => fid !== id)
            : [...s.favoriteMovementIds, id],
        })),
      toggleFavoriteCircuit: (id, name) =>
        set((s) => ({
          favoriteCircuits: s.favoriteCircuits.some((c) => c.id === id)
            ? s.favoriteCircuits.filter((c) => c.id !== id)
            : [...s.favoriteCircuits, { id, name }],
        })),

      // Profile
      setAge: (age) => set({ age }),
      setGender: (gender) => set({ gender }),

      // Full reset
      resetPreferences: () =>
        set({
          preferences: DEFAULT_PREFERENCES,
          dashboardLayout: DEFAULT_DASHBOARD_LAYOUT,
        }),
    }),
    {
      name: 'alloy-app-store',
      storage: createJSONStorage(() => localStorage),
      // Only persist these keys — keeps localStorage lean
      partialize: (state) => ({
        userId: state.userId,
        preferences: state.preferences,
        onboardingDraft: state.onboardingDraft,
        dashboardLayout: state.dashboardLayout,
        activeProgram: state.activeProgram,
        favoriteMovementIds: state.favoriteMovementIds,
        favoriteCircuits: state.favoriteCircuits,
        age: state.age,
        gender: state.gender,
      }),
      version: STORE_VERSION,
      migrate: (persisted, version) => {
        // When STORE_VERSION is bumped, reset to defaults to avoid stale data
        if (version < STORE_VERSION) {
          return {
            userId: crypto.randomUUID(),
            preferences: DEFAULT_PREFERENCES,
            onboardingDraft: null,
            dashboardLayout: DEFAULT_DASHBOARD_LAYOUT,
            activeProgram: null,
            favoriteMovementIds: [],
            favoriteCircuits: [],
            age: null,
            gender: null,
          };
        }
        return persisted as AppState & AppActions;
      },
    }
  )
);
