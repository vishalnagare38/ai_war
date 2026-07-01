import { ReactNode } from "react";

export default function Pill({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-medium text-slate-700">
      {children}
    </span>
  );
}