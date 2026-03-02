/**
 * Theme Configuration
 * JS mirror of CSS custom properties defined in index.css @theme block.
 * Use this when you need color/radius values in JavaScript (e.g. SVG fills, chart colors).
 * For Tailwind classes, always use the utility class directly.
 */

export const THEME = {
  colors: {
    primary: {
      50: '#f0f9ff',
      100: '#e0f2fe',
      200: '#bae6fd',
      300: '#7dd3fc',
      400: '#38bdf8',
      500: '#0ea5e9',
      600: '#0284c7',
      700: '#0369a1',
      800: '#075985',
      900: '#0c4a6e',
      950: '#082f49',
    },
    secondary: {
      50: '#fdf4ff',
      100: '#fae8ff',
      200: '#f5d0fe',
      300: '#f0abfc',
      400: '#e879f9',
      500: '#d946ef',
      600: '#c026d3',
      700: '#a21caf',
      800: '#86198f',
      900: '#701a75',
      950: '#4a044e',
    },
    surface: {
      50: '#fafafa',
      100: '#f4f4f5',
      200: '#e4e4e7',
      300: '#d4d4d8',
      400: '#a1a1aa',
      500: '#71717a',
      600: '#52525b',
      700: '#3f3f46',
      800: '#27272a',
      900: '#18181b',
      950: '#09090b',
    },
    /** Severity scale used for body map and readiness logging */
    severity: {
      none: '#22c55e',
      low: '#84cc16',
      medium: '#eab308',
      high: '#f97316',
      critical: '#ef4444',
    },
    semantic: {
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#3b82f6',
    },
  },

  radius: {
    sm: '0.25rem',
    md: '0.375rem',
    lg: '0.5rem',
    xl: '0.75rem',
    '2xl': '1rem',
    full: '9999px',
  },

  /** Chart color palette — ordered for consistent series coloring */
  chartColors: [
    '#0ea5e9', // primary-500
    '#d946ef', // secondary-500
    '#10b981', // success
    '#f59e0b', // warning
    '#3b82f6', // info
    '#f97316', // severity-high
  ],
} as const;

export type SeverityLevel = keyof typeof THEME.colors.severity;
