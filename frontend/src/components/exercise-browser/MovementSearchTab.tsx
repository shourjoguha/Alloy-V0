/**
 * MovementSearchTab
 * Search input + filter chips + paginated movement list.
 * Uses useMovementSearch and useMovementFilters hooks.
 */

import { useState, useMemo } from 'react';
import { Search, ChevronLeft, ChevronRight } from 'lucide-react';
import { useMovementSearch, useMovementFilters } from '../../api/queries/movements';
import { FilterBar, type FilterDef } from './FilterBar';
import { MovementCard } from './MovementCard';
import { LoadingSpinner } from '../shared/LoadingSpinner';
import { toTitleCase } from '../../lib/utils';
import type { MovementSearchParams } from '../../types/movement';

export function MovementSearchTab() {
  const [searchText, setSearchText] = useState('');
  const [filterValues, setFilterValues] = useState<Record<string, string[]>>({});
  const [page, setPage] = useState(1);

  // Build search params from state
  // Empty array = all selected = don't send filter (backend returns everything)
  const params: MovementSearchParams = useMemo(() => {
    // Boolean filter helper: single-select → boolean | undefined
    const boolFilter = (key: string): boolean | undefined => {
      const vals = filterValues[key];
      if (!vals || vals.length !== 1) return undefined;
      return vals[0] === 'true';
    };

    return {
      q: searchText || undefined,
      primary_region: filterValues['primary_region']?.length ? filterValues['primary_region'] : undefined,
      primary_muscle: filterValues['primary_muscle']?.length ? filterValues['primary_muscle'] : undefined,
      discipline: filterValues['discipline']?.length ? filterValues['discipline'] : undefined,
      metric_type: filterValues['metric_type']?.length ? filterValues['metric_type'] : undefined,
      spinal_compression: filterValues['spinal_compression']?.length ? filterValues['spinal_compression'] : undefined,
      compound: boolFilter('compound'),
      is_complex_lift: boolFilter('is_complex_lift'),
      is_unilateral: boolFilter('is_unilateral'),
      equipment: filterValues['equipment']?.length ? filterValues['equipment'] : undefined,
      page,
      per_page: 20,
    };
  }, [searchText, filterValues, page]);

  const { data, isLoading } = useMovementSearch(params);
  const { data: filtersData } = useMovementFilters();

  // Build filter definitions from API response + static boolean/equipment filters
  const filterDefs: FilterDef[] = useMemo(() => {
    const defs: FilterDef[] = [];

    if (filtersData) {
      defs.push(
        {
          key: 'primary_region',
          label: 'Region',
          options: filtersData.primary_region.map((v) => ({ label: toTitleCase(v), value: v })),
        },
        {
          key: 'primary_muscle',
          label: 'Muscle',
          options: filtersData.primary_muscle.map((v) => ({ label: toTitleCase(v), value: v })),
        },
        {
          key: 'discipline',
          label: 'Discipline',
          options: filtersData.discipline.map((v) => ({ label: toTitleCase(v), value: v })),
        },
        {
          key: 'metric_type',
          label: 'Metric',
          options: filtersData.metric_type.map((v) => ({ label: toTitleCase(v), value: v })),
        },
        {
          key: 'spinal_compression',
          label: 'Spinal Load',
          options: filtersData.spinal_compression.map((v) => ({ label: toTitleCase(v), value: v })),
        },
      );
    }

    // Boolean filters
    defs.push(
      {
        key: 'compound',
        label: 'Compound',
        options: [
          { label: 'Compound', value: 'true' },
          { label: 'Isolation', value: 'false' },
        ],
      },
      {
        key: 'is_complex_lift',
        label: 'Complex Lift',
        options: [
          { label: 'Complex', value: 'true' },
          { label: 'Simple', value: 'false' },
        ],
      },
      {
        key: 'is_unilateral',
        label: 'Unilateral',
        options: [
          { label: 'Unilateral', value: 'true' },
          { label: 'Bilateral', value: 'false' },
        ],
      },
      {
        key: 'equipment',
        label: 'Equipment',
        options: [
          { label: 'Bodyweight', value: 'bodyweight' },
          { label: 'Dumbbell', value: 'dumbbell' },
          { label: 'Kettlebell', value: 'kettlebell' },
          { label: 'Barbell', value: 'barbell' },
          { label: 'Machine', value: 'machine' },
          { label: 'Band', value: 'band' },
          { label: 'Plate / Med Ball', value: 'plate_or_med_ball' },
        ],
      },
    );

    return defs;
  }, [filtersData]);

  function handleFilterChange(key: string, values: string[]) {
    setFilterValues((prev) => ({ ...prev, [key]: values }));
    setPage(1);
  }

  return (
    <div className="flex flex-col gap-3">
      {/* Search input */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-surface-400" />
        <input
          type="text"
          placeholder="Search movements..."
          value={searchText}
          onChange={(e) => { setSearchText(e.target.value); setPage(1); }}
          className="w-full pl-9 pr-3 py-2 text-sm rounded-lg border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 text-surface-800 dark:text-surface-200 placeholder:text-surface-400 focus:outline-none focus:ring-2 focus:ring-primary-500"
        />
      </div>

      {/* Filters */}
      {filterDefs.length > 0 && (
        <FilterBar
          filters={filterDefs}
          values={filterValues}
          onChange={handleFilterChange}
        />
      )}

      {/* Results */}
      {isLoading ? (
        <div className="flex justify-center py-8">
          <LoadingSpinner />
        </div>
      ) : (
        <>
          <div className="space-y-2 max-h-[400px] overflow-y-auto">
            {data?.movements.map((movement) => (
              <MovementCard key={movement.id} movement={movement} />
            ))}
            {data?.movements.length === 0 && (
              <p className="text-xs text-surface-400 text-center py-4">
                No movements found
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
