/**
 * ExerciseBrowser
 * Full-screen modal with two tabs: Movements and Circuits.
 * Opened from HamburgerMenu via UI store's exercise-browser modal.
 */

import { useState } from 'react';
import { X, Dumbbell, Zap } from 'lucide-react';
import { motion } from 'framer-motion';
import { useUIStore } from '../../stores/ui.store';
import { MovementSearchTab } from './MovementSearchTab';
import { CircuitSearchTab } from './CircuitSearchTab';
import { cn } from '../../lib/utils';

type Tab = 'movements' | 'circuits';

export function ExerciseBrowser() {
  const activeModal = useUIStore((s) => s.activeModal);
  const closeModal = useUIStore((s) => s.closeModal);
  const [activeTab, setActiveTab] = useState<Tab>('movements');

  if (activeModal !== 'exercise-browser') return null;

  return (
    <div className="fixed inset-0 z-50 flex items-end md:items-center justify-center">
      {/* Backdrop */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="absolute inset-0 bg-black/50"
        onClick={closeModal}
      />

      {/* Panel */}
      <motion.div
        initial={{ y: 40, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        exit={{ y: 40, opacity: 0 }}
        transition={{ duration: 0.2, ease: 'easeOut' }}
        className={cn(
          'relative w-full max-w-lg max-h-[85vh] overflow-hidden',
          'bg-white dark:bg-surface-950 rounded-t-2xl md:rounded-2xl',
          'border border-surface-200 dark:border-surface-800',
          'shadow-2xl flex flex-col'
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-surface-200 dark:border-surface-800 shrink-0">
          <h2 className="text-base font-semibold text-surface-800 dark:text-surface-200">
            Exercise Browser
          </h2>
          <button
            type="button"
            onClick={closeModal}
            className="p-1.5 rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
          >
            <X className="w-4 h-4 text-surface-500" />
          </button>
        </div>

        {/* Tab bar */}
        <div className="flex border-b border-surface-200 dark:border-surface-800 shrink-0">
          <button
            type="button"
            onClick={() => setActiveTab('movements')}
            className={cn(
              'flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium transition-colors',
              activeTab === 'movements'
                ? 'text-primary-600 dark:text-primary-400 border-b-2 border-primary-500'
                : 'text-surface-400 dark:text-surface-500 hover:text-surface-600 dark:hover:text-surface-300'
            )}
          >
            <Dumbbell className="w-4 h-4" />
            Movements
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('circuits')}
            className={cn(
              'flex-1 flex items-center justify-center gap-2 py-3 text-sm font-medium transition-colors',
              activeTab === 'circuits'
                ? 'text-primary-600 dark:text-primary-400 border-b-2 border-primary-500'
                : 'text-surface-400 dark:text-surface-500 hover:text-surface-600 dark:hover:text-surface-300'
            )}
          >
            <Zap className="w-4 h-4" />
            Circuits
          </button>
        </div>

        {/* Tab content */}
        <div className="flex-1 overflow-y-auto p-4">
          {activeTab === 'movements' ? (
            <MovementSearchTab />
          ) : (
            <CircuitSearchTab />
          )}
        </div>
      </motion.div>
    </div>
  );
}
