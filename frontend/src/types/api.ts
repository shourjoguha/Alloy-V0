/**
 * Alloy Fitness - API Types
 * Standardized API response wrappers and error handling
 */

/** Pagination metadata for list responses */
export interface PaginationMeta {
  /** Current page number (1-indexed) */
  page: number;
  /** Number of items per page */
  per_page: number;
  /** Total number of items */
  total: number;
  /** Total number of pages */
  total_pages: number;
  /** Whether there are more pages */
  has_next: boolean;
  /** Whether there are previous pages */
  has_prev: boolean;
}

/** Standardized API error structure */
export interface ApiError {
  /** Error code (e.g., 'VALIDATION_ERROR', 'HTTP_400') */
  code: string;
  /** Human-readable error message */
  message: string;
  /** Trace ID for debugging/support */
  trace_id?: string;
  /** HTTP status code (set by client, not always in response) */
  status_code?: number;
}


/** API health check response */
export interface HealthCheckResponse {
  status: 'healthy' | 'unhealthy';
  service: string;
  version: string;
  timestamp: string;
}

/** Slider configuration from API */
export interface SliderConfig {
  name: string;
  range: [number, number];
  description: string;
}

/** Slider configuration response from GET /api/onboarding/config/sliders */
export interface SliderConfigResponse {
  primary_slider: SliderConfig;
  secondary_sliders: SliderConfig[];
  constraints: {
    min_value: number;
    max_value: number;
    normalization_enabled: boolean;
    hierarchical_influence: boolean;
  };
}

/** Time allocation configuration response */
export interface TimeAllocationConfigResponse {
  default_session_time: number;
  min_session_time: number;
  max_session_time: number;
  options: {
    apply_to_all_days: string;
    custom_per_day: string;
    delegate_to_system: string;
  };
  optimization_factors: string[];
}

/** API info response from GET /api/info */
export interface ApiInfoResponse {
  name: string;
  version: string;
  description: string;
  endpoints: {
    onboarding: Record<string, string>;
    system: Record<string, string>;
  };
  features: string[];
}

