/**
 * OneRMTrendChart
 * Estimated 1-rep max progression for Squat, Bench, Deadlift.
 * TODO: Wire to real API query when exercise logging is implemented.
 */

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { THEME } from '../../../config/theme.config';
import { WidgetWrapper } from './WidgetWrapper';

const MOCK_DATA = [
  { week: 'W1',  squat: 100, bench: 75,  deadlift: 120 },
  { week: 'W2',  squat: 102, bench: 77,  deadlift: 122 },
  { week: 'W3',  squat: 102, bench: 77,  deadlift: 125 },
  { week: 'W4',  squat: 105, bench: 80,  deadlift: 127 },
  { week: 'W5',  squat: 105, bench: 80,  deadlift: 130 },
  { week: 'W6',  squat: 107, bench: 82,  deadlift: 130 },
  { week: 'W7',  squat: 110, bench: 82,  deadlift: 132 },
  { week: 'W8',  squat: 110, bench: 85,  deadlift: 135 },
  { week: 'W9',  squat: 112, bench: 85,  deadlift: 137 },
  { week: 'W10', squat: 115, bench: 87,  deadlift: 140 },
  { week: 'W11', squat: 115, bench: 87,  deadlift: 142 },
  { week: 'W12', squat: 117, bench: 90,  deadlift: 145 },
];

const [c1, c2, c3] = THEME.chartColors;

export default function OneRMTrendChart() {
  return (
    <WidgetWrapper id="one-rm-trend" title="1RM Trend">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={MOCK_DATA} margin={{ top: 4, right: 4, bottom: 0, left: -20 }}>
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
            interval={2}
          />
          <YAxis
            tick={{ fontSize: 11, fill: THEME.colors.surface[400] }}
            axisLine={false}
            tickLine={false}
            tickFormatter={(v: number) => `${v}kg`}
            domain={['auto', 'auto']}
          />
          <Tooltip
            contentStyle={{
              fontSize: 12,
              borderRadius: 8,
              border: `1px solid ${THEME.colors.surface[200]}`,
            }}
            formatter={(value: number | undefined, name: string | undefined) => [value != null ? `${value}kg` : '—', name ?? '']}
          />
          <Legend
            iconType="circle"
            iconSize={8}
            wrapperStyle={{ fontSize: 11, paddingTop: 4 }}
          />
          <Line
            type="monotone"
            dataKey="squat"
            stroke={c1}
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="bench"
            stroke={c2}
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4 }}
          />
          <Line
            type="monotone"
            dataKey="deadlift"
            stroke={c3}
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </WidgetWrapper>
  );
}
