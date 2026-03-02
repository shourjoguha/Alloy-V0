/**
 * Routes Configuration
 * Single source of truth for all route path strings.
 * Import from here instead of ever writing path strings inline.
 */

export const ROUTES = {
  HOME: '/',
  DASHBOARD: '/dashboard',

  ONBOARDING: '/onboarding',
  ONBOARDING_STEP: '/onboarding/$step',

  PROGRAM: '/program',
  PROGRAM_DETAIL: '/program/$programId',

  WORKOUT: '/workout/$sessionId',
  WORKOUT_BUILDER: '/workout/builder/$sessionId',

  READINESS: '/readiness',
  SETTINGS: '/settings',

  // Auth — added in Phase 10
  LOGIN: '/login',
  SIGNUP: '/signup',
  FORGOT_PASSWORD: '/forgot-password',
} as const;

export type RoutePath = (typeof ROUTES)[keyof typeof ROUTES];
