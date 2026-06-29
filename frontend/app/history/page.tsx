'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

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

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

  useEffect(() => {
    loadDashboard();
    loadMeetings();
  }, []);

  async function loadDashboard() {
    try {
      const response = await fetch(`${API_URL}/api/dashboard`);

      const data = await response.json();

      setStats(data);
    } catch (err) {
      console.error(err);
    }
  }

  async function loadMeetings() {
    try {
      const response = await fetch(`${API_URL}/api/meetings`);

      const data = await response.json();

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
      await fetch(`${API_URL}/api/meetings/${id}`, {
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
      <main className="mx-auto max-w-7xl p-10">
        <div className="rounded-3xl bg-white p-10 text-center shadow">
          <h2 className="text-2xl font-semibold text-slate-900">Loading Meeting History...</h2>
        </div>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-7xl p-10">
      <div className="mb-10">
        <h1 className="text-4xl font-bold text-slate-400">Meeting Dashboard</h1>

        <p className="mt-2 text-slate-500">Enterprise analytics for all analyzed meetings.</p>
      </div>

      {stats && (
        <div className="mb-10 grid gap-5 md:grid-cols-5">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-500">Total Meetings</p>

            <h2 className="mt-3 text-4xl font-bold text-slate-900">{stats.total_meetings}</h2>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-500">Avg Health</p>

            <h2 className="mt-3 text-4xl font-bold text-blue-600">{stats.average_health}</h2>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-500">Avg Risk</p>

            <h2 className="mt-3 text-4xl font-bold text-red-600">
              {(stats.average_risk_probability * 100).toFixed(0)}%
            </h2>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-500">High Risk</p>

            <h2 className="mt-3 text-4xl font-bold text-red-700">{stats.high_risk_meetings}</h2>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-500">Healthy</p>

            <h2 className="mt-3 text-4xl font-bold text-green-600">{stats.healthy_meetings}</h2>
          </div>
        </div>
      )}

      <div className="mb-10">
        <h2 className="text-3xl font-bold text-slate-400">Meeting History</h2>

        <p className="mt-2 text-slate-500">Previously analyzed meetings stored in MongoDB.</p>
      </div>

      {meetings.length === 0 ? (
        <div className="rounded-3xl bg-white p-10 text-center shadow">
          <h2 className="text-2xl font-semibold text-slate-900">No meetings found</h2>

          <p className="mt-3 text-slate-500">Analyze your first meeting to see it here.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {meetings.map((meeting) => {
            const healthColor =
              meeting.meeting_health_label === 'Healthy'
                ? 'bg-green-100 text-green-700'
                : meeting.meeting_health_label === 'Stable'
                  ? 'bg-blue-100 text-blue-700'
                  : meeting.meeting_health_label === 'Needs Attention'
                    ? 'bg-yellow-100 text-yellow-700'
                    : meeting.meeting_health_label === 'At Risk'
                      ? 'bg-orange-100 text-orange-700'
                      : 'bg-red-100 text-red-700';

            const riskColor =
              meeting.overall_risk_level.toLowerCase() === 'high'
                ? 'bg-red-100 text-red-700'
                : meeting.overall_risk_level.toLowerCase() === 'medium'
                  ? 'bg-yellow-100 text-yellow-700'
                  : 'bg-green-100 text-green-700';

            return (
              <div
                key={meeting._id}
                className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm transition hover:shadow-lg"
              >
                <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
                  <div className="flex-1">
                    <h3 className="text-2xl font-semibold text-slate-900">
                      {meeting.meeting_title}
                    </h3>

                    <p className="mt-2 text-sm text-slate-500">
                      {new Date(meeting.created_at).toLocaleString()}
                    </p>

                    <div className="mt-5 flex flex-wrap gap-3">
                      <span className={`rounded-full px-4 py-2 text-sm font-semibold ${riskColor}`}>
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

                  <div className="flex flex-wrap gap-3">
                    <Link
                      href={`/history/${meeting.meeting_id}`}
                      className="rounded-xl bg-slate-900 px-5 py-3 font-medium text-white transition hover:bg-slate-700"
                    >
                      View Report
                    </Link>

                    <button
                      onClick={() => deleteMeeting(meeting._id)}
                      className="rounded-xl bg-red-600 px-5 py-3 font-medium text-white transition hover:bg-red-700"
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
    </main>
  );
}
