/**
 * Body Map Configuration
 * Region definitions, severity colours, and type exports for the body map.
 */

import { THEME } from './theme.config';

export type BodyRegionId =
  | 'chest'
  | 'abs'
  | 'left-shoulder'
  | 'right-shoulder'
  | 'left-bicep'
  | 'right-bicep'
  | 'left-quad'
  | 'right-quad'
  // Back
  | 'upper-back'
  | 'lower-back'
  | 'left-tricep'
  | 'right-tricep'
  | 'left-hamstring'
  | 'right-hamstring'
  | 'glutes';

export type SeverityLevel = 0 | 1 | 2 | 3 | 4;

export interface BodyRegionDef {
  id: BodyRegionId;
  label: string;
  view: 'front' | 'back';
  /** SVG path d attribute */
  path: string;
}

/** Simplified body region paths (in a 200×400 viewBox) */
export const REGIONS: BodyRegionDef[] = [
  // Front
  { id: 'chest',          label: 'Chest',          view: 'front', path: 'M70,90 L130,90 L135,130 L65,130 Z' },
  { id: 'abs',            label: 'Abs',            view: 'front', path: 'M70,132 L130,132 L128,200 L72,200 Z' },
  { id: 'left-shoulder',  label: 'Left Shoulder',  view: 'front', path: 'M50,75 L70,75 L70,100 L45,100 Z' },
  { id: 'right-shoulder', label: 'Right Shoulder', view: 'front', path: 'M130,75 L150,75 L155,100 L130,100 Z' },
  { id: 'left-bicep',     label: 'Left Bicep',     view: 'front', path: 'M40,105 L60,105 L55,165 L35,165 Z' },
  { id: 'right-bicep',    label: 'Right Bicep',    view: 'front', path: 'M140,105 L165,105 L165,165 L145,165 Z' },
  { id: 'left-quad',      label: 'Left Quad',      view: 'front', path: 'M72,205 L97,205 L92,310 L68,310 Z' },
  { id: 'right-quad',     label: 'Right Quad',     view: 'front', path: 'M103,205 L128,205 L132,310 L108,310 Z' },
  // Back
  { id: 'upper-back',     label: 'Upper Back',     view: 'back',  path: 'M65,90 L135,90 L135,140 L65,140 Z' },
  { id: 'lower-back',     label: 'Lower Back',     view: 'back',  path: 'M70,142 L130,142 L128,190 L72,190 Z' },
  { id: 'glutes',         label: 'Glutes',         view: 'back',  path: 'M68,192 L132,192 L130,230 L70,230 Z' },
  { id: 'left-tricep',    label: 'Left Tricep',    view: 'back',  path: 'M40,105 L60,105 L55,165 L35,165 Z' },
  { id: 'right-tricep',   label: 'Right Tricep',   view: 'back',  path: 'M140,105 L165,105 L165,165 L145,165 Z' },
  { id: 'left-hamstring', label: 'Left Hamstring', view: 'back',  path: 'M72,232 L97,232 L92,320 L68,320 Z' },
  { id: 'right-hamstring',label: 'Right Hamstring',view: 'back',  path: 'M103,232 L128,232 L132,320 L108,320 Z' },
];

/** Severity level → fill colour mapping */
export const SEVERITY_COLORS: Record<SeverityLevel, string> = {
  0: THEME.colors.severity.none,
  1: THEME.colors.severity.low,
  2: THEME.colors.severity.medium,
  3: THEME.colors.severity.high,
  4: THEME.colors.severity.critical,
};

/** Severity level → human-readable label */
export const SEVERITY_LABELS: Record<SeverityLevel, string> = {
  0: 'None',
  1: 'Mild',
  2: 'Moderate',
  3: 'High',
  4: 'Severe',
};
