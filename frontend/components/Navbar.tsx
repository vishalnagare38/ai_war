"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  {
    title: "Analyze",
    href: "/",
  },
  {
    title: "History",
    href: "/history",
  },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/80 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-8 py-4">

        <Link href="/">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">
              Meeting War Room
            </h1>

            <p className="text-sm text-slate-500">
              Multi-Agent AI Meeting Intelligence
            </p>
          </div>
        </Link>

        <nav className="flex items-center gap-3">

          {navItems.map((item) => {

            const active = pathname === item.href;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`rounded-xl px-5 py-2 font-medium transition ${
                  active
                    ? "bg-blue-600 text-white"
                    : "text-slate-700 hover:bg-slate-100"
                }`}
              >
                {item.title}
              </Link>
            );
          })}

        </nav>
      </div>
    </header>
  );
}