/**
 * /program — Current program overview
 */

import { createFileRoute, useNavigate } from '@tanstack/react-router';
import { PageContainer } from '../../../components/layout/PageContainer';
import { ErrorBoundary } from '../../../components/shared/ErrorBoundary';
import { ProgramTimeline } from '../../../components/program/ProgramTimeline';
import { EmptyState } from '../../../components/shared/EmptyState';
import { useAppStore } from '../../../stores/app.store';
import { Dumbbell } from 'lucide-react';

export const Route = createFileRoute('/_app/program/')({
  component: () => (
    <ErrorBoundary scope="Program">
      <ProgramPage />
    </ErrorBoundary>
  ),
});

function ProgramPage() {
  const navigate = useNavigate();
  const activeProgram = useAppStore((s) => s.activeProgram);

  if (!activeProgram) {
    return (
      <PageContainer>
        <div className="mb-5">
          <h1 className="text-lg font-semibold text-surface-900 dark:text-surface-50">
            My Program
          </h1>
          <p className="text-sm text-surface-400 mt-0.5">
            Your active training plan
          </p>
        </div>

        <EmptyState
          icon={Dumbbell}
          title="No program yet"
          description="Complete the setup flow to generate your personalised program."
          action={{
            label: 'Start setup',
            onClick: () => navigate({ to: '/onboarding' }),
          }}
        />
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <div className="mb-5">
        <h1 className="text-lg font-semibold text-surface-900 dark:text-surface-50">
          {activeProgram.program_name}
        </h1>
        <p className="text-sm text-surface-400 mt-0.5">
          {activeProgram.total_weeks} weeks · {activeProgram.total_sessions} sessions
        </p>
      </div>

      <ProgramTimeline
        program={activeProgram}
        onSessionClick={(sessionId) =>
          navigate({
            to: '/workout/$sessionId',
            params: { sessionId },
          })
        }
      />
    </PageContainer>
  );
}
