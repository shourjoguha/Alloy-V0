/**
 * StatCard
 * Compact KPI display: large bold value + muted label + optional sublabel.
 * Uses Card's `grouped` variant for a clean, borderless appearance.
 */

import { cn } from '../../lib/utils';
import { Card } from '../ui/card';

interface StatCardProps {
  /** Formatted display value (e.g. "245kg", "87%", "12") */
  value: string;
  /** Short label below the value */
  label: string;
  /** Optional tertiary line (e.g. movement name, date) */
  sublabel?: string;
  className?: string;
}

export function StatCard({ value, label, sublabel, className }: StatCardProps) {
  return (
    <Card variant="grouped" className={cn('p-4 text-center', className)}>
      <div className="text-2xl font-bold text-primary-600 dark:text-primary-400">
        {value}
      </div>
      <div className="text-xs text-surface-400 dark:text-surface-500 mt-1">
        {label}
      </div>
      {sublabel && (
        <div className="text-xs text-surface-300 dark:text-surface-600 mt-0.5 truncate">
          {sublabel}
        </div>
      )}
    </Card>
  );
}
