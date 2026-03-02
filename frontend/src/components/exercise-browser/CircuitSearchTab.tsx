/**
 * CircuitSearchTab
 * Search Hyrox circuits with duration range, type filter, and text search.
 * Uses useHyroxSearch hook.
 */

import { useState, useMemo } from 'react';
import { Search, ChevronLeft, ChevronRight, ArrowLeft } from 'lucide-react';
import { motion } from 'framer-motion';
import { useHyroxSearch, useHyroxMovements, useHyroxWorkoutDetail } from '../../api/queries/movements';
import { FilterBar, type FilterDef } from './FilterBar';
import { CircuitCard } from './CircuitCard';
import { HyroxWorkoutDetail } from '../program/HyroxWorkoutDetail';
import { LoadingSpinner } from '../shared/LoadingSpinner';
import { HyroxWorkoutType, HYROX_WORKOUT_TYPE_LABELS } from '../../types/hyrox';
import { toTitleCase } from '../../lib/utils';

const WORKOUT_TYPE_OPTIONS = Object.entries(HYROX_WORKOUT_TYPE_LABELS).map(
  ([value, label]) => ({ value, label })
);

const DURATION_OPTIONS = [
  { value: '10', label: '≤ 10 min' },
  { value: '20', label: '≤ 20 min' },
  { value: '30', label: '≤ 30 min' },
  { value: '45', label: '≤ 45 min' },
  { value: '60', label: '≤ 60 min' },
];

export function CircuitSearchTab() {
  const [filterValues, setFilterValues] = useState<Record<string, string[]>>({});
  const [page, setPage] = useState(1);
  const [selectedWorkoutId, setSelectedWorkoutId] = useState<number | null>(null);
  const { data: workoutDetail, isLoading: isLoadingDetail } = useHyroxWorkoutDetail(selectedWorkoutId);
  const { data: movementsData } = useHyroxMovements();

  // Compute excluded movements: all movements minus selected ones
  const allMovementNames = movementsData?.movement_names ?? [];

  const params = useMemo(() => {
    const wt = filterValues['workout_type'];
    const dur = filterValues['max_duration'];
    const cplx = filterValues['complexity'];
    const incSelected = filterValues['includes'];

    // If user has partially selected movements, compute excluded = all - selected
    let excludes: string[] | undefined;
    if (incSelected && incSelected.length > 0 && incSelected.length < allMovementNames.length) {
      const selectedSet = new Set(incSelected);
      excludes = allMovementNames.filter((name) => !selectedSet.has(name));
    }

    return {
      workout_type: wt?.length === 1 ? wt[0] : undefined,
      max_duration: dur?.length === 1 ? Number(dur[0]) : undefined,
      is_complex: cplx?.length === 1 ? cplx[0] === 'true' : undefined,
      excludes: excludes?.length ? excludes : undefined,
      page,
      per_page: 20,
    };
  }, [filterValues, page, allMovementNames]);

  const { data, isLoading } = useHyroxSearch(params);

  const filterDefs: FilterDef[] = useMemo(() => {
    const defs: FilterDef[] = [
      {
        key: 'workout_type',
        label: 'Type',
        options: WORKOUT_TYPE_OPTIONS,
      },
      {
        key: 'max_duration',
        label: 'Duration',
        options: DURATION_OPTIONS,
      },
      {
        key: 'complexity',
        label: 'Complexity',
        options: [
          { value: 'true', label: 'Complex' },
          { value: 'false', label: 'Simple' },
        ],
      },
    ];

    // "Includes" filter — populated from distinct movement names in hyrox lines
    if (movementsData?.movement_names?.length) {
      defs.push({
        key: 'includes',
        label: 'Includes',
        options: movementsData.movement_names.map((name) => ({
          label: toTitleCase(name),
          value: name,
        })),
      });
    }

    return defs;
  }, [movementsData]);

  function handleFilterChange(key: string, values: string[]) {
    setFilterValues((prev) => ({ ...prev, [key]: values }));
    setPage(1);
  }

  // Workout detail view (in-pane)
  if (selectedWorkoutId !== null) {
    return (
      <div className="flex flex-col gap-3">
        <button
          type="button"
          onClick={() => setSelectedWorkoutId(null)}
          className="flex items-center gap-1.5 text-xs font-medium text-surface-500 hover:text-surface-700 dark:hover:text-surface-300 transition-colors self-start"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          Back to circuits
        </button>

        {isLoadingDetail ? (
          <div className="flex justify-center py-8">
            <LoadingSpinner />
          </div>
        ) : workoutDetail ? (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.15 }}
          >
            <HyroxWorkoutDetail detail={workoutDetail} />
          </motion.div>
        ) : (
          <p className="text-xs text-surface-400 text-center py-4">
            Workout not found
          </p>
        )}
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      {/* Filters */}
      <FilterBar
        filters={filterDefs}
        values={filterValues}
        onChange={handleFilterChange}
      />

      {/* Results */}
      {isLoading ? (
        <div className="flex justify-center py-8">
          <LoadingSpinner />
        </div>
      ) : (
        <>
          <div className="space-y-2 max-h-[400px] overflow-y-auto">
            {data?.workouts.map((workout) => (
              <CircuitCard
                key={workout.id}
                workout={workout}
                onClick={() => setSelectedWorkoutId(workout.id)}
              />
            ))}
            {data?.workouts.length === 0 && (
              <p className="text-xs text-surface-400 text-center py-4">
                No circuits found
              </p>
            )}
          </div>

          {/* Pagination */}
          {data && data.total_pages > 1 && (
            <div className="flex items-center justify-between pt-2">
              <button
                type="button"
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page <= 1}
                className="flex items-center gap-1 text-xs text-surface-500 disabled:text-surface-300 dark:disabled:text-surface-600"
              >
                <ChevronLeft className="w-3 h-3" />
                Prev
              </button>
              <span className="text-xs text-surface-400">
                {data.page} / {data.total_pages} ({data.total} results)
              </span>
              <button
                type="button"
                onClick={() => setPage((p) => Math.min(data.total_pages, p + 1))}
                disabled={page >= data.total_pages}
                className="flex items-center gap-1 text-xs text-surface-500 disabled:text-surface-300 dark:disabled:text-surface-600"
              >
                Next
                <ChevronRight className="w-3 h-3" />
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
