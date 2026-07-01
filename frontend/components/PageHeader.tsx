import { ReactNode } from "react";

type Props = {
  badge?: string;
  title: string;
  description: string;
  children?: ReactNode;
};

export default function PageHeader({
  badge,
  title,
  description,
  children,
}: Props) {
  return (
    <div className="rounded-[32px] border border-slate-200 bg-white p-8 shadow-sm">

      {badge && (
        <div className="inline-flex rounded-full bg-blue-50 px-4 py-1.5 text-sm font-medium text-blue-700">
          {badge}
        </div>
      )}

      <h1 className="mt-5 text-5xl font-semibold tracking-tight text-slate-900">
        {title}
      </h1>

      <p className="mt-4 max-w-3xl text-lg leading-8 text-slate-600">
        {description}
      </p>

      {children && (
        <div className="mt-8">
          {children}
        </div>
      )}

    </div>
  );
}