/**
 * _app Layout Route (pathless)
 * Wraps all authenticated pages with AppShell.
 * The `_` prefix means this route adds no segment to the URL.
 *
 * All pages that should have the sidebar/nav live under src/routes/_app/
 */

import { createFileRoute } from '@tanstack/react-router';
import { AppShell } from '../components/layout/AppShell';
import { ErrorBoundary } from '../components/shared/ErrorBoundary';
import { PageLoader } from '../components/shared/LoadingSpinner';

export const Route = createFileRoute('/_app')({
  pendingComponent: PageLoader,
  component: () => (
    <ErrorBoundary scope="AppShell">
      <AppShell />
    </ErrorBoundary>
  ),
});
