import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function ProfitChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis
          dataKey="created_at"
          tickFormatter={(v) => new Date(v).toLocaleDateString()}
        />
        <YAxis />
        <Tooltip />
        <Line
          type="monotone"
          dataKey="profit"
          stroke="#7c3aed"
          strokeWidth={3}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
