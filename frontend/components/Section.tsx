type SectionProps = {
  title: string;
  items?: string[];
};

export default function Section({
  title,
  items = [],
}: SectionProps) {
  if (items.length === 0) return null;

  return (
    <section className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">

      <div className="border-b border-slate-200 px-7 py-5">

        <h2 className="text-xl font-semibold tracking-tight text-slate-900">
          {title}
        </h2>

      </div>

      <div className="space-y-4 p-7">

        {items.map((item, index) => (

          <div
            key={index}
            className="rounded-2xl border border-slate-100 bg-slate-50 px-5 py-4 transition-all duration-200 hover:border-blue-200 hover:bg-white"
          >

            <div className="flex items-start gap-4">

              <div className="mt-1 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-blue-600 text-xs font-semibold text-white">
                {index + 1}
              </div>

              <p className="leading-7 text-slate-700">
                {item}
              </p>

            </div>

          </div>

        ))}

      </div>

    </section>
  );
}