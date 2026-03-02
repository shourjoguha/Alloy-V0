# Frontend Architecture & Product Requirements Document (PRD) v2
**Project:** Smart Fitness Program Generator SaaS
**Backend Context:** Python (FastAPI) + PostgreSQL + LLM Integration
**Target Platforms:** Responsive Web (Mobile-first handheld scaling up to Desktop monitors)
**Hosting & Auth:** Railway (Hosting) + Supabase Auth (Authentication)

## 1. Core Philosophy & Agent Instructions
- **Role:** You are an expert Frontend Developer and UX Architect.
- **Goal:** Build a sleek, modern, highly modular React/TypeScript frontend for a multi-discipline fitness application.
- **Modularity (Strict Rule):** The system must be highly decoupled. Changing a UI element in one place MUST NOT break another. Use Error Boundaries around major widgets/sections. Components must have strict, well-typed interfaces.
- **Design Language:** Minimalist, highly functional, data-dense but uncluttered. Use sleek vector icons (`lucide-react`). No emojis.
- **Responsiveness:** Fluid scaling via Tailwind CSS (`flex`, `grid`). Elements must not overflow. Aspect ratios must be maintained across devices.
- **Future-Proofing (Offline):** Build data fetching using `TanStack Query` (React Query). This provides immediate caching and sets the exact foundation needed to easily implement full Offline/PWA functionality later without rewriting the data layer.

## 2. Tech Stack Recommendations
- **Framework:** React + TypeScript (via Vite)
- **Styling & Global Config:** Tailwind CSS (Single source of truth for all design tokens).
- **Animations/Transitions:** Framer Motion (for smooth page transitions, inline expansions, and swipe-to-close gestures).
- **Icons:** `lucide-react`
- **Data Fetching & State:** TanStack Query (Server state/caching) + Zustand (Lightweight global UI state).
- **Drag & Drop:** `@dnd-kit/core`
- **Charts:** `recharts` (for composable, responsive React charts) + `react-chartjs-2` (if advanced radar charts are needed).

## 3. Global Configuration & Standardization
All UI dimensions, typography, and colors MUST be config-driven.
- **Theme Config:** `tailwind.config.js` will define specific font size ranges, border radii, and a semantic color palette (Primary, Secondary, Surface, Heatmap-Severity).
- **API Contracts:** Standardize response wrappers (e.g., `{ data, meta: { pagination }, error }`).

## 4. Key Views & Component Architecture

### A. Performance View & Dashboard (Plug-and-Play Architecture)
- **Requirement:** A highly modular, customizable dashboard. Users get default charts (e.g., volume load, 1RM trends) and can click a "+" button to add more.
- **Agent Instruction for Charts Directory:**
  - Create a `/src/components/dashboard/widgets` directory.
  - Every chart must be an isolated component that fetches or selects its own specific data slice.
  - Maintain a `WidgetRegistry.ts` that maps widget IDs to their components. When a new chart is added to the repo, it is simply registered here, and the "+" modal automatically populates it as an option for the user.
  - **Visuals:** Must support both basic line/bar charts and multi-disciplinary Radar charts (mapping Cardio vs. Strength vs. Mobility).

### B. Program & Workout Viewer (List & Cards)
- **Requirement:** Clean, uncluttered cards displaying upcoming sessions. 
- **Media:** Cards must support looping animated GIFs (for movement demos) replacing static logos.
- **Horizontal Scrolling:** Use subtle tiny dot indicators for horizontally scrolling image galleries or sets.

### C. Workout Builder & Inline Swapping
- **Drag & Drop:** Users can reorder exercises *within a specific day*. Use `@dnd-kit/sortable` for list reordering.
- **The Swap Mechanism (Crucial UX):** 
  - Exercises have a `Swap` button. 
  - **Interaction:** Clicking Swap MUST NOT open a new page. It should trigger an inline Framer Motion expansion (e.g., an accordion drop-down or a sleek bottom-sheet on mobile).
  - **Options inside Swap:**
    1. *Auto-Swap:* System/AI instantly recommends 1-3 direct alternatives (e.g., Barbell Squat -> Goblet Squat).
    2. *Manual-Swap:* A searchable, virtualized list of the exercise library.

### D. Readiness Logger & Body Map
- **MVP Requirement:** A highly polished 2D interactive SVG human body map (Front and Back views).
- **Interaction:** Users can tap regions (Lower Back, Right Shoulder). 
- **Input:** Tapping a region opens a sleek popover with a 1-5 slider to log soreness/injury severity. Colors on the 2D map update dynamically based on severity (e.g., Yellow -> Red).

## 5. UI/UX & Navigation Standards
- **Mobile Navigation:** Bottom bar navigation for core routes. Modal detail views must be full-screen with a "Swipe Down to Close" gesture or prominent "X".
- **Desktop Navigation:** Sidebar or Top Navbar.
- **Menu:** Hamburger menu or expandable profile avatar (top right/left) for settings.
- **Transitions:** Smooth page-to-page transitions (fade in/out, slide).
- **Collapsible Sections:** Any subsection with secondary information must be wrapped in a smooth collapsible accordion to prevent visual clutter.
