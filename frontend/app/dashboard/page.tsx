'use client';

import { useEffect, useState } from 'react';

type DashboardData = {
  total_meetings: number;
  average_health: number;
  average_risk_probability: number;
  high_risk_meetings: number;
  healthy_meetings: number;

  history_summary: string;
  recurring_blockers: string[];

  risk_trend: string[];
  health_trend: number[];

  project_momentum: string;
};

function MetricCard({
  title,
  value,
  color = 'text-slate-900',
}: {
  title: string;
  value: string | number;
  color?: string;
}) {
  return (
    <div className="rounded-3xl border border-slate-300 bg-white p-6 shadow-md transition hover:shadow-xl">
      <p className="text-sm font-semibold uppercase tracking-wide text-slate-500">{title}</p>

      <h2 className={`mt-4 text-4xl font-extrabold ${color}`}>{value}</h2>
    </div>
  );
}

export default function DashboardPage() {
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);

  const [loading, setLoading] = useState(true);

  const API = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    try {
      const response = await fetch(`${API}/api/dashboard`);

      const data = await response.json();

      setDashboard(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-50 via-white to-blue-50">
        <div className="rounded-3xl border border-slate-200 bg-white p-10 shadow-xl">
          <h1 className="text-3xl font-bold text-slate-900">Loading Dashboard...</h1>
        </div>
      </main>
    );
  }

  if (!dashboard) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-50 via-white to-blue-50">
        <div className="rounded-3xl border border-red-200 bg-white p-10 shadow-xl">
          <h1 className="text-3xl font-bold text-red-600">Dashboard unavailable.</h1>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
      <div className="mx-auto max-w-7xl p-10">
        <div className="mb-10">
          <div className="inline-flex rounded-full bg-blue-100 px-4 py-1 text-sm font-semibold text-blue-700">
            Enterprise Analytics
          </div>

          <h1 className="mt-4 text-5xl font-extrabold tracking-tight text-slate-900">
            Project Intelligence Dashboard
          </h1>

          <p className="mt-3 max-w-3xl text-lg text-slate-600">
            Historical insights generated from previous AI meeting analyses.
          </p>
        </div>

        <div className="grid gap-5 md:grid-cols-5">
          <MetricCard title="Meetings" value={dashboard.total_meetings} />

          <MetricCard
            title="Average Health"
            value={`${dashboard.average_health}/100`}
            color="text-blue-600"
          />

          <MetricCard
            title="Average Risk"
            value={`${(dashboard.average_risk_probability * 100).toFixed(0)}%`}
            color="text-red-600"
          />

          <MetricCard title="High Risk" value={dashboard.high_risk_meetings} color="text-red-600" />

          <MetricCard title="Healthy" value={dashboard.healthy_meetings} color="text-green-600" />
        </div>

        <div className="mt-10 rounded-3xl border border-slate-200 bg-white p-8 shadow-lg">
          <h2 className="text-3xl font-bold text-slate-900">Executive History Summary</h2>

          <p className="mt-5 leading-8 text-slate-700">{dashboard.history_summary}</p>
        </div>

        <div className="mt-10 grid gap-8 lg:grid-cols-2">
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-lg">
            <h2 className="mb-6 text-3xl font-bold text-slate-900">Recurring Blockers</h2>

            {dashboard.recurring_blockers.length === 0 ? (
              <p className="text-slate-500">No recurring blockers detected.</p>
            ) : (
              <div className="flex flex-wrap gap-3">
                {dashboard.recurring_blockers.map((item) => (
                  <span
                    key={item}
                    className="rounded-full border border-red-300 bg-red-100 px-5 py-2 text-sm font-bold text-red-800 shadow-sm"
                  >
                    {item}
                  </span>
                ))}
              </div>
            )}
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-lg">
            <h2 className="mb-6 text-3xl font-bold text-slate-900">Project Momentum</h2>

            <div
              className={`inline-flex rounded-2xl px-6 py-4 text-4xl font-extrabold shadow-md ${
                dashboard.project_momentum === 'Positive'
                  ? 'bg-green-100 text-green-700'
                  : dashboard.project_momentum === 'Negative'
                    ? 'bg-red-100 text-red-700'
                    : 'bg-yellow-100 text-yellow-700'
              }`}
            >
              {dashboard.project_momentum}
            </div>
          </div>
        </div>

        <div className="mt-10 grid gap-8 lg:grid-cols-2">
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-lg">
            <h2 className="mb-6 text-3xl font-bold text-slate-900">Risk Trend</h2>

            {dashboard.risk_trend.length === 0 ? (
              <p className="text-slate-500">No trend data available.</p>
            ) : (
              <div className="space-y-3">
                {dashboard.risk_trend.map((risk, index) => {
                  const badgeColor =
                    risk.toLowerCase() === 'high'
                      ? 'bg-red-100 text-red-700 border-red-300'
                      : risk.toLowerCase() === 'medium'
                        ? 'bg-yellow-100 text-yellow-700 border-yellow-300'
                        : 'bg-green-100 text-green-700 border-green-300';

                  return (
                    <div
                      key={index}
                      className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50 p-4 shadow-sm"
                    >
                      <span className="font-semibold text-slate-800">Meeting {index + 1}</span>

                      <span className={`rounded-full border px-4 py-1 font-bold ${badgeColor}`}>
                        {risk}
                      </span>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-lg">
            <h2 className="mb-6 text-3xl font-bold text-slate-900">Health Trend</h2>

            {dashboard.health_trend.length === 0 ? (
              <p className="text-slate-500">No health trend available.</p>
            ) : (
              <div className="space-y-5">
                {dashboard.health_trend.map((score, index) => (
                  <div
                    key={index}
                    className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm"
                  >
                    <div className="mb-3 flex items-center justify-between">
                      <span className="font-semibold text-slate-800">Meeting {index + 1}</span>

                      <span className="font-bold text-slate-900">{score}/100</span>
                    </div>

                    <div className="h-4 overflow-hidden rounded-full bg-slate-200">
                      <div
                        className={`h-full rounded-full ${
                          score >= 75
                            ? 'bg-green-600'
                            : score >= 50
                              ? 'bg-yellow-500'
                              : 'bg-red-600'
                        }`}
                        style={{
                          width: `${score}%`,
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
