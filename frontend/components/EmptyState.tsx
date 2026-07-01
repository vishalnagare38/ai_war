type Props = {
  title: string;
  description: string;
};

export default function EmptyState({
  title,
  description,
}: Props) {
  return (
    <div className="rounded-[32px] border border-dashed border-slate-300 bg-white p-12 text-center">

      <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-slate-100 text-3xl">
        📄
      </div>

      <h2 className="mt-6 text-2xl font-semibold text-slate-900">
        {title}
      </h2>

      <p className="mx-auto mt-3 max-w-xl text-slate-500">
        {description}
      </p>

    </div>
  );
}