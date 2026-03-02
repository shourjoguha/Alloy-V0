/**
 * API Configuration
 * Single source of truth for all API URLs, timeouts, and endpoint paths.
 * All values sourced from environment variables — never hardcoded.
 */

export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000',
  timeout: 30_000,

  endpoints: {
    onboarding: {
      validateSliders: '/api/onboarding/validate-sliders',
      generateProgram: '/api/onboarding/generate-program',
      health: '/api/onboarding/health',
      configSliders: '/api/onboarding/config/sliders',
      configTimeAllocation: '/api/onboarding/config/time-allocation',
    },
    hyrox: {
      workouts: '/api/hyrox/workouts',
      movements: '/api/hyrox/movements',
      workoutDetail: (id: number) => `/api/hyrox/workouts/${id}`,
      recommend: '/api/hyrox/workouts/recommend',
      health: '/api/hyrox/health',
    },
    movements: {
      search: '/api/movements/search',
      filters: '/api/movements/filters',
      health: '/api/movements/health',
    },
    system: {
      health: '/health',
      info: '/api/info',
    },
  },

  /** TanStack Query defaults */
  query: {
    staleTime: 5 * 60 * 1000,        // 5 minutes
    gcTime: 10 * 60 * 1000,          // 10 minutes (formerly cacheTime)
    retryCount: 2,
    retryDelay: (attempt: number) => Math.min(1000 * 2 ** attempt, 30_000),
  },
} as const;
