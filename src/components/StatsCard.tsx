interface StatsCardProps {
  label: string;
  value: string | number;
}

export default function StatsCard({ label, value }: StatsCardProps) {
  return (
    <div className="bg-white shadow rounded p-4">
      <div className="text-sm text-gray-500">{label}</div>
      <div className="text-2xl font-semibold text-primary">{value}</div>
    </div>
  );
}
