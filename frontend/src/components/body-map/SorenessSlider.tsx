/**
 * SorenessSlider
 * Horizontal severity slider (0–4) with coloured severity steps.
 */

import * as SliderPrimitive from '@radix-ui/react-slider';
import { SEVERITY_COLORS, SEVERITY_LABELS, type SeverityLevel } from '../../config/bodymap.config';

interface SorenessSliderProps {
  value: SeverityLevel;
  onChange: (value: SeverityLevel) => void;
}

export function SorenessSlider({ value, onChange }: SorenessSliderProps) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-xs text-surface-500 dark:text-surface-400">Soreness</span>
        <span
          className="text-xs font-medium px-2 py-0.5 rounded-full"
          style={{
            backgroundColor: `${SEVERITY_COLORS[value]}20`,
            color: SEVERITY_COLORS[value],
          }}
        >
          {SEVERITY_LABELS[value]}
        </span>
      </div>

      <SliderPrimitive.Root
        min={0}
        max={4}
        step={1}
        value={[value]}
        onValueChange={([v]) => onChange((v ?? value) as SeverityLevel)}
        className="relative flex items-center select-none touch-none w-full h-5"
      >
        <SliderPrimitive.Track className="relative h-1.5 w-full grow overflow-hidden rounded-full bg-surface-200 dark:bg-surface-700">
          <SliderPrimitive.Range
            className="absolute h-full rounded-full"
            style={{ backgroundColor: SEVERITY_COLORS[value] }}
          />
        </SliderPrimitive.Track>
        <SliderPrimitive.Thumb
          className="block h-5 w-5 rounded-full border-2 bg-white shadow-md transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
          style={{ borderColor: SEVERITY_COLORS[value], '--tw-ring-color': SEVERITY_COLORS[value] } as React.CSSProperties}
        />
      </SliderPrimitive.Root>

      {/* Step indicators */}
      <div className="flex justify-between px-0.5">
        {([0, 1, 2, 3, 4] as SeverityLevel[]).map((level) => (
          <div
            key={level}
            className="w-2 h-2 rounded-full"
            style={{
              backgroundColor: level <= value ? SEVERITY_COLORS[level] : '#e4e4e7',
            }}
          />
        ))}
      </div>
    </div>
  );
}
