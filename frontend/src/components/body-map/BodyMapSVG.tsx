/**
 * BodyMapSVG
 * Single toggleable body map component (front/back view).
 * Clickable regions trigger the soreness logger.
 * Uses simplified SVG paths for each body region.
 */

import { useAppStore } from '../../stores/app.store';
import { REGIONS, SEVERITY_COLORS, type BodyRegionId, type SeverityLevel } from '../../config/bodymap.config';
import { cn } from '../../lib/utils';

interface BodyMapSVGProps {
  /** Severity values per region */
  sorenessMap: Partial<Record<BodyRegionId, SeverityLevel>>;
  /** Called when user taps a region */
  onRegionClick: (regionId: BodyRegionId) => void;
  className?: string;
}

export function BodyMapSVG({ sorenessMap, onRegionClick, className }: BodyMapSVGProps) {
  const view = useAppStore((s) => s.preferences.defaultBodyMapView);
  const setView = useAppStore((s) => s.setDefaultBodyMapView);

  const visibleRegions = REGIONS.filter((r) => r.view === view);

  return (
    <div className={cn('flex flex-col items-center gap-3', className)}>
      {/* Toggle */}
      <div className="flex items-center gap-1 p-1 rounded-xl bg-surface-100 dark:bg-surface-800">
        {(['front', 'back'] as const).map((v) => (
          <button
            key={v}
            type="button"
            onClick={() => setView(v)}
            className={cn(
              'px-4 py-1.5 text-xs font-medium rounded-lg transition-all capitalize',
              view === v
                ? 'bg-white dark:bg-surface-700 text-surface-800 dark:text-surface-200 shadow-sm'
                : 'text-surface-500 hover:text-surface-700 dark:hover:text-surface-300'
            )}
          >
            {v}
          </button>
        ))}
      </div>

      {/* SVG */}
      <svg
        viewBox="0 0 200 400"
        className="w-full max-w-[240px] h-auto"
        role="img"
        aria-label={`Body map — ${view} view`}
      >
        {/* Body outline */}
        <ellipse
          cx="100"
          cy="45"
          rx="28"
          ry="32"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          className="text-surface-200 dark:text-surface-700"
        />
        <path
          d="M72,75 L55,75 L35,170 L50,170 L60,130 L65,200 L65,320 L95,320 L95,200 L100,200 L105,200 L105,320 L135,320 L135,200 L140,130 L150,170 L165,170 L145,75 L128,75"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          className="text-surface-200 dark:text-surface-700"
        />

        {/* Clickable regions */}
        {visibleRegions.map((region) => {
          const severity = sorenessMap[region.id] ?? 0;
          const fillColor = severity > 0 ? SEVERITY_COLORS[severity] : 'transparent';

          return (
            <path
              key={region.id}
              d={region.path}
              fill={fillColor}
              fillOpacity={severity > 0 ? 0.5 : 0}
              stroke={severity > 0 ? fillColor : 'transparent'}
              strokeWidth={severity > 0 ? 1 : 0}
              className="cursor-pointer hover:fill-primary-200/40 dark:hover:fill-primary-800/40 transition-colors"
              onClick={() => onRegionClick(region.id)}
              role="button"
              aria-label={`${region.label} — severity ${severity}`}
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') onRegionClick(region.id);
              }}
            />
          );
        })}
      </svg>
    </div>
  );
}

/** Re-export config types/data for convenience */
export { REGIONS, SEVERITY_COLORS, type BodyRegionId, type SeverityLevel } from '../../config/bodymap.config';
