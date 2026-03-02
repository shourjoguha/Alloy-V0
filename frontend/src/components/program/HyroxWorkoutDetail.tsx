/**
 * HyroxWorkoutDetail
 * Renders a full Hyrox workout: name, type badge, time specification,
 * movement lines grouped by mini circuits, with reps/duration/weight.
 *
 * Used as a detail/modal view when a user clicks into a Hyrox session.
 */

import { X, Clock, Dumbbell, Flame, Pause, Repeat } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Card, CardContent, CardHeader } from '../ui/card';
import type {
  HyroxWorkoutDetail as HyroxWorkoutDetailType,
  HyroxMiniCircuit,
} from '../../types/hyrox';
import {
  HYROX_WORKOUT_TYPE_LABELS,
  HYROX_WORKOUT_TYPE_COLORS,
} from '../../types/hyrox';

interface HyroxWorkoutDetailProps {
  detail: HyroxWorkoutDetailType;
  onClose?: () => void;
}

export function HyroxWorkoutDetail({ detail, onClose }: HyroxWorkoutDetailProps) {
  const { workout, lines, mini_circuits } = detail;

  const typeLabel =
    HYROX_WORKOUT_TYPE_LABELS[workout.workout_type] ?? workout.workout_type;
  const typeColor =
    HYROX_WORKOUT_TYPE_COLORS[workout.workout_type] ??
    'bg-surface-100 text-surface-600 dark:bg-surface-800 dark:text-surface-400';

  // Separate movement lines from rest lines for display
  const movementLines = lines.filter((l) => !l.is_rest);

  return (
    <Card className="overflow-hidden animate-slide-up">
      {/* Header */}
      <CardHeader className="pb-4 border-b border-border-default">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1.5">
              <span
                className={cn(
                  'text-xs font-medium px-2.5 py-1 rounded-full shrink-0',
                  typeColor
                )}
              >
                {typeLabel}
              </span>
              {workout.badge && (
                <span className="text-xs px-2 py-0.5 rounded-full bg-amber-50 text-amber-600 dark:bg-amber-900/20 dark:text-amber-400 truncate">
                  {workout.badge}
                </span>
              )}
            </div>
            <h3 className="text-lg font-semibold text-surface-800 dark:text-surface-200">
              {workout.name}
            </h3>
          </div>
          {onClose && (
            <button
              type="button"
              onClick={onClose}
              className="p-1.5 rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors shrink-0"
            >
              <X className="w-4 h-4 text-text-muted" />
            </button>
          )}
        </div>

        {/* Meta row */}
        <div className="flex flex-wrap items-center gap-3 mt-3">
          {workout.total_time_minutes && (
            <div className="flex items-center gap-1.5 text-sm text-text-muted">
              <Clock className="w-3.5 h-3.5" />
              {workout.total_time_minutes} min
            </div>
          )}
          {workout.total_rounds && (
            <div className="flex items-center gap-1.5 text-sm text-text-muted">
              <Repeat className="w-3.5 h-3.5" />
              {workout.total_rounds} rounds
            </div>
          )}
          {workout.time_specification && (
            <div className="text-sm text-text-subtle">
              {workout.time_specification}
            </div>
          )}
          {workout.has_buy_in && (
            <span className="text-xs px-2 py-0.5 rounded-md bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400">
              Buy-In
            </span>
          )}
          {workout.has_cash_out && (
            <span className="text-xs px-2 py-0.5 rounded-md bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400">
              Cash-Out
            </span>
          )}
        </div>
      </CardHeader>

      {/* Workout body — grouped by mini circuits when present */}
      <CardContent>
        {mini_circuits.length > 0 ? (
          <CircuitGroupedLines lines={lines} miniCircuits={mini_circuits} />
        ) : (
          <>
            <h4 className="text-xs font-medium text-text-muted uppercase tracking-wide mb-3">
              Movements
            </h4>
            <div className="space-y-1.5">
              {lines.map((line) => (
                <HyroxLineRow key={line.id} line={line} />
              ))}
            </div>
          </>
        )}
      </CardContent>

      {/* Summary stats */}
      <div className="px-5 pb-5">
        <div className="flex flex-wrap items-center gap-4 text-xs text-text-muted">
          <span>{movementLines.length} movements</span>
          <span>{lines.filter((l) => l.is_rest).length} rest periods</span>
          {mini_circuits.length > 0 && <span>{mini_circuits.length} circuits</span>}
          {workout.is_complex && <span>Complex workout</span>}
        </div>
      </div>
    </Card>
  );
}

// ---------------------------------------------------------------------------
// CircuitGroupedLines — renders lines grouped under circuit headers
// ---------------------------------------------------------------------------

interface CircuitGroupedLinesProps {
  lines: HyroxWorkoutDetailType['lines'];
  miniCircuits: HyroxMiniCircuit[];
}

