/**
 * /readiness — Readiness Logger with Body Map
 */

import { createFileRoute } from '@tanstack/react-router';
import { useState } from 'react';
import { toast } from 'sonner';
import { Save } from 'lucide-react';
import { PageContainer } from '../../components/layout/PageContainer';
import { ErrorBoundary } from '../../components/shared/ErrorBoundary';
import { BodyMapSVG } from '../../components/body-map/BodyMapSVG';
import { type BodyRegionId, type SeverityLevel } from '../../config/bodymap.config';
import { RegionPopover } from '../../components/body-map/RegionPopover';

export const Route = createFileRoute('/_app/readiness')({
  component: () => (
    <ErrorBoundary scope="Readiness">
      <ReadinessPage />
    </ErrorBoundary>
  ),
});

function ReadinessPage() {
  const [sorenessMap, setSorenessMap] = useState<Partial<Record<BodyRegionId, SeverityLevel>>>({});
  const [selectedRegion, setSelectedRegion] = useState<BodyRegionId | null>(null);

  function handleRegionClick(regionId: BodyRegionId) {
    setSelectedRegion(regionId);
  }

  function handleSeverityChange(value: SeverityLevel) {
    if (!selectedRegion) return;
    setSorenessMap((prev) => ({
      ...prev,
      [selectedRegion]: value,
    }));
  }

  function handleSave() {
    // TODO: POST soreness data to API
    toast.success('Readiness logged');
  }

  const hasSorenessData = Object.values(sorenessMap).some((v) => v != null && v > 0);

  return (
    <PageContainer>
      <div className="flex items-center justify-between mb-5">
        <div>
          <h1 className="text-lg font-semibold text-surface-900 dark:text-surface-50">
            Readiness
          </h1>
          <p className="text-sm text-surface-400 mt-0.5">
            Tap a region to log muscle soreness
          </p>
        </div>
        <button
          type="button"
          onClick={handleSave}
          disabled={!hasSorenessData}
          className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg text-xs font-semibold bg-primary-600 hover:bg-primary-700 text-white transition-colors disabled:bg-surface-200 dark:disabled:bg-surface-800 disabled:text-surface-400 disabled:cursor-not-allowed"
        >
          <Save className="w-3 h-3" />
          Save
        </button>
      </div>

      <BodyMapSVG
        sorenessMap={sorenessMap}
        onRegionClick={handleRegionClick}
        className="mx-auto"
      />

      <RegionPopover
        open={selectedRegion !== null}
        regionId={selectedRegion}
        severity={selectedRegion ? sorenessMap[selectedRegion] ?? 0 : 0}
        onSeverityChange={handleSeverityChange}
        onClose={() => setSelectedRegion(null)}
      />

      {/* Severity legend */}
      <div className="mt-6 flex items-center justify-center gap-4 text-xs text-surface-400">
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-green-500" /> None
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-lime-500" /> Mild
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-yellow-500" /> Moderate
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-orange-500" /> High
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-red-500" /> Severe
        </span>
      </div>
    </PageContainer>
  );
}
