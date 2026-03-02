/**
 * API Client
 * Typed fetch wrapper. All requests go through here.
 * - Builds full URL from API_CONFIG.baseURL
 * - Transforms error responses into structured ApiError objects
 * - Dev-only request/response console logging
 */

import { API_CONFIG } from '../config/api.config';
import type { ApiError } from '../types/api';

const IS_DEV = import.meta.env.DEV;

// ─── Types ──────────────────────────────────────────────────────────────────

export interface RequestOptions extends Omit<RequestInit, 'body'> {
  body?: unknown;
  /** Override the base URL for a single request */
  baseURL?: string;
  /** Timeout in ms — defaults to API_CONFIG.timeout */
  timeout?: number;
}

export class ApiClientError extends Error {
  public readonly apiError: ApiError;
  public readonly status: number;

  constructor(apiError: ApiError, status?: number) {
    super(apiError.message);
    this.name = 'ApiClientError';
    this.apiError = apiError;
    this.status = status ?? apiError.status_code ?? 0;
  }
}

// ─── Core Request ────────────────────────────────────────────────────────────

async function request<T>(
  path: string,
  options: RequestOptions = {}
): Promise<T> {
  const {
    body,
    baseURL = API_CONFIG.baseURL,
    timeout = API_CONFIG.timeout,
    headers: customHeaders,
    ...rest
  } = options;

  const url = `${baseURL}${path}`;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    Accept: 'application/json',
    ...(customHeaders as Record<string, string>),
  };

  const controller = new AbortController();
  const timerId = setTimeout(() => controller.abort(), timeout);

  if (IS_DEV) {
    console.group(`[API] ${rest.method ?? 'GET'} ${path}`);
    if (body !== undefined) console.log('Request body:', body);
  }

  try {
    const response = await fetch(url, {
      ...rest,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
      signal: controller.signal,
    });

    // Parse response body (all responses are JSON)
    let data: unknown;
    const contentType = response.headers.get('content-type') ?? '';
    if (contentType.includes('application/json')) {
      data = await response.json();
    } else {
      data = await response.text();
    }

    if (IS_DEV) {
      console.log('Status:', response.status);
      console.log('Response:', data);
      console.groupEnd();
    }

    if (!response.ok) {
      // Backend returns { error: { code, message, trace_id } } on failures
      const errorPayload =
        typeof data === 'object' && data !== null && 'error' in data
          ? (data as { error: ApiError }).error
          : { code: 'HTTP_ERROR', message: `Request failed (${response.status})` };

      throw new ApiClientError(errorPayload as ApiError, response.status);
    }

    return data as T;
  } catch (err) {
    if (IS_DEV) console.groupEnd();

    if (err instanceof ApiClientError) throw err;

    if (err instanceof DOMException && err.name === 'AbortError') {
      throw new ApiClientError({ code: 'REQUEST_TIMEOUT', message: 'Request timed out' }, 408);
    }

    // Network-level errors
    const isFailedToFetch = err instanceof TypeError && err.message === 'Failed to fetch';
    throw new ApiClientError(
      {
        code: isFailedToFetch ? 'CONNECTION_REFUSED' : 'NETWORK_ERROR',
        message: isFailedToFetch ? 'Unable to connect to server' : 'Network error',
      },
      0
    );
  } finally {
    clearTimeout(timerId);
  }
}

// ─── Public API ──────────────────────────────────────────────────────────────

export const apiClient = {
  get: <T>(path: string, options?: RequestOptions) =>
    request<T>(path, { ...options, method: 'GET' }),

  post: <T>(path: string, body?: unknown, options?: RequestOptions) =>
    request<T>(path, { ...options, method: 'POST', body }),

  put: <T>(path: string, body?: unknown, options?: RequestOptions) =>
    request<T>(path, { ...options, method: 'PUT', body }),

  patch: <T>(path: string, body?: unknown, options?: RequestOptions) =>
    request<T>(path, { ...options, method: 'PATCH', body }),

  delete: <T>(path: string, options?: RequestOptions) =>
    request<T>(path, { ...options, method: 'DELETE' }),
};
