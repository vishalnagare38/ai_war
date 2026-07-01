type Props = {
  title: string;
  subtitle?: string;
};

export default function LoadingScreen({
  title,
  subtitle,
}: Props) {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50">

      <div className="rounded-[32px] border border-slate-200 bg-white p-12 text-center shadow-sm">

        <div className="mx-auto mb-6 h-12 w-12 animate-spin rounded-full border-4 border-slate-200 border-t-blue-600" />

        <h1 className="text-2xl font-semibold text-slate-900">
          {title}
        </h1>

        {subtitle && (
          <p className="mt-3 text-slate-500">
            {subtitle}
          </p>
        )}

      </div>

    </main>
  );
}