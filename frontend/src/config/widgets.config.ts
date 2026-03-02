/**
 * Widget Configuration
 * Pure metadata for dashboard widgets — no component references.
 * WidgetRegistry.ts imports from here and attaches lazy-loaded components.
 */

export type WidgetSize = 'sm' | 'md' | 'lg';

export interface WidgetMeta {
  id: string;
  name: string;
  description: string;
  /** Default grid span — sm=1 col, md=1 col, lg=2 cols on desktop */
  defaultSize: WidgetSize;
}

export const WIDGET_META: Record<string, WidgetMeta> = {
  'volume-load': {
    id: 'volume-load',
    name: 'Volume Load',
    description: 'Weekly training volume (total kg × reps)',
    defaultSize: 'md',
  },
  'one-rm-trend': {
    id: 'one-rm-trend',
    name: '1RM Trend',
    description: 'Estimated 1-rep max progression for key lifts',
    defaultSize: 'lg',
  },
  'session-completion': {
    id: 'session-completion',
    name: 'Session Completion',
    description: 'Completed vs planned sessions per week',
    defaultSize: 'md',
  },
  'discipline-radar': {
    id: 'discipline-radar',
    name: 'Discipline Balance',
    description: 'Radar overview of training discipline distribution',
    defaultSize: 'sm',
  },
};

/** All widget IDs in preferred display order */
export const ALL_WIDGET_IDS = Object.keys(WIDGET_META);

/** Default widgets shown to a new user */
export const DEFAULT_WIDGET_IDS = ['volume-load', 'one-rm-trend', 'session-completion'];
