/**
 * VolumeLoadChart
 * Weekly total training volume (kg × reps) over the past 8 weeks.
 * TODO: Wire to real API query when exercise logging is implemented.
 */

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { THEME } from '../../../config/theme.config';
import { WidgetWrapper } from './WidgetWrapper';

const MOCK_DATA = [
  { week: 'W1', volume: 7800 },
  { week: 'W2', volume: 8400 },
  { week: 'W3', volume: 8100 },
  { week: 'W4', volume: 9200 },
  { week: 'W5', volume: 8900 },
  { week: 'W6', volume: 9600 },
  { week: 'W7', volume: 10100 },
  { week: 'W8', volume: 9800 },
];

export default function VolumeLoadChart() {
  return (
    <WidgetWrapper id="volume-load" title="Volume Load">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={MOCK_DATA} margin={{ top: 4, right: 4, bottom: 0, left: -20 }}>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke={THEME.colors.surface[200]}
            vertical={false}
          />
          <XAxis
            dataKey="week"
            tick={{ fontSize: 11, fill: THEME.colors.surface[400] }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            tick={{ fontSize: 11, fill: THEME.colors.surface[400] }}
            axisLine={false}
            tickLine={false}
            tickFormatter={(v: number) => `${(v / 1000).toFixed(0)}k`}
          />
          <Tooltip
            contentStyle={{
              fontSize: 12,
              borderRadius: 8,
              border: `1px solid ${THEME.colors.surface[200]}`,
            }}
            formatter={(value: number | undefined) => [value != null ? `${value.toLocaleString()} kg` : '—', 'Volume']}
            cursor={{ fill: THEME.colors.surface[100] }}
          />
          <Bar
            dataKey="volume"
            fill={THEME.colors.primary[500]}
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </WidgetWrapper>
  );
}
