'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navigation = [
  {
    title: 'Analyze',
    href: '/',
  },
  {
    title: 'History',
    href: '/history',
  },
  {
    title: 'Dashboard',
    href: '/dashboard',
  },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/80 bg-white/90 backdrop-blur-xl">
      <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-6">
        <Link href="/" className="group">
          <div className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-900 text-lg font-bold text-white shadow-sm transition group-hover:scale-105">
              MW
            </div>

            <div>
              <h1 className="text-xl font-semibold tracking-tight text-slate-900">
                Meeting War Room
              </h1>

              <p className="mt-0.5 text-sm text-slate-500">Enterprise Multi-Agent Intelligence</p>
            </div>
          </div>
        </Link>

        <nav className="flex items-center gap-2 rounded-2xl border border-slate-200 bg-slate-50 p-1">
          {navigation.map((item) => {
            const active = pathname === item.href;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`rounded-xl px-5 py-2.5 text-sm font-medium transition-all duration-200 ${
                  active
                    ? 'bg-slate-900 !text-white shadow-sm'
                    : 'text-slate-600 hover:bg-white hover:text-slate-900'
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
