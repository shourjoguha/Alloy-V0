/**
 * /onboarding → redirect to /onboarding/1
 */

import { createFileRoute, redirect } from '@tanstack/react-router';

export const Route = createFileRoute('/onboarding/')({
  beforeLoad: () => {
    throw redirect({ to: '/onboarding/$step', params: { step: '1' } });
  },
});
