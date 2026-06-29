"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

function Section({
  title,
  items,
}: {
  title: string;
  items?: string[];
}) {

  if (!items?.length) return null;

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">

      <h2 className="mb-5 text-2xl font-bold text-slate-900">
        {title}
      </h2>

      <div className="space-y-3">

        {items.map((item, index) => (

          <div
            key={index}
            className="rounded-xl border border-slate-100 bg-slate-50 p-4 text-slate-700"
          >
            {item}
          </div>

        ))}

      </div>

    </div>
  );
}

function MetricCard({
  title,
  value,
}: {
  title: string;
  value: string;
}) {

  let color = "text-slate-900";

  if (value.toLowerCase().includes("high"))
    color = "text-red-600";

  else if (value.toLowerCase().includes("medium"))
    color = "text-yellow-600";

  else if (value.toLowerCase().includes("low"))
    color = "text-green-600";

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">

      <p className="text-sm font-medium text-slate-500">
        {title}
      </p>

      <p className={`mt-3 text-3xl font-bold ${color}`}>
        {value}
      </p>

    </div>
  );
}

export default function MeetingDetails() {

  const { id } = useParams();

  const router = useRouter();

  const [meeting, setMeeting] = useState<any>(null);

  const [loading, setLoading] = useState(true);

  const api =
    process.env.NEXT_PUBLIC_API_URL ||
    "http://127.0.0.1:8000";

  useEffect(() => {
    loadMeeting();
  }, []);

  async function loadMeeting() {

    const res = await fetch(`${api}/api/meetings/${id}`);

    if (!res.ok) {
      setLoading(false);
      return;
    }

    const data = await res.json();

    setMeeting(data);

    setLoading(false);
  }

  if (loading) {
    return (
      <div className="p-10 text-center">
        Loading...
      </div>
    );
  }

  if (!meeting) {
    return (
      <div className="p-10 text-center">
        Meeting not found.
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-slate-100 text-slate-900">

      <div className="mx-auto max-w-7xl p-10">

        <button
          onClick={() => router.back()}
          className="mb-8 rounded-xl bg-slate-800 px-4 py-2 text-white"
        >
          ← Back
        </button>

        <div className="rounded-3xl bg-white p-8 shadow-sm">

          <h1 className="text-4xl font-bold text-slate-900">
            {meeting.meeting_title}
          </h1>

          <p className="mt-2 text-slate-500">
            {new Date(meeting.created_at).toLocaleString()}
          </p>

        </div>

        <div className="mt-8 grid gap-4 md:grid-cols-4">

          <MetricCard
            title="Overall Risk"
            value={meeting.overall_risk_level.toUpperCase()}
          />

          <MetricCard
            title="ML Risk"
            value={`${(
              meeting.ml_risk_probability * 100
            ).toFixed(0)}%`}
          />

          <MetricCard
            title="Consensus"
            value={`${(
              meeting.consensus_score * 100
            ).toFixed(0)}%`}
          />

          <MetricCard
            title="Meeting Health"
            value={`${meeting.meeting_health_score}/100`}
          />

        </div>

        <div className="mt-8 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">

            <h2 className="text-2xl font-bold text-slate-900">
                Executive Summary
            </h2>

            <p className="mt-4 leading-8 text-slate-700">
                {meeting.executive_summary}
            </p>

        </div>

        <div className="mt-8 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">

            <h2 className="text-2xl font-bold text-slate-900">
                Final Decision
            </h2>

            <p className="mt-4 leading-8 text-slate-700">
                {meeting.final_decision}
            </p>

        </div>

        <div className="mt-8">

          <Section
            title="Priority Actions"
            items={meeting.priority_actions}
          />

        </div>

        <div className="mt-8">

          <Section
            title="Product Risks"
            items={meeting.risks}
          />

        </div>

        <div className="mt-8">

          <Section
            title="Engineering Recommendations"
            items={meeting.engineering_recommendations}
          />

        </div>

        <div className="mt-8">

          <Section
            title="Finance Recommendations"
            items={meeting.finance_recommendations}
          />

        </div>

        <div className="mt-8">

          <Section
            title="Risk Recommendations"
            items={meeting.risk_recommendations}
          />

        </div>

        <div className="mt-8">

          <Section
            title="Coordinator Notes"
            items={meeting.coordinator_notes}
          />

        </div>

      </div>

    </main>
  );
}