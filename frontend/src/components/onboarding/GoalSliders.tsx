/**
 * GoalSliders
 * Three-slider hierarchy: primary (Strength ↔ Endurance) + two secondary.
 * Secondary sliders show a live "influenced" preview based on the primary.
 */

import * as SliderPrimitive from '@radix-ui/react-slider';
import { motion } from 'framer-motion';
import type { HierarchicalGoalSliders } from '../../types/onboarding';

interface GoalSlidersProps {
  value: HierarchicalGoalSliders;
  onChange: (value: HierarchicalGoalSliders) => void;
}

interface SliderRowProps {
  label: string;
  leftLabel: string;
  rightLabel: string;
  value: number;
  influenced?: boolean;
  influencedValue?: number;
  onChange: (val: number) => void;
}

function SliderRow({
  label,
  leftLabel,
  rightLabel,
  value,
  influenced,
  influencedValue,
  onChange,
}: SliderRowProps) {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-surface-700 dark:text-surface-300">
          {label}
        </span>
        {influenced && influencedValue !== undefined && (
          <span className="text-xs text-primary-500 dark:text-primary-400">
            Adjusted: {Math.round(influencedValue * 100)}%
          </span>
        )}
      </div>

      <div className="relative py-1">
        <SliderPrimitive.Root
          min={0}
          max={1}
          step={0.01}
          value={[value]}
          onValueChange={([v]) => onChange(v ?? value)}
          className="relative flex items-center select-none touch-none w-full h-5"
        >
          <SliderPrimitive.Track className="relative h-1.5 w-full grow overflow-hidden rounded-full bg-surface-200 dark:bg-surface-700">
            <SliderPrimitive.Range className="absolute h-full bg-primary-500" />
          </SliderPrimitive.Track>
          <SliderPrimitive.Thumb className="block h-5 w-5 rounded-full border-2 border-primary-600 bg-white shadow-md ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 cursor-grab active:cursor-grabbing" />
        </SliderPrimitive.Root>

        {/* Influence indicator line */}
        {influenced && influencedValue !== undefined && influencedValue !== value && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="absolute top-1/2 -translate-y-1/2 w-1 h-3 rounded-full bg-primary-300"
            style={{ left: `calc(${influencedValue * 100}% - 2px)` }}
          />
        )}
      </div>

      <div className="flex justify-between text-xs text-surface-400">
        <span>{leftLabel}</span>
        <span>{rightLabel}</span>
      </div>
    </div>
  );
}

/** Sigmoid-based normalization, mirroring the backend logic */
function normalizeSecondary(
  baseValue: number,
  primaryValue: number,
  strengthInfluence: number,
  enduranceInfluence: number
): number {
  const k = 6.0;
  const strengthBias = 1 / (1 + Math.exp(-k * (primaryValue - 0.5)));
  const enduranceBias = 1 - strengthBias;
  const adjustment =
    strengthBias * strengthInfluence + enduranceBias * enduranceInfluence;
  return Math.min(0.95, Math.max(0.05, baseValue + adjustment));
}

export function GoalSliders({ value, onChange }: GoalSlidersProps) {
  const primaryVal = value.primary_slider.value;

  const normalizedHFL = normalizeSecondary(
    value.hypertrophy_fat_loss.value,
    primaryVal,
    0.3,
    -0.2
  );
  const normalizedPM = normalizeSecondary(
    value.power_mobility.value,
    primaryVal,
    0.4,
    -0.3
  );

  return (
    <div className="space-y-8">
      {/* Primary slider */}
      <div className="p-5 rounded-xl bg-primary-50 dark:bg-primary-900/20 border border-primary-100 dark:border-primary-900/40">
        <SliderRow
          label="Primary Goal"
          leftLabel="Endurance"
          rightLabel="Strength"
          value={primaryVal}
          onChange={(v) =>
            onChange({
              ...value,
              primary_slider: { ...value.primary_slider, value: v },
            })
          }
        />
      </div>

      {/* Secondary sliders */}
      <div className="space-y-6">
        <p className="text-xs text-surface-400 dark:text-surface-500 uppercase tracking-wide font-medium">
          Secondary Goals — influenced by Primary
        </p>

        <SliderRow
          label="Body Composition"
          leftLabel="Fat Loss"
          rightLabel="Hypertrophy"
          value={value.hypertrophy_fat_loss.value}
          influenced
          influencedValue={normalizedHFL}
          onChange={(v) =>
            onChange({
              ...value,
              hypertrophy_fat_loss: {
                ...value.hypertrophy_fat_loss,
                value: v,
              },
            })
          }
        />

        <SliderRow
          label="Performance"
          leftLabel="Mobility"
          rightLabel="Power"
          value={value.power_mobility.value}
          influenced
          influencedValue={normalizedPM}
          onChange={(v) =>
            onChange({
              ...value,
              power_mobility: { ...value.power_mobility, value: v },
            })
          }
        />
      </div>
    </div>
  );
}
