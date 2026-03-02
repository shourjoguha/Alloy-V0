/**
 * Toast Helpers
 * Typed convenience wrappers around Sonner's toast() API.
 * Ensures consistent messaging patterns for mutation feedback.
 *
 * Usage:
 *   import { showSuccess, showError, showMutationResult } from '@/lib/toast';
 *   showSuccess('Profile saved');
 *   showError('Upload failed', { description: 'File too large' });
 */

import { toast } from 'sonner';

interface ToastOptions {
  description?: string;
  duration?: number;
}

/** Green success toast */
export function showSuccess(message: string, options?: ToastOptions): void {
  toast.success(message, {
    description: options?.description,
    duration: options?.duration ?? 4000,
  });
}

/** Red error toast — pass trace_id for support reference */
export function showError(
  message: string,
  options?: ToastOptions & { trace_id?: string }
): void {
  const description = options?.trace_id
    ? `${options.description ?? 'Something went wrong.'} (ref: ${options.trace_id})`
    : options?.description;

  toast.error(message, {
    description,
    duration: options?.duration ?? 6000,
  });
}

/** Amber warning toast */
export function showWarning(message: string, options?: ToastOptions): void {
  toast.warning(message, {
    description: options?.description,
    duration: options?.duration ?? 5000,
  });
}

/** Blue info toast */
export function showInfo(message: string, options?: ToastOptions): void {
  toast.info(message, {
    description: options?.description,
    duration: options?.duration ?? 4000,
  });
}

/**
 * Convenience for API mutation results.
 * Checks result.success and shows appropriate toast.
 *
 * @example
 *   const result = await mutation.mutateAsync(payload);
 *   showMutationResult(result, 'Program generated!');
 */
export function showMutationResult(
  result: { success: boolean; errors?: string[]; warnings?: string[] },
  successMessage: string
): void {
  if (result.success) {
    showSuccess(successMessage);

    if (result.warnings?.length) {
      result.warnings.forEach((w) => showWarning(w));
    }
  } else {
    const errorMsg = result.errors?.[0] ?? 'Operation failed';
    showError(errorMsg, {
      description: 'Please try again or contact support.',
    });
  }
}
