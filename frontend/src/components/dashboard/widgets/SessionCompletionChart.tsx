/**
 * SessionCompletionChart
 * Completed vs planned sessions per week.
 * TODO: Wire to real API query when session tracking is implemented.
 */

import {
  BarChart,
  Bar,
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
  { week: 'W1', completed: 3, missed: 1 },
  { week: 'W2', completed: 4, missed: 0 },
  { week: 'W3', completed: 3, missed: 1 },
  { week: 'W4', completed: 4, missed: 0 },
  { week: 'W5', completed: 2, missed: 2 },
  { week: 'W6', completed: 4, missed: 0 },
  { week: 'W7', completed: 4, missed: 0 },
  { week: 'W8', completed: 3, missed: 1 },
];

export default function SessionCompletionChart() {
  return (
    <WidgetWrapper id="session-completion" title="Session Completion">
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
            allowDecimals={false}
          />
          <Tooltip
            contentStyle={{
              fontSize: 12,
              borderRadius: 8,
              border: `1px solid ${THEME.colors.surface[200]}`,
            }}
            formatter={(value: number | undefined, name: string | undefined) => [
              value != null ? `${value} sessions` : '—',
              name ? name.charAt(0).toUpperCase() + name.slice(1) : '',
            ]}
          />
          <Legend
            iconType="circle"
            iconSize={8}
            wrapperStyle={{ fontSize: 11, paddingTop: 4 }}
          />
          <Bar
            dataKey="completed"
            stackId="a"
            fill={THEME.colors.semantic.success}
            radius={[0, 0, 0, 0]}
          />
          <Bar
            dataKey="missed"
            stackId="a"
            fill={THEME.colors.surface[200]}
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </WidgetWrapper>
  );
}