function CircuitGroupedLines({ lines, miniCircuits }: CircuitGroupedLinesProps) {
  // Separate lines into: buy-in (standalone), per-circuit, cash-out (standalone), ungrouped
  const buyInLines = lines.filter((l) => l.is_buy_in && !l.mini_circuit_id);
  const cashOutLines = lines.filter((l) => l.is_cash_out && !l.mini_circuit_id);
  const ungroupedLines = lines.filter(
    (l) => !l.mini_circuit_id && !l.is_buy_in && !l.is_cash_out
  );

  // Group lines by circuit
  const circuitLines = new Map<number, HyroxWorkoutDetailType['lines']>();
  for (const line of lines) {
    if (line.mini_circuit_id != null) {
      const existing = circuitLines.get(line.mini_circuit_id) ?? [];
      existing.push(line);
      circuitLines.set(line.mini_circuit_id, existing);
    }
  }

  return (
    <div className="space-y-4">
      {/* Buy-in lines (standalone, before circuits) */}
      {buyInLines.length > 0 && (
        <div>
          <h4 className="text-xs font-medium text-blue-500 uppercase tracking-wide mb-2">
            Buy-In
          </h4>
          <div className="space-y-1.5">
            {buyInLines.map((line) => (
              <HyroxLineRow key={line.id} line={line} />
            ))}
          </div>
        </div>
      )}

      {/* Circuit sections */}
      {miniCircuits.map((circuit) => {
        const linesForCircuit = circuitLines.get(circuit.id) ?? [];
        const circuitTypeLabel =
          HYROX_WORKOUT_TYPE_LABELS[circuit.circuit_type] ?? circuit.circuit_type;

        return (
          <div key={circuit.id}>
            <div className="flex items-center gap-2 mb-2">
              <span
                className={cn(
                  'text-xs font-medium px-2 py-0.5 rounded-full',
                  HYROX_WORKOUT_TYPE_COLORS[circuit.circuit_type] ??
                    'bg-surface-100 text-surface-600 dark:bg-surface-800 dark:text-surface-400'
                )}
              >
                {circuitTypeLabel}
              </span>
              {circuit.rounds && (
                <span className="text-xs text-text-muted">
                  {circuit.rounds} rounds
                </span>
              )}
              {circuit.duration_minutes && (
                <span className="text-xs text-text-muted">
                  {circuit.duration_minutes} min
                </span>
              )}
            </div>
            {circuit.notes && (
              <p className="text-xs text-text-subtle mb-2 italic">
                {circuit.notes}
              </p>
            )}
            <div className="space-y-1.5">
              {linesForCircuit.map((line) => (
                <HyroxLineRow key={line.id} line={line} />
              ))}
            </div>
            {circuit.rest_after_minutes != null && circuit.rest_after_minutes > 0 && (
              <Card variant="grouped" className="flex items-center gap-2 py-1.5 px-3 mt-1.5">
                <Pause className="w-3 h-3 text-text-subtle" />
                <span className="text-xs text-text-muted">
                  {circuit.rest_after_minutes} min rest between circuits
                </span>
              </Card>
            )}
          </div>
        );
      })}

      {/* Cash-out lines (standalone, after circuits) */}
      {cashOutLines.length > 0 && (
        <div>
          <h4 className="text-xs font-medium text-purple-500 uppercase tracking-wide mb-2">
            Cash-Out
          </h4>
          <div className="space-y-1.5">
            {cashOutLines.map((line) => (
              <HyroxLineRow key={line.id} line={line} />
            ))}
          </div>
        </div>
      )}

      {/* Ungrouped lines (not in any circuit, not buy-in/cash-out) */}
      {ungroupedLines.length > 0 && (
        <div>
          <h4 className="text-xs font-medium text-text-muted uppercase tracking-wide mb-2">
            Additional Movements
          </h4>
          <div className="space-y-1.5">
            {ungroupedLines.map((line) => (
              <HyroxLineRow key={line.id} line={line} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

interface HyroxLineRowProps {
  line: HyroxWorkoutDetailType['lines'][number];
}

function HyroxLineRow({ line }: HyroxLineRowProps) {
  if (line.is_rest) {
    return (
      <Card variant="grouped" className="flex items-center gap-2 py-1.5 px-3">
        <Pause className="w-3 h-3 text-text-subtle" />
        <span className="text-xs text-text-muted">
          {line.duration_seconds ? `${line.duration_seconds}s rest` : 'Rest'}
        </span>
      </Card>
    );
  }

  return (
    <Card
      variant="grouped"
      className={cn(
        'flex items-center gap-3 py-2 px-3',
        line.is_buy_in && 'border-l-2 border-blue-400',
        line.is_cash_out && 'border-l-2 border-purple-400'
      )}
    >
      {/* Movement indicator */}
      <div className="shrink-0">
        {line.is_max_effort ? (
          <Flame className="w-3.5 h-3.5 text-orange-500" />
        ) : (
          <Dumbbell className="w-3.5 h-3.5 text-text-muted" />
        )}
      </div>

      {/* Movement name + text */}
      <div className="flex-1 min-w-0">
        <p className="text-sm text-surface-700 dark:text-surface-300 truncate">
          {line.movement_name ?? line.line_text}
        </p>
        {line.movement_name && line.line_text !== line.movement_name && (
          <p className="text-xs text-text-muted truncate">{line.line_text}</p>
        )}
      </div>

      {/* Metrics */}
      <div className="flex items-center gap-2 shrink-0">
        {line.reps != null && (
          <span className="text-xs font-medium text-surface-600 dark:text-surface-400">
            {line.reps} reps
          </span>
        )}
        {line.duration_seconds != null && !line.is_rest && (
          <span className="text-xs font-medium text-surface-600 dark:text-surface-400">
            {line.duration_seconds}s
          </span>
        )}
        {line.distance_meters != null && (
          <span className="text-xs font-medium text-surface-600 dark:text-surface-400">
            {line.distance_meters}m
          </span>
        )}
        {line.calories != null && (
          <span className="text-xs font-medium text-surface-600 dark:text-surface-400">
            {line.calories} cal
          </span>
        )}
        {(line.weight_male != null || line.weight_female != null) && (
          <span className="text-xs text-text-muted">
            {line.weight_male != null && `${line.weight_male}lb`}
            {line.weight_male != null && line.weight_female != null && '/'}
            {line.weight_female != null && `${line.weight_female}lb`}
          </span>
        )}
      </div>
    </Card>
  );
}
