/**
 * WeekView
 * Shows all sessions in a given week as a horizontal scroll strip.
 */

import { Moon } from 'lucide-react';
import { dayNumberToName } from '../../lib/utils';
import { SessionCard } from './SessionCard';
import type { WeeklyPlan } from '../../types/program';

interface WeekViewProps {
  plan: WeeklyPlan;
  onSessionClick?: (sessionId: string) => void;
}

export function WeekView({ plan, onSessionClick }: WeekViewProps) {
  const allDays = Array.from({ length: 7 }, (_, i) => i + 1);

  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <div>
          <h3 className="text-sm font-semibold text-surface-800 dark:text-surface-200">
            Week {plan.week_number}
          </h3>
          <p className="text-xs text-surface-400 mt-0.5 capitalize">{plan.weekly_focus}</p>
        </div>
        <span className="text-xs text-surface-400">
          {plan.total_sessions} sessions
        </span>
      </div>

      <div className="grid grid-cols-7 gap-1.5">
        {allDays.map((dayNum) => {
          const session = plan.sessions.find((s) => s.day_number === dayNum);
          const isRest = plan.rest_days.includes(dayNum);

          return (
            <div key={dayNum} className="min-w-0">
              {/* Day label */}
              <p className="text-[10px] text-surface-400 text-center mb-1">
                {dayNumberToName(dayNum).slice(0, 3)}
              </p>

              {session ? (
                <SessionCard
                  session={session}
                  compact
                  onClick={onSessionClick ? () => onSessionClick(session.session_id) : undefined}
                />
              ) : (
                <div className="p-3 rounded-xl border border-dashed border-surface-200 dark:border-surface-700 flex items-center justify-center min-h-[60px]">
                  {isRest && <Moon className="w-3.5 h-3.5 text-surface-300 dark:text-surface-600" />}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
