/**
 * EquipmentSelector
 * Multi-select grid of equipment types.
 */

import { Check, Dumbbell } from 'lucide-react';
import { cn } from '../../lib/utils';
import { EquipmentType } from '../../types/enums';
import { toTitleCase } from '../../lib/utils';

interface EquipmentSelectorProps {
  value: EquipmentType[];
  onChange: (value: EquipmentType[]) => void;
}

const EQUIPMENT_OPTIONS = Object.values(EquipmentType);

export function EquipmentSelector({ value, onChange }: EquipmentSelectorProps) {
  const toggle = (item: EquipmentType) => {
    onChange(
      value.includes(item) ? value.filter((e) => e !== item) : [...value, item]
    );
  };

  return (
    <div className="space-y-4">
      <p className="text-sm text-surface-500 dark:text-surface-400">
        Select all equipment you have regular access to.
      </p>

      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {EQUIPMENT_OPTIONS.map((equipment) => {
          const isSelected = value.includes(equipment);

          return (
            <button
              key={equipment}
              type="button"
              onClick={() => toggle(equipment)}
              className={cn(
                'relative flex flex-col items-center gap-2 p-4 rounded-xl border-2 text-sm font-medium transition-all',
                isSelected
                  ? 'bg-primary-50 border-primary-500 text-primary-700 dark:bg-primary-900/30 dark:border-primary-500 dark:text-primary-300'
                  : 'bg-white dark:bg-surface-900 border-surface-200 dark:border-surface-700 text-surface-600 dark:text-surface-400 hover:border-surface-300 dark:hover:border-surface-600'
              )}
            >
              {isSelected && (
                <span className="absolute top-2 right-2 flex items-center justify-center w-4 h-4 rounded-full bg-primary-600">
                  <Check className="w-2.5 h-2.5 text-white" />
                </span>
              )}
              <Dumbbell className="w-6 h-6" />
              <span className="text-xs text-center leading-tight">
                {toTitleCase(equipment)}
              </span>
            </button>
          );
        })}
      </div>

      {value.length === 0 && (
        <p className="text-xs text-amber-600 dark:text-amber-400">
          Select at least bodyweight to continue.
        </p>
      )}
    </div>
  );
}
