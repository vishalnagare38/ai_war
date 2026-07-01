'use client';

import { useEffect, useState } from 'react';

import MetricCard from '@/components/MetricCard';
import PageHeader from '@/components/PageHeader';
import Section from '@/components/Section';
import TrendBadge from '@/components/TrendBadge';

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

function HealthRow({ meeting, score }: { meeting: number; score: number }) {
  const color =
    score >= 80
      ? 'bg-green-600'
      : score >= 60
        ? 'bg-blue-600'
        : score >= 40
          ? 'bg-amber-500'
          : 'bg-red-600';

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-700">Meeting {meeting}</span>

        <span className="text-sm font-semibold text-slate-900">{score}/100</span>
      </div>

      <div className="h-2 overflow-hidden rounded-full bg-slate-200">
        <div
          className={`h-full rounded-full ${color}`}
          style={{
            width: `${score}%`,
          }}
        />
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);

  const [loading, setLoading] = useState(true);

  const API = process.env.NEXT_PUBLIC_API_URL ?? 'http://127.0.0.1:8000';

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
      <main className="min-h-screen bg-slate-50">
        <div className="mx-auto max-w-7xl px-6 py-12">
          <div className="rounded-[32px] border border-slate-200 bg-white p-12 text-center shadow-sm">
            <h2 className="text-3xl font-semibold text-slate-900">Loading Dashboard...</h2>
          </div>
        </div>
      </main>
    );
  }

  if (!dashboard) {
    return (
      <main className="min-h-screen bg-slate-50">
        <div className="mx-auto max-w-7xl px-6 py-12">
          <div className="rounded-[32px] border border-red-200 bg-white p-12 text-center shadow-sm">
            <h2 className="text-3xl font-semibold text-red-600">Dashboard unavailable.</h2>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <PageHeader
          badge="Enterprise Intelligence"
          title="Project Intelligence Dashboard"
          description="Historical analytics generated from previous AI meeting analyses, showing long-term delivery trends, recurring blockers and overall project health."
        />

        <div className="mt-10 grid gap-5 md:grid-cols-2 xl:grid-cols-5">
          <MetricCard
            label="Meetings"
            value={dashboard.total_meetings.toString()}
            subtext="Stored Reports"
          />

          <MetricCard
            label="Average Health"
            value={`${dashboard.average_health}/100`}
            subtext="Historical Average"
          />

          <MetricCard
            label="Average Risk"
            value={`${(dashboard.average_risk_probability * 100).toFixed(0)}%`}
            subtext="ML Prediction"
          />

          <MetricCard
            label="High Risk"
            value={dashboard.high_risk_meetings.toString()}
            subtext="Projects"
          />

          <MetricCard
            label="Healthy"
            value={dashboard.healthy_meetings.toString()}
            subtext="Projects"
          />
        </div>

        <div className="mt-10 rounded-[32px] border border-slate-200 bg-white p-8 shadow-sm">
          <h2 className="text-3xl font-semibold text-slate-900">Executive Historical Summary</h2>

          <p className="mt-5 leading-8 text-slate-700">{dashboard.history_summary}</p>
        </div>

        <div className="mt-10 grid gap-8 xl:grid-cols-2">
          <Section title="Recurring Blockers" items={dashboard.recurring_blockers} />

          <div className="rounded-[32px] border border-slate-200 bg-white p-8 shadow-sm">
            <h2 className="text-3xl font-semibold text-slate-900">Project Momentum</h2>

            <p className="mt-3 text-slate-500">
              Overall delivery direction derived from historical meetings.
            </p>

            <div className="mt-8">
              <TrendBadge title="Current Momentum" value={dashboard.project_momentum} />
            </div>
          </div>
        </div>

        <div className="mt-10 grid gap-8 xl:grid-cols-2">
          <div className="rounded-[32px] border border-slate-200 bg-white p-8 shadow-sm">
            <h2 className="text-3xl font-semibold text-slate-900">Risk Trend</h2>

            <p className="mt-2 text-slate-500">Risk evolution across previous meetings.</p>

            <div className="mt-8 space-y-4">
              {dashboard.risk_trend.length === 0 ? (
                <p className="text-slate-500">No historical trend available.</p>
              ) : (
                dashboard.risk_trend.map((risk, index) => {
                  const badge =
                    risk.toLowerCase() === 'high'
                      ? 'bg-red-100 text-red-700'
                      : risk.toLowerCase() === 'medium'
                        ? 'bg-amber-100 text-amber-700'
                        : 'bg-green-100 text-green-700';

                  return (
                    <div
                      key={index}
                      className="flex items-center justify-between rounded-2xl border border-slate-200 bg-slate-50 px-5 py-4"
                    >
                      <span className="font-medium text-slate-700">Meeting {index + 1}</span>

                      <span className={`rounded-full px-4 py-2 text-sm font-semibold ${badge}`}>
                        {risk}
                      </span>
                    </div>
                  );
                })
              )}
            </div>
          </div>

          <div className="rounded-[32px] border border-slate-200 bg-white p-8 shadow-sm">
            <h2 className="text-3xl font-semibold text-slate-900">Health Trend</h2>

            <p className="mt-2 text-slate-500">Historical project health across meetings.</p>

            <div className="mt-8 space-y-6">
              {dashboard.health_trend.length === 0 ? (
                <p className="text-slate-500">No historical health available.</p>
              ) : (
                dashboard.health_trend.map((score, index) => (
                  <HealthRow key={index} meeting={index + 1} score={score} />
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
