/**
 * TanStack QueryClient
 * Centralized query client with tuned defaults.
 * Import this singleton wherever QueryClientProvider is needed.
 */

import { QueryClient } from '@tanstack/react-query';
import { API_CONFIG } from '../config/api.config';
import { ApiClientError } from './client';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: API_CONFIG.query.staleTime,
      gcTime: API_CONFIG.query.gcTime,
      retry: (failureCount, error) => {
        // Don't retry on 4xx client errors — they won't self-resolve
        if (error instanceof ApiClientError && error.status >= 400 && error.status < 500) {
          return false;
        }
        return failureCount < API_CONFIG.query.retryCount;
      },
      retryDelay: API_CONFIG.query.retryDelay,
      refetchOnWindowFocus: true,
      refetchOnReconnect: true,
    },
    mutations: {
      retry: false,
    },
  },
});
