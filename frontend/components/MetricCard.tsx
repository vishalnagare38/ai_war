type MetricCardProps = {
  label: string;
  value: string | number;
  subtext?: string;
};

export default function MetricCard({
  label,
  value,
  subtext,
}: MetricCardProps) {
  const text = String(value).toLowerCase();

  let valueColor = "text-slate-900";
  let badgeColor = "bg-slate-100 text-slate-700";

  if (text.includes("high")) {
    valueColor = "text-red-600";
    badgeColor = "bg-red-50 text-red-700";
  } else if (text.includes("medium")) {
    valueColor = "text-amber-600";
    badgeColor = "bg-amber-50 text-amber-700";
  } else if (text.includes("low")) {
    valueColor = "text-emerald-600";
    badgeColor = "bg-emerald-50 text-emerald-700";
  } else if (text.includes("/100")) {
    valueColor = "text-blue-600";
    badgeColor = "bg-blue-50 text-blue-700";
  } else if (text.includes("%")) {
    valueColor = "text-indigo-600";
    badgeColor = "bg-indigo-50 text-indigo-700";
  }

  return (
    <div className="group rounded-3xl border border-slate-200 bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:border-slate-300 hover:shadow-lg">

      <div className="flex items-start justify-between">

        <div>

          <p className="text-sm font-medium text-slate-500">
            {label}
          </p>

          <h2 className={`mt-3 text-4xl font-semibold tracking-tight ${valueColor}`}>
            {value}
          </h2>

          {subtext && (
            <p className="mt-3 text-sm leading-6 text-slate-500">
              {subtext}
            </p>
          )}

        </div>

        <div
          className={`rounded-2xl px-3 py-2 text-xs font-semibold ${badgeColor}`}
        >
          Live
        </div>

      </div>

    </div>
  );
}