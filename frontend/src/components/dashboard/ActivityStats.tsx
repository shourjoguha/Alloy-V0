/**
 * ActivityStats
 * 3-column grid: Workouts Done, Week Streak, Adherence %.
 * Same card style as DashboardStats with amber values.
 */

import { cn } from '../../lib/utils';
import { Card } from '../ui/card';

interface ActivityStatsProps {
  workoutsDone?: number;
  weekStreak?: number;
  adherence?: string;
  className?: string;
}

export function ActivityStats({
  workoutsDone = 2,
  weekStreak = 1,
  adherence = '67%',
  className,
}: ActivityStatsProps) {
  const stats = [
    { value: String(workoutsDone), label: 'Workouts Done' },
    { value: String(weekStreak), label: 'Week Streak' },
    { value: adherence, label: 'Adherence' },
  ];

  return (
    <div className={cn('grid grid-cols-3 gap-3', className)}>
      {stats.map((stat) => (
        <Card key={stat.label} variant="grouped" className="p-4 text-center">
          <div className="text-2xl font-bold text-amber-accent">
            {stat.value}
          </div>
          <div className="text-xs text-surface-400 dark:text-surface-500 mt-1">
            {stat.label}
          </div>
        </Card>
      ))}
    </div>
  );
}
