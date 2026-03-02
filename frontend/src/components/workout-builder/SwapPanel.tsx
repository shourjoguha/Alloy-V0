/**
 * SwapPanel
 * Inline expansion below an exercise — allows searching for and selecting a replacement.
 * Animated open/close with Framer Motion.
 */

import { useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { Search, ArrowRightLeft } from 'lucide-react';
import { useBuilder, type BuilderExercise } from './BuilderContext';
import { cn } from '../../lib/utils';

interface SwapPanelProps {
  exerciseId: string;
}

// Mock exercise catalogue — will be replaced with API search
const EXERCISE_CATALOGUE: BuilderExercise[] = [
  { id: 'swap-1',  name: 'Front Squat',          sets: 4, reps: '6-8',  restSeconds: 180, equipment: 'barbell' },
  { id: 'swap-2',  name: 'Leg Press',            sets: 3, reps: '10-12', restSeconds: 120, equipment: 'machine' },
  { id: 'swap-3',  name: 'Bulgarian Split Squat', sets: 3, reps: '8-10', restSeconds: 90,  equipment: 'dumbbell' },
  { id: 'swap-4',  name: 'Romanian Deadlift',     sets: 4, reps: '6-8',  restSeconds: 150, equipment: 'barbell' },
  { id: 'swap-5',  name: 'Hip Thrust',           sets: 3, reps: '10-12', restSeconds: 90,  equipment: 'barbell' },
  { id: 'swap-6',  name: 'Goblet Squat',         sets: 3, reps: '12-15', restSeconds: 60,  equipment: 'kettlebell' },
  { id: 'swap-7',  name: 'Leg Curl',             sets: 3, reps: '10-12', restSeconds: 60,  equipment: 'machine' },
  { id: 'swap-8',  name: 'Step-up',              sets: 3, reps: '10',    restSeconds: 60,  equipment: 'dumbbell' },
];

export function SwapPanel({ exerciseId }: SwapPanelProps) {
  const { swapExercise, exercises } = useBuilder();
  const [search, setSearch] = useState('');

  const currentIds = useMemo(() => new Set(exercises.map((e) => e.id)), [exercises]);

  const filtered = useMemo(() => {
    const q = search.toLowerCase().trim();
    return EXERCISE_CATALOGUE.filter(
      (e) => !currentIds.has(e.id) && (!q || e.name.toLowerCase().includes(q))
    );
  }, [search, currentIds]);

  return (
    <motion.div
      initial={{ height: 0, opacity: 0 }}
      animate={{ height: 'auto', opacity: 1 }}
      exit={{ height: 0, opacity: 0 }}
      transition={{ duration: 0.2, ease: 'easeInOut' }}
      className="overflow-hidden"
    >
      <div className="ml-7 mt-1 mb-2 p-3 rounded-xl bg-surface-50 dark:bg-surface-800/50 border border-surface-100 dark:border-surface-800 space-y-3">
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-surface-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search exercises…"
            className="w-full pl-8 pr-3 py-1.5 text-xs rounded-lg border border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-900 text-surface-800 dark:text-surface-200 placeholder:text-surface-400 focus:outline-none focus:ring-1 focus:ring-primary-500"
          />
        </div>

        {/* Results */}
        <div className="max-h-[200px] overflow-y-auto space-y-1">
          {filtered.length === 0 ? (
            <p className="text-xs text-surface-400 py-2 text-center">No exercises found</p>
          ) : (
            filtered.map((exercise) => (
              <button
                key={exercise.id}
                type="button"
                onClick={() =>
                  swapExercise(exerciseId, {
                    ...exercise,
                    id: `${exercise.id}-${Date.now()}`, // Unique ID for the new instance
                  })
                }
                className={cn(
                  'w-full flex items-center justify-between gap-2 px-3 py-2 rounded-lg text-left',
                  'hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors'
                )}
              >
                <div className="min-w-0">
                  <p className="text-xs font-medium text-surface-700 dark:text-surface-300 truncate">
                    {exercise.name}
                  </p>
                  <p className="text-[10px] text-surface-400 capitalize">
                    {exercise.equipment} · {exercise.sets}×{exercise.reps}
                  </p>
                </div>
                <ArrowRightLeft className="w-3 h-3 text-surface-300 shrink-0" />
              </button>
            ))
          )}
        </div>
      </div>
    </motion.div>
  );
}
