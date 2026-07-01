type TrendBadgeProps = {
  title: string;
  value: string;
};

export default function TrendBadge({
  title,
  value,
}: TrendBadgeProps) {
  const text = value.toLowerCase();

  let badge =
    "bg-slate-100 text-slate-700 border-slate-200";

  if (
    text.includes("improv") ||
    text.includes("positive") ||
    text.includes("decre")
  ) {
    badge =
      "bg-emerald-50 text-emerald-700 border-emerald-200";
  }

  if (
    text.includes("declin") ||
    text.includes("critical") ||
    text.includes("incre")
  ) {
    badge =
      "bg-red-50 text-red-700 border-red-200";
  }

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">

      <p className="text-sm font-medium text-slate-500">
        {title}
      </p>

      <div
        className={`mt-4 inline-flex rounded-full border px-4 py-2 text-sm font-semibold ${badge}`}
      >
        {value}
      </div>

    </div>
  );
}