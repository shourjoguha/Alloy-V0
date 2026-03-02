/**
 * BudgetAllocator
 * Reusable "distribute N points across M items" UI pattern.
 * Inspired by Gainsly's goal/discipline dollar-budget metaphor.
 *
 * Not wired to any specific page — use as a building block for
 * goal weighting, discipline priorities, etc.
 *
 * @example
 *   <BudgetAllocator
 *     items={GOALS}
 *     totalBudget={10}
 *     maxSelections={3}
 *     value={allocations}
 *     onChange={setAllocations}
 *   />
 */

import { cn } from '../../lib/utils';
import { Card } from '../ui/card';

// ─── Types ──────────────────────────────────────────────────────────────────

export interface BudgetItem {
  id: string;
  name: string;
  description: string;
  icon?: string;
}

export interface BudgetAllocation {
  id: string;
  weight: number;
}

interface BudgetAllocatorProps {
  /** Available items to allocate budget across */
  items: BudgetItem[];
  /** Total budget to distribute (e.g. 10) */
  totalBudget: number;
  /** Max number of items that can have weight > 0 */
  maxSelections?: number;
  /** Current allocations */
  value: BudgetAllocation[];
  /** Called when allocations change */
  onChange: (allocations: BudgetAllocation[]) => void;
  /** Unit label shown next to values (default: "$") */
  unitLabel?: string;
  className?: string;
}

// ─── Component ──────────────────────────────────────────────────────────────

export function BudgetAllocator({
  items,
  totalBudget,
  maxSelections,
  value,
  onChange,
  unitLabel = '$',
  className,
}: BudgetAllocatorProps) {
  const totalAllocated = value.reduce((sum, a) => sum + a.weight, 0);
  const remaining = totalBudget - totalAllocated;
  const activeCount = value.filter((a) => a.weight > 0).length;
  const isComplete = remaining === 0;

  function getWeight(id: string): number {
    return value.find((a) => a.id === id)?.weight ?? 0;
  }

  function handleChange(id: string, delta: number): void {
    const currentWeight = getWeight(id);
    const newWeight = Math.max(0, Math.min(totalBudget, currentWeight + delta));

    // Block increment if budget exhausted
    if (delta > 0 && totalAllocated >= totalBudget) return;

    // Block adding new item if max selections reached
    if (
      delta > 0 &&
      currentWeight === 0 &&
      maxSelections !== undefined &&
      activeCount >= maxSelections
    ) {
      return;
    }

    const updated = value.filter((a) => a.id !== id);
    if (newWeight > 0) {
      updated.push({ id, weight: newWeight });
    }
    onChange(updated);
  }

  return (
    <div className={cn('space-y-4', className)}>
      {/* Budget progress */}
      <Card variant="grouped" className="p-4">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-surface-700 dark:text-surface-300">
            Budget Remaining
          </span>
          <span
            className={cn(
              'text-lg font-bold tabular-nums',
              isComplete
                ? 'text-success'
                : remaining < 0
                  ? 'text-error'
                  : 'text-primary-600 dark:text-primary-400'
            )}
          >
            {unitLabel}{remaining}
          </span>
        </div>
        <div className="h-2 bg-surface-200 dark:bg-surface-800 rounded-full overflow-hidden">
          <div
            className={cn(
              'h-full transition-all duration-300 rounded-full',
              isComplete ? 'bg-success' : 'bg-primary-500'
            )}
            style={{
              width: `${Math.min(100, (totalAllocated / totalBudget) * 100)}%`,
            }}
          />
        </div>
        {maxSelections !== undefined && activeCount > maxSelections && (
          <p className="text-xs text-error mt-2">
            Maximum {maxSelections} selections allowed
          </p>
        )}
      </Card>

      {/* Item cards */}
      <div className="grid gap-3">
        {items.map((item) => {
          const weight = getWeight(item.id);
          const isActive = weight > 0;
          const canIncrement =
            totalAllocated < totalBudget &&
            (isActive || maxSelections === undefined || activeCount < maxSelections);

          return (
            <Card
              key={item.id}
              variant={isActive ? 'selected' : 'grouped'}
              className="p-4"
            >
              <div className="flex items-center gap-4">
                {item.icon && (
                  <div className="text-2xl shrink-0">{item.icon}</div>
                )}
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-sm text-surface-900 dark:text-surface-100">
                    {item.name}
                  </h3>
                  <p className="text-xs text-surface-400 dark:text-surface-500">
                    {item.description}
                  </p>
                </div>

                {/* Stepper controls */}
                <div className="flex items-center gap-2 shrink-0">
                  <button
                    type="button"
                    onClick={() => handleChange(item.id, -1)}
                    disabled={weight === 0}
                    className={cn(
                      'h-8 w-8 rounded-lg flex items-center justify-center text-lg font-bold transition-colors',
                      weight === 0
                        ? 'bg-surface-100 dark:bg-surface-800 text-surface-300 dark:text-surface-600 cursor-not-allowed'
                        : 'bg-surface-100 dark:bg-surface-800 hover:bg-primary-500 hover:text-white text-surface-600 dark:text-surface-300'
                    )}
                    aria-label={`Decrease ${item.name}`}
                  >
                    −
                  </button>
                  <div
                    className={cn(
                      'w-10 h-10 rounded-lg flex items-center justify-center text-lg font-bold tabular-nums',
                      isActive
                        ? 'bg-primary-600 text-white'
                        : 'bg-surface-100 dark:bg-surface-800 text-surface-600 dark:text-surface-400'
                    )}
                  >
                    {unitLabel}{weight}
                  </div>
                  <button
                    type="button"
                    onClick={() => handleChange(item.id, 1)}
                    disabled={!canIncrement}
                    className={cn(
                      'h-8 w-8 rounded-lg flex items-center justify-center text-lg font-bold transition-colors',
                      !canIncrement
                        ? 'bg-surface-100 dark:bg-surface-800 text-surface-300 dark:text-surface-600 cursor-not-allowed'
                        : 'bg-surface-100 dark:bg-surface-800 hover:bg-primary-500 hover:text-white text-surface-600 dark:text-surface-300'
                    )}
                    aria-label={`Increase ${item.name}`}
                  >
                    +
                  </button>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Validation hint */}
      {!isComplete && totalAllocated > 0 && (
        <p className="text-center text-sm text-surface-400">
          Distribute all {unitLabel}{totalBudget} to continue (currently{' '}
          {unitLabel}{totalAllocated})
        </p>
      )}
    </div>
  );
}
