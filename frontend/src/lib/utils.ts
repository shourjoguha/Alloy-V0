/**
 * Utility Functions
 * Small, pure helpers. No side effects.
 */

import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

// ─── Tailwind Class Merger ────────────────────────────────────────────────────

/**
 * Merge Tailwind CSS classes safely, resolving conflicts.
 * This is the standard pattern from shadcn/ui.
 *
 * @example cn('px-4 py-2', isActive && 'bg-primary-500', className)
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

// ─── Number Formatters ────────────────────────────────────────────────────────

/** Format minutes as "Xh Ym" or "Ym" */
export function formatDuration(minutes: number): string {
  if (minutes < 60) return `${minutes}m`;
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return m === 0 ? `${h}h` : `${h}h ${m}m`;
}

/** Format a weight value with unit */
export function formatWeight(value: number, unit: 'kg' | 'lbs'): string {
  return `${value}${unit}`;
}

/** Convert kg to lbs */
export function kgToLbs(kg: number): number {
  return Math.round(kg * 2.20462 * 10) / 10;
}

/** Convert lbs to kg */
export function lbsToKg(lbs: number): number {
  return Math.round((lbs / 2.20462) * 10) / 10;
}

/** Clamp a number between min and max */
export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

// ─── String Formatters ────────────────────────────────────────────────────────

/** Convert snake_case or kebab-case to Title Case */
export function toTitleCase(str: string): string {
  return str
    .replace(/[-_]/g, ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

/** Capitalise the first letter only */
export function capitalise(str: string): string {
  if (!str) return str;
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/** Format day number (1–7) to day name */
export function dayNumberToName(day: number): string {
  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  return days[(day - 1) % 7] ?? 'Unknown';
}

// ─── Date Formatters ─────────────────────────────────────────────────────────

/** Format an ISO date string to a readable date */
export function formatDate(isoString: string): string {
  return new Intl.DateTimeFormat('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(new Date(isoString));
}

// ─── Array Helpers ────────────────────────────────────────────────────────────

/** Move an item in an array by index — returns a new array */
export function arrayMove<T>(arr: T[], from: number, to: number): T[] {
  const result = [...arr];
  const [removed] = result.splice(from, 1);
  if (removed !== undefined) result.splice(to, 0, removed);
  return result;
}
