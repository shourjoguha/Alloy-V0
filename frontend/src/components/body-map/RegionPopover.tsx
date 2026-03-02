/**
 * RegionPopover
 * Small popover that appears when a body region is clicked.
 * Allows setting soreness severity.
 */

import * as Popover from '@radix-ui/react-popover';
import { X } from 'lucide-react';
import { SorenessSlider } from './SorenessSlider';
import { REGIONS, type BodyRegionId, type SeverityLevel } from '../../config/bodymap.config';

interface RegionPopoverProps {
  open: boolean;
  regionId: BodyRegionId | null;
  severity: SeverityLevel;
  onSeverityChange: (value: SeverityLevel) => void;
  onClose: () => void;
}

export function RegionPopover({
  open,
  regionId,
  severity,
  onSeverityChange,
  onClose,
}: RegionPopoverProps) {
  const region = regionId ? REGIONS.find((r) => r.id === regionId) : null;

  return (
    <Popover.Root open={open} onOpenChange={(o) => !o && onClose()}>
      <Popover.Anchor className="fixed top-1/2 left-1/2" />
      <Popover.Portal>
        <Popover.Content
          sideOffset={8}
          className="z-50 w-64 rounded-2xl bg-white dark:bg-surface-900 shadow-xl border border-surface-100 dark:border-surface-800 p-4 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95"
        >
          {/* Header */}
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-semibold text-surface-800 dark:text-surface-200">
              {region?.label ?? 'Region'}
            </h4>
            <Popover.Close asChild>
              <button
                type="button"
                className="flex items-center justify-center w-6 h-6 rounded-md text-surface-400 hover:text-surface-600 hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
                aria-label="Close"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </Popover.Close>
          </div>

          {/* Slider */}
          <SorenessSlider value={severity} onChange={onSeverityChange} />

          <Popover.Arrow className="fill-white dark:fill-surface-900" />
        </Popover.Content>
      </Popover.Portal>
    </Popover.Root>
  );
}
