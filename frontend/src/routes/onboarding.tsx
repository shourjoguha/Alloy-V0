/**
 * Onboarding Layout Route
 * Full-screen layout for the onboarding flow.
 * No AppShell — this is pre-auth UX.
 */

import { createFileRoute, Outlet } from '@tanstack/react-router';

export const Route = createFileRoute('/onboarding')({
  component: OnboardingLayout,
});

function OnboardingLayout() {
  return (
    <div className="min-h-screen bg-surface-50 dark:bg-surface-950 flex flex-col">
      <Outlet />
    </div>
  );
}
