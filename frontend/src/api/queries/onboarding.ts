/**
 * Onboarding Query Hooks
 * Config fetchers — cached, rarely change.
 */

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../client';
import { API_CONFIG } from '../../config/api.config';
import type { SliderConfigResponse, TimeAllocationConfigResponse } from '../../types/api';

export const onboardingKeys = {
  all: ['onboarding'] as const,
  sliderConfig: () => [...onboardingKeys.all, 'slider-config'] as const,
  timeConfig: () => [...onboardingKeys.all, 'time-config'] as const,
};

export function useSliderConfig() {
  return useQuery({
    queryKey: onboardingKeys.sliderConfig(),
    queryFn: () =>
      apiClient.get<SliderConfigResponse>(API_CONFIG.endpoints.onboarding.configSliders),
    staleTime: Infinity, // Config rarely changes
  });
}

export function useTimeAllocationConfig() {
  return useQuery({
    queryKey: onboardingKeys.timeConfig(),
    queryFn: () =>
      apiClient.get<TimeAllocationConfigResponse>(
        API_CONFIG.endpoints.onboarding.configTimeAllocation
      ),
    staleTime: Infinity,
  });
}
