/**
 * PageTransition
 * Wraps a page in a Framer Motion fade+slide animation.
 * Apply as the outermost wrapper inside each route component.
 */

import { motion } from 'framer-motion';
import type { ReactNode } from 'react';

const variants = {
  initial: { opacity: 0, y: 6 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -4 },
};

interface PageTransitionProps {
  children: ReactNode;
  /** Unique key so AnimatePresence tracks route changes */
  routeKey: string;
}

export function PageTransition({ children, routeKey }: PageTransitionProps) {
  return (
    <motion.div
      key={routeKey}
      variants={variants}
      initial="initial"
      animate="animate"
      exit="exit"
      transition={{ duration: 0.18, ease: 'easeOut' }}
      className="flex flex-col flex-1 h-full"
    >
      {children}
    </motion.div>
  );
}
