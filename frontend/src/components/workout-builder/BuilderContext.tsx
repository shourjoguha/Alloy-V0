/**
 * BuilderContext
 * Provides DnD context and manages the exercise list state for the workout builder.
 */

import { createContext, useContext, useState, useCallback, type ReactNode } from 'react';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  type DragEndEvent,
} from '@dnd-kit/core';
import {
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { arrayMove } from '../../lib/utils';

// ─── Types ──────────────────────────────────────────────────────────────────

export interface BuilderExercise {
  id: string;
  name: string;
  sets: number;
  reps: string;
  restSeconds: number;
  equipment?: string;
  notes?: string;
}

interface BuilderState {
  exercises: BuilderExercise[];
  expandedSwapId: string | null;
  isDirty: boolean;
}

interface BuilderActions {
  reorderExercises: (from: number, to: number) => void;
  removeExercise: (id: string) => void;
  addExercise: (exercise: BuilderExercise) => void;
  swapExercise: (oldId: string, replacement: BuilderExercise) => void;
  setExpandedSwapId: (id: string | null) => void;
  reset: () => void;
}

type BuilderContextType = BuilderState & BuilderActions;

// ─── Context ────────────────────────────────────────────────────────────────

const Ctx = createContext<BuilderContextType | null>(null);

export function useBuilder() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('useBuilder must be used within <BuilderProvider>');
  return ctx;
}

// ─── Provider ───────────────────────────────────────────────────────────────

interface BuilderProviderProps {
  initialExercises: BuilderExercise[];
  children: ReactNode;
}

export function BuilderProvider({ initialExercises, children }: BuilderProviderProps) {
  const [exercises, setExercises] = useState<BuilderExercise[]>(initialExercises);
  const [expandedSwapId, setExpandedSwapId] = useState<string | null>(null);
  const [isDirty, setIsDirty] = useState(false);

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 8 } }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const reorderExercises = useCallback((from: number, to: number) => {
    setExercises((prev) => arrayMove(prev, from, to));
    setIsDirty(true);
  }, []);

  const removeExercise = useCallback((id: string) => {
    setExercises((prev) => prev.filter((e) => e.id !== id));
    setIsDirty(true);
  }, []);

  const addExercise = useCallback((exercise: BuilderExercise) => {
    setExercises((prev) => [...prev, exercise]);
    setIsDirty(true);
  }, []);

  const swapExercise = useCallback((oldId: string, replacement: BuilderExercise) => {
    setExercises((prev) =>
      prev.map((e) => (e.id === oldId ? replacement : e))
    );
    setExpandedSwapId(null);
    setIsDirty(true);
  }, []);

  const reset = useCallback(() => {
    setExercises(initialExercises);
    setExpandedSwapId(null);
    setIsDirty(false);
  }, [initialExercises]);

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    if (over && active.id !== over.id) {
      const oldIdx = exercises.findIndex((e) => e.id === active.id);
      const newIdx = exercises.findIndex((e) => e.id === over.id);
      if (oldIdx !== -1 && newIdx !== -1) {
        reorderExercises(oldIdx, newIdx);
      }
    }
  }

  const ctx: BuilderContextType = {
    exercises,
    expandedSwapId,
    isDirty,
    reorderExercises,
    removeExercise,
    addExercise,
    swapExercise,
    setExpandedSwapId,
    reset,
  };

  return (
    <Ctx.Provider value={ctx}>
      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragEnd={handleDragEnd}
      >
        <SortableContext
          items={exercises.map((e) => e.id)}
          strategy={verticalListSortingStrategy}
        >
          {children}
        </SortableContext>
      </DndContext>
    </Ctx.Provider>
  );
}
