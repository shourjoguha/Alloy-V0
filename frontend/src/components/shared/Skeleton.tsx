/**
 * Skeleton
 * Shimmer-animated placeholder for loading states.
 * Uses the `.skeleton` CSS utility from index.css.
 */

import { cn } from '../../lib/utils';

type SkeletonVariant = 'text' | 'circle' | 'rect';

interface SkeletonProps {
  /** Shape of the skeleton placeholder */
  variant?: SkeletonVariant;
  /** Width — Tailwind class or CSS value */
  width?: string;
  /** Height — Tailwind class or CSS value */
  height?: string;
  className?: string;
}

const VARIANT_CLASSES: Record<SkeletonVariant, string> = {
  text: 'rounded-full',
  circle: 'rounded-full aspect-square',
  rect: 'rounded-xl',
};

export function Skeleton({
  variant = 'rect',
  width,
  height,
  className,
}: SkeletonProps) {
  return (
    <div
      className={cn(
        'skeleton',
        VARIANT_CLASSES[variant],
        width,
        height,
        className
      )}
      aria-hidden="true"
    />
  );
}
