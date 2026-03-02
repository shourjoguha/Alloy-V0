/**
 * FilterBar
 * Reusable horizontal-scroll row of multi-select filter dropdown chips.
 * Each chip opens a dropdown with checkboxes and a "Select All" toggle.
 * Default state: all options selected (= no filter applied).
 */

import { useState, useRef, useEffect, useCallback } from 'react';
import { createPortal } from 'react-dom';
import { ChevronDown, Check } from 'lucide-react';
import { motion } from 'framer-motion';
import { cn } from '../../lib/utils';

export interface FilterOption {
  label: string;
  value: string;
}

export interface FilterDef {
  key: string;
  label: string;
  options: FilterOption[];
}

interface FilterBarProps {
  filters: FilterDef[];
  /**
   * Current active filter values: { filterKey: selectedValues[] }.
   * An empty array or undefined = all selected (no filter applied).
   */
  values: Record<string, string[]>;
  onChange: (key: string, values: string[]) => void;
  className?: string;
}

export function FilterBar({ filters, values, onChange, className }: FilterBarProps) {
  return (
    <div className={cn('flex gap-2 overflow-x-auto scrollbar-hide pb-1', className)}>
      {filters.map((filter) => (
        <MultiSelectChip
          key={filter.key}
          filter={filter}
          selected={values[filter.key] ?? []}
          onChange={(vals) => onChange(filter.key, vals)}
        />
      ))}
    </div>
  );
}

// ─── Multi-Select Chip ────────────────────────────────────────────────────────

interface MultiSelectChipProps {
  filter: FilterDef;
  /** Currently selected values. Empty array = all selected. */
  selected: string[];
  onChange: (values: string[]) => void;
}

function MultiSelectChip({ filter, selected, onChange }: MultiSelectChipProps) {
  const [open, setOpen] = useState(false);
  const [noneMode, setNoneMode] = useState(false);
  const chipRef = useRef<HTMLDivElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const [dropdownPos, setDropdownPos] = useState({ top: 0, left: 0 });

  // Calculate dropdown position from chip bounding rect
  const updatePosition = useCallback(() => {
    if (!chipRef.current) return;
    const rect = chipRef.current.getBoundingClientRect();
    setDropdownPos({
      top: rect.bottom + 4,
      left: rect.left,
    });
  }, []);

  // Position on open + scroll/resize
  useEffect(() => {
    if (!open) return;
    updatePosition();
    window.addEventListener('scroll', updatePosition, true);
    window.addEventListener('resize', updatePosition);
    return () => {
      window.removeEventListener('scroll', updatePosition, true);
      window.removeEventListener('resize', updatePosition);
    };
  }, [open, updatePosition]);

  // Close on click outside
  useEffect(() => {
    if (!open) return;
    function handleClick(e: MouseEvent) {
      const target = e.target as Node;
      if (
        chipRef.current && !chipRef.current.contains(target) &&
        dropdownRef.current && !dropdownRef.current.contains(target)
      ) {
        setOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [open]);

  const allValues = filter.options.map((o) => o.value);
  const isAllSelected = !noneMode && (selected.length === 0 || selected.length === allValues.length);
  const hasPartialSelection = !isAllSelected && !noneMode && selected.length > 0;
  const selectedCount = noneMode ? 0 : isAllSelected ? allValues.length : selected.length;

  function toggleOption(value: string) {
    if (noneMode) {
      // Coming from "none" mode — start fresh with just this option
      setNoneMode(false);
      onChange([value]);
      return;
    }

    const currentSet = isAllSelected ? new Set(allValues) : new Set(selected);

    if (currentSet.has(value)) {
      currentSet.delete(value);
      if (currentSet.size === 0) {
        // All items deselected via individual toggles → enter noneMode
        setNoneMode(true);
        onChange([]);
        return;
      }
    } else {
      currentSet.add(value);
    }

    if (currentSet.size === allValues.length) {
      onChange([]);
    } else {
      onChange(Array.from(currentSet));
    }
  }

  function toggleAll() {
    if (isAllSelected) {
      // Deselect all → enter noneMode so user can pick individually
      setNoneMode(true);
      onChange([]);
    } else {
      // Select all → back to default
      setNoneMode(false);
      onChange([]);
    }
  }

  const chipLabel = isAllSelected
    ? filter.label
    : `${filter.label} (${selectedCount})`;

  const dropdownContent = open ? (
    <motion.div
      ref={dropdownRef}
      initial={{ opacity: 0, y: -4 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -4 }}
      transition={{ duration: 0.12 }}
      style={{ position: 'fixed', top: dropdownPos.top, left: dropdownPos.left }}
      className={cn(
        'z-[100] min-w-[180px] max-h-[260px] overflow-y-auto',
        'bg-white dark:bg-surface-900 rounded-xl',
        'border border-surface-200 dark:border-surface-700 shadow-lg',
        'py-1'
      )}
    >
      {/* Select All toggle */}
      <button
        type="button"
        onClick={toggleAll}
        className={cn(
          'w-full flex items-center gap-2.5 px-3 py-2 text-xs text-left transition-colors',
          'border-b border-surface-100 dark:border-surface-800',
          'text-surface-700 dark:text-surface-300 hover:bg-surface-50 dark:hover:bg-surface-800',
          'font-medium'
        )}
      >
        <span
          className={cn(
            'flex items-center justify-center w-3.5 h-3.5 rounded border transition-colors',
            isAllSelected
              ? 'bg-amber-accent border-amber-accent'
              : 'border-surface-300 dark:border-surface-600'
          )}
        >
          {isAllSelected && <Check className="w-2.5 h-2.5 text-surface-950" />}
        </span>
        <span>Select All</span>
      </button>

      {/* Individual options */}
      {filter.options.map((opt) => {
        const isChecked = !noneMode && (isAllSelected || selected.includes(opt.value));
        return (
          <button
            key={opt.value}
            type="button"
            onClick={() => toggleOption(opt.value)}
            className={cn(
              'w-full flex items-center gap-2.5 px-3 py-2 text-xs text-left transition-colors',
              'text-surface-600 dark:text-surface-400 hover:bg-surface-50 dark:hover:bg-surface-800'
            )}
          >
            <span
              className={cn(
                'flex items-center justify-center w-3.5 h-3.5 rounded border transition-colors',
                isChecked
                  ? 'bg-amber-accent border-amber-accent'
                  : 'border-surface-300 dark:border-surface-600'
              )}
            >
              {isChecked && <Check className="w-2.5 h-2.5 text-surface-950" />}
            </span>
            <span>{opt.label}</span>
          </button>
        );
      })}
    </motion.div>
  ) : null;

  return (
    <div ref={chipRef} className="relative shrink-0">
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className={cn(
          'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors',
          'border whitespace-nowrap',
          hasPartialSelection
            ? 'bg-amber-accent-muted border-amber-accent/50 text-amber-accent-hover'
            : 'bg-white dark:bg-surface-900 border-surface-200 dark:border-surface-700 text-surface-600 dark:text-surface-400'
        )}
      >
        <span>{chipLabel}</span>
        <ChevronDown className={cn('w-3 h-3 transition-transform', open && 'rotate-180')} />
      </button>

      {/* Portal dropdown to document.body to avoid overflow clipping */}
      {dropdownContent && createPortal(dropdownContent, document.body)}
    </div>
  );
}
