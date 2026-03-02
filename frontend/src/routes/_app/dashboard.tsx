/**
 * Dashboard Route (/dashboard)
 * Performance overview with stat cards and customisable widget grid.
 */

import { createFileRoute } from '@tanstack/react-router';
import { PageContainer } from '../../components/layout/PageContainer';
import { ErrorBoundary } from '../../components/shared/ErrorBoundary';
import { WidgetGrid } from '../../components/dashboard/WidgetGrid';
import { AddWidgetModal } from '../../components/dashboard/AddWidgetModal';
import { StatCard } from '../../components/dashboard/StatCard';

export const Route = createFileRoute('/_app/dashboard')({
  component: () => (
    <ErrorBoundary scope="Dashboard">
      <DashboardPage />
    </ErrorBoundary>
  ),
});

/** Mock stat data — replace with TanStack Query hooks when API is ready */
const STAT_CARDS = [
  { value: '—', label: 'Heaviest Lift', sublabel: 'No data yet' },
  { value: '0', label: 'Workouts Done' },
  { value: '—', label: 'Adherence' },
] as const;

function DashboardPage() {
  return (
    <PageContainer>
      <div className="mb-5">
        <h1 className="text-lg font-semibold text-surface-900 dark:text-surface-50">
          Dashboard
        </h1>
        <p className="text-sm text-surface-400 mt-0.5">Your training at a glance</p>
      </div>

      {/* Glanceable KPI stat cards */}
      <div className="grid grid-cols-3 gap-3 mb-5 animate-fade-in">
        {STAT_CARDS.map((stat) => (
          <StatCard
            key={stat.label}
            value={stat.value}
            label={stat.label}
            sublabel={'sublabel' in stat ? stat.sublabel : undefined}
          />
        ))}
      </div>

      <WidgetGrid />
      <AddWidgetModal />
    </PageContainer>
  );
}
