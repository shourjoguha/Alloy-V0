/**
 * Card
 * Surface container with optional header, content, and footer slots.
 * Supports variants: default | interactive | selected | grouped
 */

import * as React from 'react';
import { cn } from '../../lib/utils';

type CardVariant = 'default' | 'interactive' | 'selected' | 'grouped';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: CardVariant;
}

const VARIANT_CLASSES: Record<CardVariant, string> = {
  default:
    'border border-surface-200 dark:border-surface-800 shadow-sm',
  interactive:
    'border border-surface-200 dark:border-surface-800 shadow-sm cursor-pointer hover:shadow-md hover:border-primary-200 dark:hover:border-primary-800 active:scale-[0.99] transition-all',
  selected:
    'ring-2 ring-primary-500 bg-primary-50 dark:bg-primary-900/20 shadow-sm',
  grouped:
    'shadow-[0_1px_3px_rgba(0,0,0,0.04),0_1px_2px_rgba(0,0,0,0.06)] border-0',
};

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = 'default', ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        'rounded-xl bg-white dark:bg-surface-900',
        VARIANT_CLASSES[variant],
        className
      )}
      {...props}
    />
  )
);
Card.displayName = 'Card';

export const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex flex-col gap-1.5 p-5 pb-0', className)}
    {...props}
  />
));
CardHeader.displayName = 'CardHeader';

export const CardTitle = React.forwardRef<
  HTMLHeadingElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      'text-base font-semibold text-surface-900 dark:text-surface-50 leading-tight',
      className
    )}
    {...props}
  />
));
CardTitle.displayName = 'CardTitle';

export const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn('text-sm text-surface-500 dark:text-surface-400', className)}
    {...props}
  />
));
CardDescription.displayName = 'CardDescription';

export const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('p-5', className)} {...props} />
));
CardContent.displayName = 'CardContent';

export const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      'flex items-center p-5 pt-0 border-t border-surface-100 dark:border-surface-800 mt-4',
      className
    )}
    {...props}
  />
));
CardFooter.displayName = 'CardFooter';
