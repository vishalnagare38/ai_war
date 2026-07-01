'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

import PageHeader from '@/components/PageHeader';
import MetricCard from '@/components/MetricCard';

interface Meeting {
  _id: string;
  meeting_id: string;
  meeting_title: string;
  overall_risk_level: string;
  meeting_health_score: number;
  meeting_health_label: string;
  created_at: string;
}

interface DashboardStats {
  total_meetings: number;
  average_health: number;
  average_risk_probability: number;
  high_risk_meetings: number;
  healthy_meetings: number;
}

export default function HistoryPage() {
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  const API = process.env.NEXT_PUBLIC_API_URL ?? 'http://127.0.0.1:8000';

  useEffect(() => {
    loadDashboard();
    loadMeetings();
  }, []);

  async function loadDashboard() {
    try {
      const res = await fetch(`${API}/api/dashboard`);
      const data = await res.json();
      setStats(data);
    } catch (err) {
      console.error(err);
    }
  }

  async function loadMeetings() {
    try {
      const res = await fetch(`${API}/api/meetings`);
      const data = await res.json();
      setMeetings(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function deleteMeeting(id: string) {
    if (!confirm('Delete this meeting?')) return;

    try {
      await fetch(`${API}/api/meetings/${id}`, {
        method: 'DELETE',
      });

      loadDashboard();
      loadMeetings();
    } catch (err) {
      console.error(err);
    }
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-50">
        <div className="mx-auto max-w-7xl px-6 py-12">
          <div className="rounded-[32px] border border-slate-200 bg-white p-12 text-center shadow-sm">
            <h2 className="text-3xl font-semibold text-slate-900">Loading Meeting History...</h2>
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
          title="Meeting History"
          description="Review every analyzed meeting, monitor historical project health, and revisit executive AI reports."
        />

        {stats && (
          <div className="mt-10 grid gap-5 md:grid-cols-2 xl:grid-cols-5">
            <MetricCard
              label="Meetings"
              value={stats.total_meetings.toString()}
              subtext="Stored Reports"
            />

            <MetricCard
              label="Average Health"
              value={`${stats.average_health}/100`}
              subtext="Historical Average"
            />

            <MetricCard
              label="Average Risk"
              value={`${(stats.average_risk_probability * 100).toFixed(0)}%`}
              subtext="ML Prediction"
            />

            <MetricCard
              label="High Risk"
              value={stats.high_risk_meetings.toString()}
              subtext="Projects"
            />

            <MetricCard
              label="Healthy"
              value={stats.healthy_meetings.toString()}
              subtext="Projects"
            />
          </div>
        )}

        <div className="mt-12">
          <h2 className="text-3xl font-semibold text-slate-900">Saved Executive Reports</h2>

          <p className="mt-2 text-slate-500">Every analyzed meeting stored inside MongoDB.</p>
        </div>

        {meetings.length === 0 ? (
          <div className="mt-8 rounded-[32px] border border-slate-200 bg-white p-12 text-center shadow-sm">
            <h3 className="text-2xl font-semibold text-slate-900">No Meeting Reports Found</h3>

            <p className="mt-3 text-slate-500">
              Analyze your first meeting to build historical intelligence.
            </p>
          </div>
        ) : (
          <div className="mt-8 space-y-6">
            {meetings.map((meeting) => {
              const riskColor =
                meeting.overall_risk_level === 'high'
                  ? 'bg-red-100 text-red-700'
                  : meeting.overall_risk_level === 'medium'
                    ? 'bg-amber-100 text-amber-700'
                    : 'bg-green-100 text-green-700';

              const healthColor =
                meeting.meeting_health_label === 'Healthy'
                  ? 'bg-green-100 text-green-700'
                  : meeting.meeting_health_label === 'Stable'
                    ? 'bg-blue-100 text-blue-700'
                    : meeting.meeting_health_label === 'Needs Attention'
                      ? 'bg-amber-100 text-amber-700'
                      : 'bg-red-100 text-red-700';

              return (
                <div
                  key={meeting._id}
                  className="rounded-[28px] border border-slate-200 bg-white p-8 shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
                >
                  <div className="flex flex-col gap-8 xl:flex-row xl:items-center xl:justify-between">
                    <div className="flex-1">
                      <h3 className="text-2xl font-semibold text-slate-900">
                        {meeting.meeting_title}
                      </h3>

                      <p className="mt-2 text-sm text-slate-500">
                        {new Date(meeting.created_at).toLocaleString()}
                      </p>

                      <div className="mt-6 flex flex-wrap gap-3">
                        <span
                          className={`rounded-full px-4 py-2 text-sm font-semibold ${riskColor}`}
                        >
                          {meeting.overall_risk_level.toUpperCase()}
                        </span>

                        <span className="rounded-full bg-blue-100 px-4 py-2 text-sm font-semibold text-blue-700">
                          {meeting.meeting_health_score}/100
                        </span>

                        <span
                          className={`rounded-full px-4 py-2 text-sm font-semibold ${healthColor}`}
                        >
                          {meeting.meeting_health_label}
                        </span>
                      </div>
                    </div>

                    <div className="flex gap-3">
                      <Link
                        href={`/history/${meeting.meeting_id}`}
                        className="rounded-2xl bg-slate-900 px-6 py-3 text-sm font-semibold !text-white transition hover:bg-slate-800"
                      >
                        View Report
                      </Link>

                      <button
                        onClick={() => deleteMeeting(meeting._id)}
                        className="rounded-2xl border border-red-200 bg-red-50 px-6 py-3 text-sm font-semibold text-red-700 transition hover:bg-red-100"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </main>
  );
}
