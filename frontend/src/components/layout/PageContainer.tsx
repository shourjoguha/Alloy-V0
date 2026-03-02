/**
 * PageContainer
 * Standard content padding wrapper.
 * Accounts for mobile BottomNav height via pb-20 on small screens.
 */

import type { ReactNode } from 'react';
import { cn } from '../../lib/utils';

interface PageContainerProps {
  children: ReactNode;
  className?: string;
  /** Remove horizontal padding (for full-bleed layouts) */
  noPadding?: boolean;
}

export function PageContainer({
  children,
  className,
  noPadding = false,
}: PageContainerProps) {
  return (
    <main
      className={cn(
        'flex-1 min-h-0 overflow-y-auto',
        // Mobile: pad bottom for BottomNav
        'pb-20 md:pb-6',
        !noPadding && 'px-4 pt-4 md:px-6 md:pt-6',
        className
      )}
    >
      {children}
    </main>
  );
}
