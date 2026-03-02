/**
 * Index Route (/)
 * Redirects to /dashboard. This is the app's default entry point.
 */

import { createFileRoute, redirect } from '@tanstack/react-router';

export const Route = createFileRoute('/')({
  beforeLoad: () => {
    throw redirect({ to: '/dashboard' });
  },
});
