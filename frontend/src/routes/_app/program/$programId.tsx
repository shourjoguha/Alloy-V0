/**
 * /program/:programId — Program detail view
 */

import { createFileRoute } from '@tanstack/react-router';
import { PageContainer } from '../../../components/layout/PageContainer';
import { ErrorBoundary } from '../../../components/shared/ErrorBoundary';

export const Route = createFileRoute('/_app/program/$programId')({
  component: () => (
    <ErrorBoundary scope="ProgramDetail">
      <ProgramDetailPage />
    </ErrorBoundary>
  ),
});

function ProgramDetailPage() {
  const { programId } = Route.useParams();

  return (
    <PageContainer>
      <div className="mb-5">
        <h1 className="text-lg font-semibold text-surface-900 dark:text-surface-50">
          Program Detail
        </h1>
        <p className="text-sm text-surface-400 mt-0.5">ID: {programId}</p>
      </div>
      {/* TODO: Fetch and display specific program when program API is available */}
    </PageContainer>
  );
}
