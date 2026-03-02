/**
 * Alloy Fitness - Movement Types
 * TypeScript equivalents of the movements table and search API responses.
 */

/** A single movement from the movements table */
export interface Movement {
  id: number;
  name: string;
  primary_muscle: string;
  primary_region: string;
  compound: boolean | null;
  is_complex_lift: boolean | null;
  is_unilateral: boolean | null;
  metric_type: string;
  spinal_compression: string;
  bodyweight_possible: boolean | null;
  dumbbell_possible: boolean | null;
  kettlebell_possible: boolean | null;
  barbell_possible: boolean | null;
  machine_possible: boolean | null;
  band_possible: boolean | null;
  plate_or_med_ball_possible: boolean | null;
  discipline: string | null;
  pattern: string | null;
}

/** Query parameters for movement search */
export interface MovementSearchParams {
  q?: string;
  primary_region?: string[];
  primary_muscle?: string[];
  discipline?: string[];
  compound?: boolean;
  is_complex_lift?: boolean;
  is_unilateral?: boolean;
  metric_type?: string[];
  spinal_compression?: string[];
  equipment?: string[];
  page?: number;
  per_page?: number;
}

/** Paginated response from GET /api/movements/search */
export interface MovementSearchResponse {
  movements: Movement[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

/** Distinct filter values from GET /api/movements/filters */
export interface MovementFilters {
  primary_region: string[];
  primary_muscle: string[];
  discipline: string[];
  metric_type: string[];
  spinal_compression: string[];
  equipment: string[];
}
