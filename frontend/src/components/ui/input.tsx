/**
 * Input
 * Styled form text input. Use with React Hook Form via {...register('field')}.
 */

import * as React from 'react';
import { cn } from '../../lib/utils';

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: boolean;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, error, ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={cn(
          'flex h-9 w-full rounded-lg border bg-white px-3 py-2 text-sm',
          'dark:bg-surface-900',
          'placeholder:text-surface-400 dark:placeholder:text-surface-600',
          'text-surface-900 dark:text-surface-50',
          'transition-colors',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500',
          'disabled:cursor-not-allowed disabled:opacity-50',
          error
            ? 'border-error focus-visible:ring-error'
            : 'border-surface-200 dark:border-surface-700',
          className
        )}
        {...props}
      />
    );
  }
);
Input.displayName = 'Input';

/** Inline error message — renders below an input */
export function InputError({ message }: { message?: string }) {
  if (!message) return null;
  return (
    <p className="mt-1 text-xs text-error" role="alert">
      {message}
    </p>
  );
}

/** Label for an input */
export function Label({
  className,
  ...props
}: React.LabelHTMLAttributes<HTMLLabelElement>) {
  return (
    <label
      className={cn(
        'block text-sm font-medium text-surface-700 dark:text-surface-300 mb-1',
        className
      )}
      {...props}
    />
  );
}
