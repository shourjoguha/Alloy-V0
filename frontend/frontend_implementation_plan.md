# Alloy Fitness - Frontend Implementation Plan

**Project:** Smart Fitness Program Generator SaaS  
**Stack:** React 18 + TypeScript + Vite + Tailwind CSS v4  
**Last Updated:** 2026-03-01  
**Status:** Phase 1 Complete

---

## Table of Contents

1. [Architecture Decisions](#1-architecture-decisions)
2. [Directory Structure](#2-directory-structure)
3. [Configuration Standards](#3-configuration-standards)
4. [Phase 1: Foundation (COMPLETE)](#4-phase-1-foundation-complete)
5. [Phase 2: Core Infrastructure](#5-phase-2-core-infrastructure)
6. [Phase 3: Layout & Navigation](#6-phase-3-layout--navigation)
7. [Phase 4: Onboarding Flow](#7-phase-4-onboarding-flow)
8. [Phase 5: Dashboard & Widgets](#8-phase-5-dashboard--widgets)
9. [Phase 6: Program & Workout Views](#9-phase-6-program--workout-views)
10. [Phase 7: Workout Builder](#10-phase-7-workout-builder)
11. [Phase 8: Readiness Logger & Body Map](#11-phase-8-readiness-logger--body-map)
12. [Phase 9: Settings & Preferences](#12-phase-9-settings--preferences)
13. [Phase 10: Authentication Integration](#13-phase-10-authentication-integration)
14. [Railway Deployment Guide](#14-railway-deployment-guide)
15. [Appendix: File Reference](#15-appendix-file-reference)

---

## 1. Architecture Decisions

### 1.1 Technology Choices

| Category | Choice | Rationale |
|----------|--------|-----------|
| **Framework** | React 18 + TypeScript | Type safety, ecosystem maturity |
| **Build Tool** | Vite 7.x | Fast HMR, native ESM, Tailwind plugin |
| **Styling** | Tailwind CSS v4 | Config-driven tokens, `@theme` directive |
| **Routing** | TanStack Router | Type-safe routes, search params, prefetching |
| **Server State** | TanStack Query | Caching, background refetch, offline-ready |
| **Client State** | Zustand | Lightweight, no boilerplate, selective persist |
| **UI Primitives** | Radix UI (shadcn/ui) | Accessible, unstyled, composable |
| **Animations** | Framer Motion | Declarative, gesture support, layout animations |
| **Icons** | lucide-react | Tree-shakeable, consistent stroke width |
| **Charts** | Recharts | Composable, responsive, React-native |
| **Drag & Drop** | @dnd-kit | Accessible, performant, sortable lists |
| **Toasts** | Sonner | Minimal API, stacking, promise support |
| **Forms** | React Hook Form + Zod | Performant validation, type inference |

### 1.2 State Management Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                     STATE ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│  SERVER STATE (TanStack Query)                              │
│  • API responses (programs, sessions, exercises)            │
│  • Cached with stale-while-revalidate                       │
│  • Background refetch on window focus                       │
├─────────────────────────────────────────────────────────────┤
│  CLIENT STATE - VOLATILE (useUIStore)                       │
│  • Sidebar open/closed                                      │
│  • Active modal ID                                          │
│  • Mobile menu state                                        │
│  • Resets on refresh (NOT persisted)                        │
├─────────────────────────────────────────────────────────────┤
│  CLIENT STATE - PERSISTENT (useAppStore)                    │
│  • User preferences (units, theme, default views)           │
│  • Draft states (onboarding progress, workout builder)      │
│  • Persisted to localStorage                                │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Error Handling Strategy

| Error Type | Handling Approach |
|------------|-------------------|
| **Form Validation** | Inline errors below inputs (red text) |
| **API Errors (User Action)** | Sonner toast (bottom-center) |
| **Widget Data Fetch Failure** | Localized error state within widget container |
| **Route Component Crash** | Error Boundary with branded fallback UI |
| **DnD Builder Crash** | Isolated Error Boundary with "Try Again" |

### 1.4 Routing Architecture

- **Pre-auth routes:** `/onboarding/*`, `/login`, `/signup`
- **Post-auth routes:** `/dashboard`, `/program/*`, `/workout/*`, `/readiness`, `/settings`
- **Default authenticated route:** `/dashboard`
- **Search params:** Type-validated for filters, pagination, widget states

---

## 2. Directory Structure

```
frontend/
├── public/
│   └── assets/
│       └── body-map/           # SVG assets for body map
├── src/
│   ├── api/                    # API client and query hooks
│   │   ├── client.ts           # Axios/fetch instance with interceptors
│   │   ├── queries/            # TanStack Query hooks by domain
│   │   │   ├── onboarding.ts
│   │   │   ├── program.ts
│   │   │   └── exercises.ts
│   │   └── mutations/          # TanStack Mutation hooks
│   │       ├── onboarding.ts
│   │       └── program.ts
│   ├── components/
│   │   ├── ui/                 # Radix/shadcn primitives
│   │   │   ├── button.tsx
│   │   │   ├── slider.tsx
│   │   │   ├── modal.tsx
│   │   │   ├── toast.tsx
│   │   │   └── ...
│   │   ├── layout/             # App shell components
│   │   │   ├── AppShell.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── BottomNav.tsx
│   │   │   ├── TopNav.tsx
│   │   │   └── PageContainer.tsx
│   │   ├── dashboard/
│   │   │   ├── widgets/        # Plug-and-play chart widgets
│   │   │   │   ├── WidgetRegistry.ts
│   │   │   │   ├── VolumeLoadChart.tsx
│   │   │   │   ├── OneRMTrendChart.tsx
│   │   │   │   └── RadarChart.tsx
│   │   │   ├── WidgetGrid.tsx
│   │   │   └── AddWidgetModal.tsx
│   │   ├── onboarding/         # Onboarding flow components
│   │   │   ├── GoalSliders.tsx
│   │   │   ├── AvailabilityPicker.tsx
│   │   │   ├── EquipmentSelector.tsx
│   │   │   └── OnboardingStepper.tsx
│   │   ├── program/            # Program/workout viewer
│   │   │   ├── SessionCard.tsx
│   │   │   ├── WeekView.tsx
│   │   │   └── ProgramTimeline.tsx
│   │   ├── workout-builder/    # DnD workout builder
│   │   │   ├── ExerciseList.tsx
│   │   │   ├── SwapPanel.tsx
│   │   │   └── BuilderContext.tsx
│   │   ├── body-map/           # Readiness logger
│   │   │   ├── BodyMapSVG.tsx
│   │   │   ├── RegionPopover.tsx
│   │   │   └── SorenessSlider.tsx
│   │   └── shared/             # Cross-cutting components
│   │       ├── ErrorBoundary.tsx
│   │       ├── ErrorFallback.tsx
│   │       ├── LoadingSpinner.tsx
│   │       └── EmptyState.tsx
│   ├── config/                 # Centralized configuration
│   │   ├── api.config.ts       # API URLs, timeouts
│   │   ├── theme.config.ts     # Color tokens, spacing
│   │   ├── routes.config.ts    # Route paths as constants
│   │   └── widgets.config.ts   # Dashboard widget definitions
│   ├── hooks/                  # Custom React hooks
│   │   ├── useMediaQuery.ts
│   │   ├── useLocalStorage.ts
│   │   └── useDebounce.ts
│   ├── lib/                    # Utility libraries
│   │   ├── utils.ts            # cn() helper, formatters
│   │   └── validators.ts       # Zod schemas
│   ├── routes/                 # TanStack Router route definitions
│   │   ├── __root.tsx
│   │   ├── index.tsx           # Redirects to /dashboard
│   │   ├── dashboard.tsx
│   │   ├── onboarding/
│   │   │   ├── index.tsx
│   │   │   └── $step.tsx
│   │   ├── program/
│   │   │   ├── index.tsx
│   │   │   └── $programId.tsx
│   │   ├── workout/
│   │   │   └── $sessionId.tsx
│   │   ├── readiness.tsx
│   │   └── settings.tsx
│   ├── stores/                 # Zustand stores
│   │   ├── ui.store.ts         # Volatile UI state
│   │   └── app.store.ts        # Persistent app state
│   ├── types/                  # TypeScript definitions
│   │   ├── index.ts
│   │   ├── enums.ts
│   │   ├── onboarding.ts
│   │   ├── program.ts
│   │   └── api.ts
│   ├── App.tsx                 # Root component with providers
│   ├── main.tsx                # Entry point
│   ├── index.css               # Tailwind + theme tokens
│   └── routeTree.gen.ts        # Auto-generated route tree
├── .env.example                # Environment variable template
├── .env.local                  # Local dev environment (gitignored)
├── vite.config.ts
├── tailwind.config.ts          # If needed for plugins
├── tsconfig.json
├── tsconfig.app.json
├── Dockerfile                  # Production container
├── nginx.conf                  # SPA fallback config
└── frontend_implementation_plan.md
```

---

## 3. Configuration Standards

### 3.1 Environment Variables

All environment-specific values MUST be defined in `.env` files and accessed via `import.meta.env`.

```bash
# .env.example
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Alloy Fitness
VITE_SUPABASE_URL=                    # Added in Phase 10
VITE_SUPABASE_ANON_KEY=               # Added in Phase 10
```

### 3.2 API Configuration (`src/config/api.config.ts`)

```typescript
export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  endpoints: {
    onboarding: {
      validateSliders: '/api/onboarding/validate-sliders',
      generateProgram: '/api/onboarding/generate-program',
      health: '/api/onboarding/health',
      configSliders: '/api/onboarding/config/sliders',
      configTimeAllocation: '/api/onboarding/config/time-allocation',
    },
    system: {
      health: '/health',
      info: '/api/info',
    },
  },
} as const;
```

### 3.3 Route Configuration (`src/config/routes.config.ts`)

```typescript
export const ROUTES = {
  HOME: '/',
  DASHBOARD: '/dashboard',
  ONBOARDING: '/onboarding',
  ONBOARDING_STEP: '/onboarding/$step',
  PROGRAM: '/program',
  PROGRAM_DETAIL: '/program/$programId',
  WORKOUT: '/workout/$sessionId',
  READINESS: '/readiness',
  SETTINGS: '/settings',
} as const;
```

### 3.4 Theme Configuration (`src/config/theme.config.ts`)

```typescript
// Mirror of CSS custom properties for JS access
export const THEME = {
  colors: {
    primary: {
      50: '#f0f9ff',
      // ... full scale
      950: '#082f49',
    },
    severity: {
      none: '#22c55e',
      low: '#84cc16',
      medium: '#eab308',
      high: '#f97316',
      critical: '#ef4444',
    },
  },
  radius: {
    sm: '0.25rem',
    md: '0.375rem',
    lg: '0.5rem',
    xl: '0.75rem',
    '2xl': '1rem',
    full: '9999px',
  },
} as const;
```

---

## 4. Phase 1: Foundation (COMPLETE)

### 4.1 Tasks

- [x] **1.1** Initialize Vite + React + TypeScript project in `/frontend`
- [x] **1.2** Install core dependencies:
  - [x] `tailwindcss`, `@tailwindcss/vite`
  - [x] `framer-motion`
  - [x] `lucide-react`
  - [x] `@dnd-kit/core`, `@dnd-kit/sortable`
  - [x] `@tanstack/react-query`
  - [x] `recharts`
  - [x] `zustand`
- [x] **1.3** Configure Tailwind CSS v4 with `@theme` directive
  - [x] Primary colors (sky blue scale)
  - [x] Secondary colors (fuchsia scale)
  - [x] Surface colors (zinc scale) with dark mode
  - [x] Severity/heatmap colors (green → red)
  - [x] Semantic colors (success, warning, error, info)
  - [x] Typography scale (xs → 5xl)
  - [x] Border radius tokens
  - [x] Font families (Inter, JetBrains Mono)
- [x] **1.4** Configure Vite with API proxy to `http://localhost:8000`
- [x] **1.5** Generate TypeScript types from backend models:
  - [x] `src/types/enums.ts` — All const-object enums
  - [x] `src/types/onboarding.ts` — Onboarding interfaces
  - [x] `src/types/program.ts` — Program/session interfaces
  - [x] `src/types/api.ts` — API response wrappers
  - [x] `src/types/index.ts` — Barrel export
- [x] **1.6** Verify TypeScript compilation and Vite build

### 4.2 Files Created

| File | Purpose |
|------|---------|
| `vite.config.ts` | Vite config with Tailwind plugin + API proxy |
| `src/index.css` | Tailwind imports + `@theme` design tokens |
| `src/types/enums.ts` | Const-object enums (erasableSyntaxOnly compatible) |
| `src/types/onboarding.ts` | Onboarding request/response types |
| `src/types/program.ts` | Program skeleton types |
| `src/types/api.ts` | Standardized API contracts |
| `src/types/index.ts` | Central type exports |

---

## 5. Phase 2: Core Infrastructure (COMPLETE)

### 5.1 Tasks

- [x] **2.1** Install additional dependencies:
  - [x] `@tanstack/react-router`, `@tanstack/router-devtools`, `@tanstack/router-plugin`
  - [x] `sonner`
  - [x] `@radix-ui/react-*` (dialog, popover, slider, dropdown-menu, tooltip, switch, select, separator)
  - [x] `react-hook-form`, `@hookform/resolvers`, `zod`
  - [x] `clsx`, `tailwind-merge`
- [x] **2.2** Create configuration files:
  - [x] `src/config/api.config.ts` — API URLs, timeouts, query defaults
  - [x] `src/config/routes.config.ts` — All route paths as constants
  - [x] `src/config/theme.config.ts` — JS mirror of CSS tokens + chart colours
  - [x] `src/config/navigation.config.ts` — Nav items with icons and routes
- [x] **2.3** Set up API client:
  - [x] `src/api/client.ts` — Typed fetch wrapper, timeout, error transformation
  - [x] Error response transformed into `ApiClientError` class
  - [x] Dev-only request/response console logging
- [x] **2.4** Set up TanStack Query:
  - [x] `src/api/queryClient.ts` — Singleton with stale time, smart retry (no 4xx retries)
- [x] **2.5** Set up Zustand stores:
  - [x] `src/stores/ui.store.ts` — Volatile: sidebar, modals, mobile menu (NOT persisted)
  - [x] `src/stores/app.store.ts` — Persistent: theme, units, body map view, onboarding draft, dashboard layout
- [x] **2.6** Create utility functions:
  - [x] `src/lib/utils.ts` — `cn()`, `formatDuration`, weight converters, `arrayMove`, etc.
  - [x] `src/lib/validators.ts` — Zod schemas mirroring all Pydantic models
- [x] **2.7** Set up TanStack Router:
  - [x] `@tanstack/router-plugin` added to `vite.config.ts`
  - [x] `src/routes/__root.tsx` — Root layout with theme sync, Toaster, devtools
  - [x] `src/routes/index.tsx` — Redirects `/` → `/dashboard`
  - [x] `src/routes/dashboard.tsx` — Placeholder
  - [x] `src/routes/settings.tsx` — Placeholder
  - [x] `src/routeTree.gen.ts` — Auto-generated (do not edit manually)
- [x] **2.8** Create shared components:
  - [x] `src/components/shared/ErrorBoundary.tsx` — Class component with scope logging
  - [x] `src/components/shared/ErrorFallback.tsx` — Branded fallback with compact variant
  - [x] `src/components/shared/LoadingSpinner.tsx` — Size variants + PageLoader
  - [x] `src/components/shared/EmptyState.tsx` — Configurable empty state
- [x] **2.9** Wire up `src/main.tsx`:
  - [x] `RouterProvider` wrapping entire app
  - [x] `QueryClientProvider` with singleton `queryClient`
  - [x] `Toaster` (sonner) in `__root.tsx` at `bottom-center`
- [x] **2.10** Create environment files:
  - [x] `.env.example` — Template with all keys documented
  - [x] `.env.local` — Local dev values (gitignored via `*.local`)

### 5.2 Acceptance Criteria

- [x] TanStack Router generates route tree without errors
- [x] Full TypeScript build passes (`tsc -b` clean)
- [x] Vite production build succeeds
- Zustand stores initialize correctly *(verified at runtime)*
- Error boundary catches and displays fallback *(verified at runtime)*

### 5.3 Files Created

| File | Purpose |
|------|---------|
| `src/config/api.config.ts` | ✅ API URLs + query defaults |
| `src/config/routes.config.ts` | ✅ Route path constants |
| `src/config/theme.config.ts` | ✅ JS theme tokens + chart colours |
| `src/config/navigation.config.ts` | ✅ Nav items config |
| `src/api/client.ts` | ✅ Typed fetch wrapper |
| `src/api/queryClient.ts` | ✅ TanStack Query singleton |
| `src/stores/ui.store.ts` | ✅ Volatile UI store |
| `src/stores/app.store.ts` | ✅ Persistent app store |
| `src/lib/utils.ts` | ✅ `cn()` + formatters |
| `src/lib/validators.ts` | ✅ Zod schemas |
| `src/routes/__root.tsx` | ✅ Root route + providers |
| `src/routes/index.tsx` | ✅ `/` redirect |
| `src/routes/dashboard.tsx` | ✅ Dashboard placeholder |
| `src/routes/settings.tsx` | ✅ Settings placeholder |
| `src/components/shared/ErrorBoundary.tsx` | ✅ Error boundary |
| `src/components/shared/ErrorFallback.tsx` | ✅ Error fallback UI |
| `src/components/shared/LoadingSpinner.tsx` | ✅ Spinner + PageLoader |
| `src/components/shared/EmptyState.tsx` | ✅ Empty state |
| `src/main.tsx` | ✅ Rewired with all providers |
| `.env.example` | ✅ Env variable template |
| `.env.local` | ✅ Local dev values |

---

## 6. Phase 3: Layout & Navigation (COMPLETE)

### 6.1 Tasks

- [x] **3.1** Create base UI components (Radix + Tailwind):
  - [x] `src/components/ui/button.tsx`
  - [x] `src/components/ui/card.tsx`
  - [x] `src/components/ui/input.tsx`
  - [x] `src/components/ui/separator.tsx`
  - [x] `src/components/ui/tooltip.tsx`
  - [x] `src/components/ui/badge.tsx`
  - Note: `slider.tsx`, `modal.tsx`, `dropdown-menu.tsx` not created as standalone wrappers — Radix primitives are used directly in consuming components (GoalSliders, AddWidgetModal, etc.)
- [x] **3.2** Create layout components:
  - [x] `src/components/layout/AppShell.tsx` — Main layout wrapper
  - [x] `src/components/layout/Sidebar.tsx` — Desktop sidebar nav
  - [x] `src/components/layout/BottomNav.tsx` — Mobile bottom navigation
  - [x] `src/components/layout/TopNav.tsx` — Top bar with settings link
  - [x] `src/components/layout/PageContainer.tsx` — Content wrapper
  - [x] `src/components/layout/PageTransition.tsx` — Framer Motion wrapper
  - [x] `src/components/layout/ThemeToggle.tsx` — Sun/moon toggle
- [x] **3.3** Implement responsive breakpoints:
  - [x] Mobile: Bottom nav visible, sidebar hidden (`md:hidden` / `hidden md:flex`)
  - [x] Tablet: Collapsible sidebar (Framer Motion 220px↔64px)
  - [x] Desktop: Fixed sidebar
- [x] **3.4** Create navigation config:
  - [x] `src/config/navigation.config.ts` — Nav items with icons
- [x] **3.5** Implement theme toggle:
  - [x] Add to AppStore preferences
  - [x] Apply `dark` class to `<html>` (in `__root.tsx`)
  - [x] Persist preference to localStorage (via zustand persist)
- [x] **3.6** Add page transition animations:
  - [x] Framer Motion `AnimatePresence` on route changes (in AppShell)
  - [x] Fade/slide transitions (PageTransition component)

### 6.2 Acceptance Criteria

- Layout renders correctly at mobile/tablet/desktop breakpoints
- Navigation highlights active route
- Theme toggle persists across refresh
- Page transitions animate smoothly
- Sidebar collapse state persists (volatile)

---

## 7. Phase 4: Onboarding Flow (COMPLETE)

### 7.1 Tasks

- [x] **4.1** Create onboarding route structure:
  - [x] `src/routes/onboarding.tsx` — Full-screen layout (no AppShell)
  - [x] `src/routes/onboarding/index.tsx` — Redirects to step 1
  - [x] `src/routes/onboarding/$step.tsx` — Dynamic step handler
- [x] **4.2** Create onboarding stepper:
  - [x] `src/components/onboarding/OnboardingStepper.tsx`
  - [x] Step indicators with progress (check icons for completed)
  - [x] Back/Next navigation (sticky footer CTA)
- [x] **4.3** Create goal sliders component:
  - [x] `src/components/onboarding/GoalSliders.tsx`
  - [x] Primary slider (Strength ↔ Endurance) with Radix Slider
  - [x] Secondary sliders with sigmoid-based influence visualization
  - [x] Real-time normalized values display ("Adjusted: X%")
- [x] **4.4** Create availability picker:
  - [x] `src/components/onboarding/AvailabilityPicker.tsx`
  - [x] Days per week selector (1–7 buttons)
  - [x] Preferred days selector (optional, Mon–Sun)
  - [x] Time per session buttons (30–120m)
  - [x] "Let system optimize" toggle (Radix Switch)
- [x] **4.5** Create equipment selector:
  - [x] `src/components/onboarding/EquipmentSelector.tsx`
  - [x] Multi-select grid with icons
  - [x] Validation: blocks Continue if empty
- [x] **4.6** Create experience level selector:
  - [x] `src/components/onboarding/ExperienceSelector.tsx`
  - [x] Beginner / Intermediate / Advanced cards with descriptions
- [x] **4.7** Create review step:
  - [x] Display goals, availability, equipment, experience summary
  - [x] Program length display
  - [x] Generate button calls API
- [x] **4.8** Integrate API calls:
  - [x] `src/api/queries/onboarding.ts` — Config queries (staleTime: Infinity)
  - [x] `src/api/mutations/onboarding.ts` — Validate + generate with error toasts
- [x] **4.9** Persist draft state:
  - [x] Save progress to AppStore via setOnboardingDraft()
  - [x] Restore on return (useState initializers read draft)
  - [x] Clear on completion (clearOnboardingDraft)
- [ ] **4.10** Add form validation:
  - [x] Equipment step blocks Continue if empty
  - [ ] Full Zod schemas per step (deferred — basic validation in place)
  - [ ] Inline error display (deferred)

### 7.2 Onboarding Steps

1. **Goals** — Hierarchical slider configuration
2. **Availability** — Days per week + time allocation
3. **Equipment** — Available equipment selection
4. **Experience** — Fitness level selection
5. **Review** — Confirm and generate program

### 7.3 Acceptance Criteria

- Sliders update normalized values in real-time
- Draft state persists across refresh
- Validation prevents invalid submissions
- Program generates successfully on completion
- User redirected to dashboard after completion

---

## 8. Phase 5: Dashboard & Widgets (COMPLETE)

### 8.1 Tasks

- [x] **5.1** Create dashboard route:
  - [x] `src/routes/_app/dashboard.tsx` — Renders WidgetGrid + AddWidgetModal
  - [ ] Search params for widget layout state (deferred — using AppStore instead)
- [x] **5.2** Create widget registry:
  - [x] `src/components/dashboard/widgets/WidgetRegistry.ts` — Widget defs + lazy imports
  - Note: `src/config/widgets.config.ts` not created separately — config co-located in WidgetRegistry
- [x] **5.3** Create widget grid:
  - [x] `src/components/dashboard/WidgetGrid.tsx`
  - [x] Responsive 2-column grid (lg widgets span 2 cols)
  - [ ] Drag-to-reorder (optional future)
- [x] **5.4** Create base widget wrapper:
  - [x] `src/components/dashboard/widgets/WidgetWrapper.tsx`
  - [x] Loading skeleton
  - [x] Error state (localized with retry)
  - [x] Remove button
- [x] **5.5** Create initial widgets (all code-split via React.lazy):
  - [x] `VolumeLoadChart.tsx` — Bar chart, weekly volume trend
  - [x] `OneRMTrendChart.tsx` — Multi-line chart (Squat/Bench/Deadlift)
  - [x] `SessionCompletionChart.tsx` — Stacked bar (completed/missed)
  - [x] `DisciplineRadarChart.tsx` — Radar chart
- [x] **5.6** Create "Add Widget" modal:
  - [x] `src/components/dashboard/AddWidgetModal.tsx` (Radix Dialog)
  - [x] Lists available widgets from registry
  - [x] Toggle widgets on/off (filters already-added)
- [x] **5.7** Persist widget layout:
  - [x] Store in AppStore.dashboardLayout (persisted to localStorage)

### 8.2 Widget Configuration Schema

```typescript
interface WidgetDefinition {
  id: string;
  name: string;
  description: string;
  component: React.LazyExoticComponent<React.FC>;
  defaultSize: 'sm' | 'md' | 'lg';
  dataSource: string; // Query key
}
```

### 8.3 Acceptance Criteria

- Dashboard renders with default widgets
- Widgets fetch their own data independently
- Failed widget shows localized error (not crash)
- Add widget modal shows available options
- Widget layout persists across sessions

---

## 9. Phase 6: Program & Workout Views (COMPLETE)

### 9.1 Tasks

- [x] **6.1** Create program routes:
  - [x] `src/routes/_app/program/index.tsx` — Program overview (EmptyState when no program)
  - [x] `src/routes/_app/program/$programId.tsx` — Program detail (placeholder for API)
- [x] **6.2** Create session card component:
  - [x] `src/components/program/SessionCard.tsx`
  - [x] Session type badge (colour-coded per type)
  - [x] Duration display
  - [x] Target muscle groups (up to 4 + overflow count)
  - [x] Compact + full variants
  - [ ] Animated GIF support (deferred — requires exercise media assets)
- [x] **6.3** Create week view:
  - [x] `src/components/program/WeekView.tsx`
  - [x] 7-day grid layout with day labels
  - [x] Session cards per day + rest day indicator (Moon icon)
- [x] **6.4** Create program timeline:
  - [x] `src/components/program/ProgramTimeline.tsx`
  - [x] Training blocks with Framer Motion accordion expansion
  - [ ] Current week indicator (deferred — requires active program tracking)
- [x] **6.5** Create workout detail route:
  - [x] `src/routes/_app/workout/$sessionId.tsx`
  - [x] Block list with sets/reps/rest display
  - [x] Collapsible block sections (Framer Motion)
  - [ ] Rest timers (deferred — requires real-time tracking)
  - [ ] Completion tracking (deferred — requires session logging API)
- [x] **6.6** Add collapsible sections:
  - [x] Block details (expandable via AnimatePresence)
  - [x] Block notes display
  - [ ] Progression info (deferred — requires exercise history)

### 9.2 Acceptance Criteria

- Program view shows all training blocks
- Week navigation works smoothly
- Session cards display correct information
- Workout detail shows exercise progression
- Collapsible sections animate smoothly

---

## 10. Phase 7: Workout Builder (COMPLETE)

### 10.1 Tasks

- [x] **7.1** Create workout builder route:
  - [x] `src/routes/_app/workout/builder.$sessionId.tsx`
- [x] **7.2** Set up DnD context:
  - [x] `src/components/workout-builder/BuilderContext.tsx`
  - [x] DndContext with PointerSensor + KeyboardSensor
  - [x] SortableContext with verticalListSortingStrategy
  - [x] React context for exercise state + actions
- [x] **7.3** Create draggable exercise list:
  - [x] `src/components/workout-builder/ExerciseList.tsx`
  - [x] Sortable exercise items (useSortable)
  - [x] Drag handle (GripVertical icon)
  - [x] Remove button per exercise
- [x] **7.4** Create swap panel (inline expansion):
  - [x] `src/components/workout-builder/SwapPanel.tsx`
  - [x] Framer Motion height animation
  - [x] Search-based exercise lookup (mock catalogue)
  - [ ] Auto-swap AI suggestions (deferred — requires AI endpoint)
  - [ ] Virtualized results (deferred — mock list is small)
- [ ] **7.5** Create exercise search:
  - Note: Search is integrated into SwapPanel directly. Standalone ExerciseSearch.tsx not created.
  - [ ] Filter by equipment, muscle group (deferred)
  - [ ] Virtualized results with react-window (deferred)
- [x] **7.6** Wrap in Error Boundary:
  - [x] Route wrapped in `<ErrorBoundary scope="WorkoutBuilder">`
- [x] **7.7** Save draft state:
  - [x] isDirty tracking + Reset button
  - [ ] Auto-save to AppStore (deferred — manual Save button implemented)
  - [ ] Confirm before discarding changes (TODO noted in code)

### 10.2 Acceptance Criteria

- Exercises can be reordered via drag & drop
- Swap button opens inline panel (no page navigation)
- Auto-swap shows relevant alternatives
- Manual search is fast with large exercise library
- DnD crash doesn't break entire app
- Draft state persists

---

## 11. Phase 8: Readiness Logger & Body Map (COMPLETE)

### 11.1 Tasks

- [x] **8.1** Create readiness route:
  - [x] `src/routes/_app/readiness.tsx` — BodyMap + RegionPopover + Save button
- [x] **8.2** Create body map SVG:
  - [x] Single inline SVG with front/back toggle (no external SVG files needed)
  - [x] 15 body regions with simplified polygon paths
- [x] **8.3** Create body map component:
  - [x] `src/components/body-map/BodyMapSVG.tsx`
  - [x] Interactive region paths (click + keyboard accessible)
  - [x] Front/back view toggle (persisted via AppStore)
  - [x] Dynamic fill colors based on severity (green→red heatmap)
  - [x] Body outline with head + torso + limbs
- [x] **8.4** Create region popover:
  - [x] `src/components/body-map/RegionPopover.tsx`
  - [x] Opens on region tap/click
  - [x] Radix Popover for accessibility
- [x] **8.5** Create soreness slider:
  - [x] `src/components/body-map/SorenessSlider.tsx`
  - [x] 0-4 scale with severity colors (Radix Slider)
  - [x] Colour-coded step indicators + severity badge
- [x] **8.6** Map region IDs to body parts:
  - [x] Region definitions co-located in BodyMapSVG.tsx (REGIONS array)
  - [x] Region ID → display name + view (front/back)
  - [x] Severity → colour mapping (SEVERITY_COLORS)
  - Note: `src/config/bodymap.config.ts` not created separately — config co-located with sole consumer
- [ ] **8.7** Persist readiness data:
  - [ ] Save to AppStore (draft) — currently local state, persist deferred
  - [ ] API mutation to submit (deferred — toast placeholder in place)
- [x] **8.8** Add default view preference:
  - [x] Front/back default in AppStore.preferences.defaultBodyMapView

### 11.2 Body Map Regions

```typescript
const BODY_REGIONS = {
  // Front
  'front-neck': { name: 'Neck', group: 'upper' },
  'front-chest': { name: 'Chest', group: 'upper' },
  'front-shoulders': { name: 'Shoulders', group: 'upper' },
  'front-biceps-l': { name: 'Left Bicep', group: 'arms' },
  'front-biceps-r': { name: 'Right Bicep', group: 'arms' },
  'front-abs': { name: 'Abs', group: 'core' },
  'front-quads-l': { name: 'Left Quad', group: 'legs' },
  'front-quads-r': { name: 'Right Quad', group: 'legs' },
  // Back
  'back-traps': { name: 'Traps', group: 'upper' },
  'back-lats': { name: 'Lats', group: 'upper' },
  'back-lower': { name: 'Lower Back', group: 'core' },
  'back-glutes': { name: 'Glutes', group: 'legs' },
  'back-hamstrings-l': { name: 'Left Hamstring', group: 'legs' },
  'back-hamstrings-r': { name: 'Right Hamstring', group: 'legs' },
  // ... etc
} as const;
```

### 11.3 Acceptance Criteria

- Body map renders with all regions tappable
- Front/back toggle works smoothly
- Tapping region opens popover with slider
- Severity colors update dynamically
- Default view preference persists
- Data saves on submit

---

## 12. Phase 9: Settings & Preferences (COMPLETE)

### 12.1 Tasks

- [x] **9.1** Create settings route:
  - [x] `src/routes/_app/settings.tsx` — Full settings page with sections
- [x] **9.2** Create settings sections:
  - [x] **Appearance:** Light/dark segmented picker
  - [x] **Units:** kg/lbs weight, km/miles distance
  - [x] **Defaults:** Body map view (front/back)
  - [ ] **Account:** (Placeholder for Phase 10 auth integration)
  - [ ] **About:** App version, links (deferred)
- [x] **9.3** Create settings components:
  - [x] Section + Row + SegmentedPicker — defined inline in settings route
  - Note: Separate `settings/` component directory not created — components are route-local
- [x] **9.4** Persist all preferences:
  - [x] Sync with AppStore (reads + writes preferences directly)
  - [x] Apply immediately on change
- [x] **9.5** Add reset option:
  - [x] "Reset to defaults" button (calls resetPreferences + toast)

### 12.2 Acceptance Criteria

- All settings persist across sessions
- Theme toggle applies instantly
- Unit changes reflect throughout app
- Reset clears preferences correctly

---

## 13. Phase 10: Authentication Integration

### 13.1 Tasks

- [ ] **10.1** Install Supabase client:
  - [ ] `@supabase/supabase-js`
- [ ] **10.2** Create auth configuration:
  - [ ] `src/config/auth.config.ts`
  - [ ] Environment variables for Supabase
- [ ] **10.3** Create auth context:
  - [ ] `src/contexts/AuthContext.tsx`
  - [ ] Session management
  - [ ] User state
- [ ] **10.4** Create auth routes:
  - [ ] `src/routes/login.tsx`
  - [ ] `src/routes/signup.tsx`
  - [ ] `src/routes/forgot-password.tsx`
- [ ] **10.5** Create auth components:
  - [ ] `src/components/auth/LoginForm.tsx`
  - [ ] `src/components/auth/SignupForm.tsx`
  - [ ] `src/components/auth/SocialLogin.tsx`
- [ ] **10.6** Implement route protection:
  - [ ] Auth guard for protected routes
  - [ ] Redirect logic
- [ ] **10.7** Update navigation:
  - [ ] Show user avatar when logged in
  - [ ] Logout option in dropdown
- [ ] **10.8** Sync onboarding with user:
  - [ ] Link generated program to user ID
  - [ ] Migrate draft state on signup

### 13.2 Acceptance Criteria

- Users can sign up and log in
- Protected routes redirect to login
- Session persists across refresh
- Logout clears session and redirects
- Onboarding data links to user account

---

## 14. Railway Deployment Guide

### 14.1 Overview

TanStack Router uses client-side routing. Railway (or any static host) must be configured to serve `index.html` for all routes, allowing the client-side router to handle navigation.

### 14.2 Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 14.3 Nginx Configuration

Create `frontend/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    server {
        listen 80;
        server_name _;
        root /usr/share/nginx/html;
        index index.html;

        # Gzip compression
        gzip on;
        gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;

        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # SPA fallback - serve index.html for all routes
        location / {
            try_files $uri $uri/ /index.html;
        }

        # API proxy (if frontend and backend on same domain)
        # Uncomment if using Railway's internal networking
        # location /api {
        #     proxy_pass http://backend:8000;
        #     proxy_http_version 1.1;
        #     proxy_set_header Upgrade $http_upgrade;
        #     proxy_set_header Connection 'upgrade';
        #     proxy_set_header Host $host;
        #     proxy_cache_bypass $http_upgrade;
        # }
    }
}
```

### 14.4 Railway Configuration

Create `frontend/railway.toml` (optional, can also configure in Railway dashboard):

```toml
[build]
builder = "dockerfile"
dockerfilePath = "Dockerfile"

[deploy]
healthcheckPath = "/"
healthcheckTimeout = 30
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 3
```

### 14.5 Environment Variables on Railway

Set these in Railway dashboard under your frontend service:

| Variable | Value | Notes |
|----------|-------|-------|
| `VITE_API_BASE_URL` | `https://your-backend.railway.app` | Backend service URL |
| `VITE_SUPABASE_URL` | `https://xxx.supabase.co` | From Supabase dashboard |
| `VITE_SUPABASE_ANON_KEY` | `eyJ...` | From Supabase dashboard |

### 14.6 Build Command Override

If not using Dockerfile, set in Railway:

- **Build Command:** `npm run build`
- **Start Command:** Not applicable (static files served by Railway's CDN)
- **Output Directory:** `dist`

### 14.7 Deployment Checklist

- [x] Create `Dockerfile` in frontend directory (multi-stage: Node 20 build → Nginx 1.27 Alpine)
- [x] Create `nginx.conf` in frontend directory (gzip, immutable caching, SPA fallback, /healthz)
- [ ] Push to GitHub (Railway auto-deploys on push)
- [ ] Set environment variables in Railway dashboard
- [ ] Verify `/dashboard`, `/onboarding/1`, etc. work after deploy
- [ ] Test API connectivity to backend service
- [ ] Enable custom domain (optional)
- [ ] Create `railway.toml` (optional)

---

## 15. Appendix: File Reference

### Phase 1 Files (Complete)

| File | Status |
|------|--------|
| `vite.config.ts` | ✅ Created |
| `src/index.css` | ✅ Created |
| `src/types/enums.ts` | ✅ Created |
| `src/types/onboarding.ts` | ✅ Created |
| `src/types/program.ts` | ✅ Created |
| `src/types/api.ts` | ✅ Created |
| `src/types/index.ts` | ✅ Created |

### Phase 2 Files (Complete)

| File | Status |
|------|--------|
| `src/config/api.config.ts` | ✅ Created |
| `src/config/routes.config.ts` | ✅ Created |
| `src/config/theme.config.ts` | ✅ Created |
| `src/api/client.ts` | ✅ Created |
| `src/api/queryClient.ts` | ✅ Created |
| `src/stores/ui.store.ts` | ✅ Created |
| `src/stores/app.store.ts` | ✅ Created |
| `src/lib/utils.ts` | ✅ Created |
| `src/lib/validators.ts` | ✅ Created |
| `src/routes/__root.tsx` | ✅ Created |
| `src/components/shared/ErrorBoundary.tsx` | ✅ Created |
| `src/components/shared/ErrorFallback.tsx` | ✅ Created |
| `src/components/shared/LoadingSpinner.tsx` | ✅ Created |
| `src/components/shared/EmptyState.tsx` | ✅ Created |
| `.env.example` | ✅ Created |

### Phase 3 Files (Complete)

| File | Status |
|------|--------|
| `src/routes/_app.tsx` | ✅ Created |
| `src/components/layout/AppShell.tsx` | ✅ Created |
| `src/components/layout/Sidebar.tsx` | ✅ Created |
| `src/components/layout/BottomNav.tsx` | ✅ Created |
| `src/components/layout/TopNav.tsx` | ✅ Created |
| `src/components/layout/PageTransition.tsx` | ✅ Created |
| `src/components/layout/ThemeToggle.tsx` | ✅ Created |
| `src/components/ui/button.tsx` | ✅ Created |
| `src/components/ui/card.tsx` | ✅ Created |
| `src/components/ui/badge.tsx` | ✅ Created |
| `src/components/ui/input.tsx` | ✅ Created |
| `src/components/ui/separator.tsx` | ✅ Created |
| `src/components/ui/tooltip.tsx` | ✅ Created |

### Phase 4 Files (Complete)

| File | Status |
|------|--------|
| `src/routes/onboarding.tsx` | ✅ Created |
| `src/routes/onboarding/index.tsx` | ✅ Created |
| `src/routes/onboarding/$step.tsx` | ✅ Created |
| `src/components/onboarding/OnboardingStepper.tsx` | ✅ Created |
| `src/components/onboarding/GoalSliders.tsx` | ✅ Created |
| `src/components/onboarding/AvailabilityPicker.tsx` | ✅ Created |
| `src/components/onboarding/EquipmentSelector.tsx` | ✅ Created |
| `src/components/onboarding/ExperienceSelector.tsx` | ✅ Created |
| `src/api/queries/onboarding.ts` | ✅ Created |
| `src/api/mutations/onboarding.ts` | ✅ Created |

### Phase 5 Files (Complete)

| File | Status |
|------|--------|
| `src/routes/_app/dashboard.tsx` | ✅ Created |
| `src/components/dashboard/WidgetGrid.tsx` | ✅ Created |
| `src/components/dashboard/AddWidgetModal.tsx` | ✅ Created |
| `src/components/dashboard/widgets/WidgetRegistry.ts` | ✅ Created |
| `src/components/dashboard/widgets/WidgetWrapper.tsx` | ✅ Created |
| `src/components/dashboard/widgets/VolumeLoadChart.tsx` | ✅ Created |
| `src/components/dashboard/widgets/OneRMTrendChart.tsx` | ✅ Created |
| `src/components/dashboard/widgets/SessionCompletionChart.tsx` | ✅ Created |
| `src/components/dashboard/widgets/DisciplineRadarChart.tsx` | ✅ Created |

### Phase 6 Files (Complete)

| File | Status |
|------|--------|
| `src/routes/_app/program/index.tsx` | ✅ Created |
| `src/routes/_app/program/$programId.tsx` | ✅ Created |
| `src/routes/_app/workout/$sessionId.tsx` | ✅ Created |
| `src/components/program/SessionCard.tsx` | ✅ Created |
| `src/components/program/WeekView.tsx` | ✅ Created |
| `src/components/program/ProgramTimeline.tsx` | ✅ Created |

### Phase 7 Files (Complete)

| File | Status |
|------|--------|
| `src/routes/_app/workout/builder.$sessionId.tsx` | ✅ Created |
| `src/components/workout-builder/BuilderContext.tsx` | ✅ Created |
| `src/components/workout-builder/ExerciseList.tsx` | ✅ Created |
| `src/components/workout-builder/SwapPanel.tsx` | ✅ Created |

### Phase 8 Files (Complete)

| File | Status |
|------|--------|
| `src/routes/_app/readiness.tsx` | ✅ Created |
| `src/components/body-map/BodyMapSVG.tsx` | ✅ Created |
| `src/components/body-map/RegionPopover.tsx` | ✅ Created |
| `src/components/body-map/SorenessSlider.tsx` | ✅ Created |

### Phase 9 Files (Complete)

| File | Status |
|------|--------|
| `src/routes/_app/settings.tsx` | ✅ Created |

### Deployment Files (Complete)

| File | Status |
|------|--------|
| `Dockerfile` | ✅ Created |
| `nginx.conf` | ✅ Created |

---

## Changelog

| Date | Phase | Changes |
|------|-------|---------|
| 2026-03-01 | Phase 1 | Initial setup complete - Vite, Tailwind, TypeScript types |
| 2026-03-01 | Phase 2 | Core infra: router, query client, stores, utils, validators, error boundary |
| 2026-03-01 | Phase 3 | Layout: AppShell, Sidebar, BottomNav, TopNav, PageTransition, ThemeToggle, UI primitives |
| 2026-03-01 | Phase 4 | Onboarding: 5-step flow with GoalSliders, AvailabilityPicker, EquipmentSelector, ExperienceSelector |
| 2026-03-01 | Phase 5 | Dashboard: WidgetGrid, 4 Recharts widgets (lazy-loaded), AddWidgetModal, layout persistence |
| 2026-03-01 | Phase 6 | Program & Workout: SessionCard, WeekView, ProgramTimeline, workout detail with collapsible blocks |
| 2026-03-01 | Phase 7 | Workout Builder: DnD context, sortable exercise list, swap panel with search |
| 2026-03-01 | Phase 8 | Readiness: Interactive body map SVG (15 regions), severity heatmap, RegionPopover, SorenessSlider |
| 2026-03-01 | Phase 9 | Settings: Theme, units, body map default view, reset to defaults |
| 2026-03-01 | Deployment | Dockerfile (multi-stage Node→Nginx Alpine), nginx.conf (gzip, SPA fallback, /healthz) |

---

*This document is the single source of truth for frontend development. Update task checkboxes and file references as work progresses.*
