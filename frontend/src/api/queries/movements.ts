/**
 * Movement Query Hooks
 * TanStack Query hooks for movement search and filter fetching.
 * Reusable across ExerciseBrowser, workout builder, and any future movement selection UI.
 */

import { useQuery, keepPreviousData } from '@tanstack/react-query';
import { apiClient } from '../client';
import { API_CONFIG } from '../../config/api.config';
import type {
  MovementSearchParams,
  MovementSearchResponse,
  MovementFilters,
} from '../../types/movement';
import type { HyroxSearchResponse, HyroxWorkoutDetail } from '../../types/hyrox';

// ─── Query Keys ──────────────────────────────────────────────────────────────

export const movementKeys = {
  all: ['movements'] as const,
  search: (params: MovementSearchParams) =>
    [...movementKeys.all, 'search', params] as const,
  filters: () => [...movementKeys.all, 'filters'] as const,
};

export const hyroxKeys = {
  all: ['hyrox'] as const,
  search: (params: Record<string, unknown>) =>
    [...hyroxKeys.all, 'search', params] as const,
};

// ─── Movement Search ─────────────────────────────────────────────────────────

/** Build query string from MovementSearchParams */
function buildMovementQueryString(params: MovementSearchParams): string {
  const searchParams = new URLSearchParams();

  if (params.q) searchParams.set('q', params.q);

  // Multi-select enum filters — repeated query params
  const multiFields = [
    'primary_region', 'primary_muscle', 'discipline', 'metric_type', 'spinal_compression',
  ] as const;
  for (const field of multiFields) {
    const values = params[field];
    if (values && values.length > 0) {
      for (const v of values) searchParams.append(field, v);
    }
  }

  if (params.compound !== undefined) searchParams.set('compound', String(params.compound));
  if (params.is_complex_lift !== undefined) searchParams.set('is_complex_lift', String(params.is_complex_lift));
  if (params.is_unilateral !== undefined) searchParams.set('is_unilateral', String(params.is_unilateral));
  if (params.equipment) {
    for (const eq of params.equipment) {
      searchParams.append('equipment', eq);
    }
  }
  searchParams.set('page', String(params.page ?? 1));
  searchParams.set('per_page', String(params.per_page ?? 20));

  return searchParams.toString();
}

/**
 * Search movements with optional filters.
 * Uses keepPreviousData for smooth pagination transitions.
 */
export function useMovementSearch(params: MovementSearchParams, enabled = true) {
  return useQuery({
    queryKey: movementKeys.search(params),
    queryFn: () => {
      const qs = buildMovementQueryString(params);
      return apiClient.get<MovementSearchResponse>(
        `${API_CONFIG.endpoints.movements.search}?${qs}`
      );
    },
    placeholderData: keepPreviousData,
    staleTime: API_CONFIG.query.staleTime,
    enabled,
  });
}

// ─── Movement Filters ────────────────────────────────────────────────────────

/**
 * Fetch distinct filter values for movement dropdowns.
 * Cached with long staleTime since filter options rarely change.
 */
export function useMovementFilters() {
  return useQuery({
    queryKey: movementKeys.filters(),
    queryFn: () =>
      apiClient.get<MovementFilters>(API_CONFIG.endpoints.movements.filters),
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
}

// ─── Hyrox Circuit Search ────────────────────────────────────────────────────

interface HyroxSearchParams {
  workout_type?: string;
  min_duration?: number;
  max_duration?: number;
  is_complex?: boolean;
  has_mini_circuit?: boolean;
  includes?: string[];
  excludes?: string[];
  page?: number;
  per_page?: number;
}

function buildHyroxQueryString(params: HyroxSearchParams): string {
  const searchParams = new URLSearchParams();

  if (params.workout_type) searchParams.set('workout_type', params.workout_type);
  if (params.min_duration !== undefined) searchParams.set('min_duration', String(params.min_duration));
  if (params.max_duration !== undefined) searchParams.set('max_duration', String(params.max_duration));
  if (params.is_complex !== undefined) searchParams.set('is_complex', String(params.is_complex));
  if (params.has_mini_circuit !== undefined) searchParams.set('has_mini_circuit', String(params.has_mini_circuit));
  if (params.includes && params.includes.length > 0) {
    for (const name of params.includes) searchParams.append('includes', name);
  }
  if (params.excludes && params.excludes.length > 0) {
    for (const name of params.excludes) searchParams.append('excludes', name);
  }
  searchParams.set('page', String(params.page ?? 1));
  searchParams.set('per_page', String(params.per_page ?? 20));

  return searchParams.toString();
}

/**
 * Search Hyrox circuits/workouts with optional filters.
 */
export function useHyroxSearch(params: HyroxSearchParams, enabled = true) {
  return useQuery({
    queryKey: hyroxKeys.search(params as Record<string, unknown>),
    queryFn: () => {
      const qs = buildHyroxQueryString(params);
      return apiClient.get<HyroxSearchResponse>(
        `${API_CONFIG.endpoints.hyrox.workouts}?${qs}`
      );
    },
    placeholderData: keepPreviousData,
    staleTime: API_CONFIG.query.staleTime,
    enabled,
  });
}

// ─── Hyrox Workout Detail ────────────────────────────────────────────────

/**
 * Fetch full Hyrox workout detail (lines + mini circuits).
 * Used when a user clicks a circuit card to view the full workout.
 */
export function useHyroxWorkoutDetail(workoutId: number | null) {
  return useQuery({
    queryKey: [...hyroxKeys.all, 'detail', workoutId] as const,
    queryFn: () =>
      apiClient.get<HyroxWorkoutDetail>(
        API_CONFIG.endpoints.hyrox.workoutDetail(workoutId!)
      ),
    enabled: workoutId != null,
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
}

// ─── Hyrox Movement Names ───────────────────────────────────────────────

/**
 * Fetch distinct movement names from Hyrox workout lines.
 * Used for the "Includes" filter in CircuitSearchTab.
 */
export function useHyroxMovements() {
  return useQuery({
    queryKey: [...hyroxKeys.all, 'movements'] as const,
    queryFn: () =>
      apiClient.get<{ movement_names: string[] }>(API_CONFIG.endpoints.hyrox.movements),
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
}
