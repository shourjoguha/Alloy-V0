/**
 * DashboardStats
 * 3-column grid: Heaviest Lift, Longest Workout, Total Volume This Month.
 * Values in amber/gold; stacks to 2-col on narrow mobile.
 */

import { cn } from '../../lib/utils';
import { Card } from '../ui/card';

interface StatItem {
  value: string;
  label: string;
  sublabel?: string;
}

interface DashboardStatsProps {
  stats?: StatItem[];
  className?: string;
}

const DEFAULT_STATS: StatItem[] = [
  { value: '7.5kg', label: 'Heaviest Lift', sublabel: 'Ab Wheel Rollout' },
  { value: '9m', label: 'Longest Workout', sublabel: '1/3/2026' },
  { value: '38kg', label: 'Total Volume This Month' },
];

export function DashboardStats({ stats = DEFAULT_STATS, className }: DashboardStatsProps) {
  return (
    <div className={cn('grid grid-cols-2 md:grid-cols-3 gap-3', className)}>
      {stats.map((stat) => (
        <Card key={stat.label} variant="grouped" className="p-4 text-center">
          <div className="text-2xl font-bold text-amber-accent">
            {stat.value}
          </div>
          <div className="text-xs text-surface-400 dark:text-surface-500 mt-1">
            {stat.label}
          </div>
          {stat.sublabel && (
            <div className="text-xs text-surface-300 dark:text-surface-600 mt-0.5 truncate">
              {stat.sublabel}
            </div>
          )}
        </Card>
      ))}
    </div>
  );
}
