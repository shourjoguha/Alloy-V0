/**
 * Onboarding Mutation Hooks
 */

import { useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';
import { apiClient } from '../client';
import { API_CONFIG } from '../../config/api.config';
import { ApiClientError } from '../client';
import type { OnboardingRequest, OnboardingResponse } from '../../types/onboarding';
import type { ProgramGenerationResponse } from '../../types/program';

export function useValidateSliders() {
  return useMutation({
    mutationFn: (data: OnboardingRequest) =>
      apiClient.post<OnboardingResponse>(
        API_CONFIG.endpoints.onboarding.validateSliders,
        data
      ),
    onError: (err) => {
      const msg =
        err instanceof ApiClientError ? err.apiError.message : 'Validation failed';
      toast.error(msg);
    },
  });
}

export function useGenerateProgram() {
  return useMutation({
    mutationFn: (data: OnboardingRequest) =>
      apiClient.post<ProgramGenerationResponse>(
        API_CONFIG.endpoints.onboarding.generateProgram,
        data
      ),
    // NOTE: Error handling is done in the component (handleGenerate) to provide
    // richer context like trace_id. Do NOT add onError here to avoid duplicate toasts.
  });
}
