'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';

import MetricCard from '@/components/MetricCard';
import Section from '@/components/Section';
import PageHeader from '@/components/PageHeader';

function TimelineCard({ agent, time, total }: { agent: string; time: number; total: number }) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="font-medium text-slate-700">{agent}</span>

        <span className="text-sm text-slate-500">{time.toFixed(2)}s</span>
      </div>

      <div className="h-2 overflow-hidden rounded-full bg-slate-200">
        <div
          className="h-full rounded-full bg-blue-600 transition-all duration-700"
          style={{
            width: `${Math.min((time / total) * 100, 100)}%`,
          }}
        />
      </div>
    </div>
  );
}

export default function MeetingDetails() {
  const { id } = useParams();

  const router = useRouter();

  const [meeting, setMeeting] = useState<any>(null);

  const [loading, setLoading] = useState(true);

  const API = process.env.NEXT_PUBLIC_API_URL ?? 'http://127.0.0.1:8000';

  useEffect(() => {
    loadMeeting();
  }, []);

  async function loadMeeting() {
    try {
      const res = await fetch(`${API}/api/meetings/${id}`);

      if (!res.ok) {
        setLoading(false);
        return;
      }

      const data = await res.json();

      setMeeting(data);
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
            <h2 className="text-3xl font-semibold text-slate-900">Loading Executive Report...</h2>
          </div>
        </div>
      </main>
    );
  }

  if (!meeting) {
    return (
      <main className="min-h-screen bg-slate-50">
        <div className="mx-auto max-w-7xl px-6 py-12">
          <div className="rounded-[32px] border border-slate-200 bg-white p-12 text-center shadow-sm">
            <h2 className="text-3xl font-semibold text-slate-900">Meeting Not Found</h2>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <button
          onClick={() => router.back()}
          className="mb-8 rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-100"
        >
          ← Back
        </button>

        <PageHeader
          badge="Executive Report"
          title={meeting.meeting_title}
          description={new Date(meeting.created_at).toLocaleString()}
        />

        <div className="mt-10 grid gap-5 md:grid-cols-2 xl:grid-cols-4">
          <MetricCard
            label="Overall Risk"
            value={meeting.overall_risk_level.toUpperCase()}
            subtext="Coordinator Assessment"
          />

          <MetricCard
            label="ML Risk"
            value={`${(meeting.ml_risk_probability * 100).toFixed(1)}%`}
            subtext="Predictive Analytics"
          />

          <MetricCard
            label="Consensus"
            value={`${(meeting.consensus_score * 100).toFixed(0)}%`}
            subtext="Cross-Agent Agreement"
          />

          <MetricCard
            label="Meeting Health"
            value={`${meeting.meeting_health_score}/100`}
            subtext={meeting.meeting_health_label}
          />
        </div>

        <div className="mt-8 rounded-[32px] border border-slate-200 bg-white p-8 shadow-sm">
          <h2 className="text-3xl font-semibold text-slate-900">Executive Summary</h2>

          <p className="mt-5 leading-8 text-slate-700">{meeting.executive_summary}</p>
        </div>

        <div className="mt-8 rounded-[32px] border border-slate-200 bg-white p-8 shadow-sm">
          <h2 className="text-3xl font-semibold text-slate-900">Final Decision</h2>

          <p className="mt-5 leading-8 text-slate-700">{meeting.final_decision}</p>
        </div>

        <div className="mt-8 rounded-[32px] border border-slate-200 bg-white p-8 shadow-sm">
          <h2 className="text-3xl font-semibold text-slate-900">Consensus Explanation</h2>

          <p className="mt-5 leading-8 text-slate-700">{meeting.consensus_reason}</p>
        </div>

        <div className="mt-8 grid gap-8 xl:grid-cols-2">
          <Section title="Priority Actions" items={meeting.priority_actions} />

          <Section title="Consensus Factors" items={meeting.consensus_factors} />
        </div>

        <Section title="Product Risks" items={meeting.risks} />

        <Section title="Engineering Recommendations" items={meeting.engineering_recommendations} />

        <Section title="Finance Recommendations" items={meeting.finance_recommendations} />

        <Section title="Risk Recommendations" items={meeting.risk_recommendations} />

        <div className="mt-8 rounded-[32px] border border-slate-200 bg-white p-8 shadow-sm">
          <h2 className="text-3xl font-semibold text-slate-900">Agent Execution Timeline</h2>

          <p className="mt-2 text-slate-500">
            Runtime contribution of every stage in the analysis pipeline.
          </p>

          <div className="mt-8 space-y-6">
            {Object.entries(meeting.agent_timings).map(([agent, time]: any) => (
              <TimelineCard
                key={agent}
                agent={agent}
                time={Number(time)}
                total={meeting.processing_time_seconds}
              />
            ))}
          </div>
        </div>

        <Section title="Coordinator Notes" items={meeting.coordinator_notes} />
      </div>
    </main>
  );
}
