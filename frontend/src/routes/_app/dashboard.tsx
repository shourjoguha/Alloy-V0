/**
 * Dashboard Route (/dashboard)
 * Main dashboard with week navigation, workout selection, stats, and exercise browser.
 */

import { useMemo } from 'react';
import { createFileRoute, useNavigate } from '@tanstack/react-router';
import { Plus } from 'lucide-react';
import { PageContainer } from '../../components/layout/PageContainer';
import { ErrorBoundary } from '../../components/shared/ErrorBoundary';
import { EmptyState } from '../../components/shared/EmptyState';
import { WeekNavigator } from '../../components/dashboard/WeekNavigator';
import { WorkoutSelector } from '../../components/dashboard/WorkoutSelector';
import { WorkoutPreview } from '../../components/dashboard/WorkoutPreview';
import { ActionRow } from '../../components/dashboard/ActionRow';
import { DashboardStats } from '../../components/dashboard/DashboardStats';
import { SocialStats } from '../../components/dashboard/SocialStats';
import { ActivityStats } from '../../components/dashboard/ActivityStats';
import { ExerciseBrowser } from '../../components/exercise-browser/ExerciseBrowser';
import { useAppStore } from '../../stores/app.store';
import { useUIStore } from '../../stores/ui.store';
import { Dumbbell, Users } from 'lucide-react';
import { cn } from '../../lib/utils';
import type { WeeklyPlan } from '../../types/program';

export const Route = createFileRoute('/_app/dashboard')({
  component: () => (
    <ErrorBoundary scope="Dashboard">
      <DashboardPage />
    </ErrorBoundary>
  ),
});

/** Flatten all weekly plans across training blocks */
function useFlatWeeks() {
  const program = useAppStore((s) => s.activeProgram);
  return useMemo(() => {
    if (!program) return [];
    const weeks: WeeklyPlan[] = [];
    for (const block of program.training_blocks) {
      for (const week of block.weekly_plans) {
        weeks.push(week);
      }
    }
    return weeks;
  }, [program]);
}

function DashboardPage() {
  const navigate = useNavigate();
  const activeProgram = useAppStore((s) => s.activeProgram);
  const selectedTab = useUIStore((s) => s.selectedDashboardTab);
  const selectedWeekIndex = useUIStore((s) => s.selectedWeekIndex);
  const selectedDayIndex = useUIStore((s) => s.selectedDayIndex);
  const flatWeeks = useFlatWeeks();

  const currentWeek = flatWeeks[selectedWeekIndex];
  const sessions = currentWeek?.sessions ?? [];
  const selectedSession = selectedDayIndex !== null ? sessions[selectedDayIndex] : null;

  // Squads tab — show "Coming Soon" placeholder
  if (selectedTab === 'squads') {
    return (
      <PageContainer>
        <div className="flex flex-col items-center justify-center py-24 text-center animate-fade-in">
          <div className="flex items-center justify-center w-14 h-14 rounded-2xl bg-surface-100 dark:bg-surface-800 mb-4">
            <Users className="w-7 h-7 text-surface-400" />
          </div>
          <h2 className="text-lg font-semibold text-surface-800 dark:text-surface-200 mb-1">
            Squads
          </h2>
          <p className="text-sm text-surface-400">
            Coming soon
          </p>
        </div>
      </PageContainer>
    );
  }

  // No active program — show empty state with CTA
  if (!activeProgram) {
    return (
      <PageContainer>
        <EmptyState
          icon={Dumbbell}
          title="No program yet"
          description="Create a personalised training program to get started."
          action={{
            label: 'Create Program',
            onClick: () => navigate({ to: '/onboarding' }),
          }}
        />
        <ExerciseBrowser />
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <div className="space-y-4 animate-fade-in">
        {/* Week navigator */}
        <WeekNavigator program={activeProgram} />

        {/* Workout selector CTA + day pills */}
        <WorkoutSelector sessions={sessions} />

        {/* Action row: Adapt Session, New Program, icons */}
        <ActionRow />

        {/* Log Custom Workout button */}
        <button
          type="button"
          className={cn(
            'w-full flex items-center justify-center gap-2 py-3 rounded-xl',
            'text-sm font-medium transition-colors',
            'bg-white dark:bg-surface-900 border border-amber-accent/40',
            'text-surface-600 dark:text-surface-400',
            'hover:border-amber-accent hover:bg-amber-accent-muted'
          )}
        >
          <Plus className="w-4 h-4" />
          Log Custom Workout
        </button>

        {/* Selected workout preview */}
        {selectedSession && <WorkoutPreview session={selectedSession} />}

        {/* Stats: Heaviest Lift, Longest Workout, Total Volume */}
        <DashboardStats />

        {/* Social stats */}
        <SocialStats />

        {/* Activity stats: Workouts Done, Streak, Adherence */}
        <ActivityStats />
      </div>

      {/* Exercise Browser modal (rendered globally) */}
      <ExerciseBrowser />
    </PageContainer>
  );
}
