/**
 * Widget Registry
 * Central catalogue of all available dashboard widgets.
 * Attaches lazy-loaded components to metadata from widgets.config.ts.
 */

import { lazy, type LazyExoticComponent, type ComponentType } from 'react';
import {
  WIDGET_META,
  ALL_WIDGET_IDS,
  DEFAULT_WIDGET_IDS,
  type WidgetMeta,
  type WidgetSize,
} from '../../../config/widgets.config';

export type { WidgetSize };

export interface WidgetDefinition extends WidgetMeta {
  /** Lazy-loaded component — enables per-widget code splitting */
  component: LazyExoticComponent<ComponentType>;
}

/** Map of widget ID → lazy component import */
const WIDGET_COMPONENTS: Record<string, LazyExoticComponent<ComponentType>> = {
  'volume-load':        lazy(() => import('./VolumeLoadChart')),
  'one-rm-trend':       lazy(() => import('./OneRMTrendChart')),
  'session-completion': lazy(() => import('./SessionCompletionChart')),
  'discipline-radar':   lazy(() => import('./DisciplineRadarChart')),
};

/** Full widget definitions: metadata + lazy component */
export const WIDGET_REGISTRY: Record<string, WidgetDefinition> = Object.fromEntries(
  Object.entries(WIDGET_META).map(([id, meta]) => [
    id,
    { ...meta, component: WIDGET_COMPONENTS[id] },
  ]),
) as Record<string, WidgetDefinition>;

export { ALL_WIDGET_IDS, DEFAULT_WIDGET_IDS };
