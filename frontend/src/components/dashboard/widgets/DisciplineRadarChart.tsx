/**
 * DisciplineRadarChart
 * Training discipline distribution radar (Strength, Endurance, etc.)
 * TODO: Derive from actual program session breakdown.
 */

import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip,
} from 'recharts';
import { THEME } from '../../../config/theme.config';
import { WidgetWrapper } from './WidgetWrapper';

const MOCK_DATA = [
  { discipline: 'Strength',   value: 80 },
  { discipline: 'Endurance',  value: 45 },
  { discipline: 'Mobility',   value: 60 },
  { discipline: 'Power',      value: 70 },
  { discipline: 'Hypertrophy', value: 55 },
];

export default function DisciplineRadarChart() {
  return (
    <WidgetWrapper id="discipline-radar" title="Discipline Balance">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={MOCK_DATA} margin={{ top: 10, right: 20, bottom: 10, left: 20 }}>
          <PolarGrid stroke={THEME.colors.surface[200]} />
          <PolarAngleAxis
            dataKey="discipline"
            tick={{ fontSize: 10, fill: THEME.colors.surface[500] }}
          />
          <PolarRadiusAxis
            angle={30}
            domain={[0, 100]}
            tick={false}
            axisLine={false}
          />
          <Tooltip
            contentStyle={{
              fontSize: 12,
              borderRadius: 8,
              border: `1px solid ${THEME.colors.surface[200]}`,
            }}
            formatter={(value: number | undefined) => [value != null ? `${value}%` : '—', 'Balance']}
          />
          <Radar
            name="Training Balance"
            dataKey="value"
            stroke={THEME.colors.primary[500]}
            fill={THEME.colors.primary[500]}
            fillOpacity={0.25}
          />
        </RadarChart>
      </ResponsiveContainer>
    </WidgetWrapper>
  );
}
