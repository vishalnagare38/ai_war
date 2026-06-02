"use client";

import { useMemo, useState } from "react";

type AnalyzeResponse = {
  consensus_score: number;
  agent_agreement: string;
  processing_time_seconds: number;
  meeting_title?: string;
  summary: string;
  action_items: string[];
  risks: string[];
  recommendations: string[];
  confidence_score: number;
  agent_used: string;

  engineering_insights: string[];
  engineering_risks: string[];
  engineering_recommendations: string[];

  finance_insights: string[];
  finance_risks: string[];
  finance_recommendations: string[];

  risk_insights: string[];
  risk_level: string;
  risk_recommendations: string[];

  ml_risk_probability: number;
  ml_risk_label: string;
  delay_likelihood: number;

  executive_summary: string;
  final_decision: string;
  priority_actions: string[];
  overall_risk_level: string;
  coordinator_notes: string[];
};

const DEMO_MEETING_TITLE = "Product Review Meeting";

const DEMO_TRANSCRIPT = `We need to finalize the MVP scope this week. The backend integration is blocked by the API delay. We should assign ownership for frontend tasks and follow up on the database schema. Budget is limited, so cost control matters. Testing is behind, and we need to avoid deadline risk.`;

const pipeline = [
  "Transcript Input",
  "Product Agent",
  "Engineering Agent",
  "Finance Agent",
  "Risk Agent",
  "ML Scorer",
  "Coordinator",
];

function Section({
  title,
  items,
}: {
  title: string;
  items?: string[];
}) {
  if (!items || items.length === 0) return null;

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
      <h3 className="mb-4 text-lg font-semibold text-slate-900">{title}</h3>
      <ul className="space-y-2">
        {items.map((item, index) => (
          <li
            key={index}
            className="rounded-2xl bg-slate-50 px-4 py-3 text-sm leading-6 text-slate-700"
          >
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

function MetricCard({
  label,
  value,
  subtext,
}: {
  label: string;
  value: string;
  subtext?: string;
}) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
      <p className="text-sm text-slate-500">{label}</p>
      <p className="mt-2 text-2xl font-bold text-slate-900">{value}</p>
      {subtext ? <p className="mt-2 text-sm text-slate-500">{subtext}</p> : null}
    </div>
  );
}

function Pill({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <span className="rounded-full border border-slate-200 bg-white px-3 py-1 text-xs font-medium text-slate-700 shadow-sm">
      {children}
    </span>
  );
}

export default function Home() {
  const [meetingTitle, setMeetingTitle] = useState(DEMO_MEETING_TITLE);
  const [transcript, setTranscript] = useState(DEMO_TRANSCRIPT);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<AnalyzeResponse | null>(null);

  const apiUrl = useMemo(
    () => process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000",
    []
  );

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setResult(null);

    if (transcript.trim().length < 20) {
      setError("Please enter a longer transcript.");
      return;
    }

    try {
      setLoading(true);

      const response = await fetch(`${apiUrl}/api/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          meeting_title: meetingTitle || null,
          transcript,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || "Failed to analyze transcript.");
      }

      const data: AnalyzeResponse = await response.json();
      setResult(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const loadDemo = () => {
    setMeetingTitle(DEMO_MEETING_TITLE);
    setTranscript(DEMO_TRANSCRIPT);
    setError("");
    setResult(null);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-8 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
          <div className="flex flex-wrap gap-2">
            <Pill>FastAPI Connected</Pill>
            <Pill>LangGraph Workflow</Pill>
            <Pill>5 Agents Active</Pill>
            <Pill>ML Risk Scorer On</Pill>
          </div>

          <div className="mt-6 inline-flex rounded-full bg-blue-100 px-4 py-1 text-sm font-medium text-blue-700">
            Multi-Agent GenAI System
          </div>

          <h1 className="mt-4 text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
            Meeting War Room
          </h1>

          <p className="mt-3 max-w-3xl text-base leading-7 text-slate-600 sm:text-lg">
            Paste a meeting transcript and get product, engineering, finance,
            risk, and coordinator insights with predictive risk scoring.
          </p>

          <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {pipeline.map((item, index) => (
              <div
                key={item}
                className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm font-medium text-slate-700"
              >
                <span className="mr-2 text-slate-400">{index + 1}.</span>
                {item}
              </div>
            ))}
          </div>
        </div>

        <div className="grid gap-8 lg:grid-cols-2">
          <form
            onSubmit={handleAnalyze}
            className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-2xl font-semibold text-slate-900">
                  Analyze Transcript
                </h2>
                <p className="mt-1 text-sm text-slate-500">
                  Run the full multi-agent workflow on a meeting transcript.
                </p>
              </div>
              <button
                type="button"
                onClick={loadDemo}
                className="rounded-2xl border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
              >
                Load Demo
              </button>
            </div>

            <div className="mt-6 space-y-4">
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">
                  Meeting Title
                </label>
                <input
                  value={meetingTitle}
                  onChange={(e) => setMeetingTitle(e.target.value)}
                  placeholder="Product Review Meeting"
                  className="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none transition focus:border-blue-500"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">
                  Transcript
                </label>
                <textarea
                  value={transcript}
                  onChange={(e) => setTranscript(e.target.value)}
                  placeholder="Paste the meeting transcript here..."
                  rows={12}
                  className="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none transition focus:border-blue-500"
                />
              </div>

              {error ? (
                <div className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                  {error}
                </div>
              ) : null}

              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-2xl bg-blue-600 px-5 py-3 font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? "Analyzing..." : "Run Multi-Agent Analysis"}
              </button>
            </div>
          </form>

          <div className="space-y-6">
            {!result ? (
              <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-2xl font-semibold text-slate-900">
                  Results
                </h2>
                <p className="mt-2 text-sm text-slate-500">
                  Your analysis will appear here after submission.
                </p>

                <div className="mt-6 grid gap-4 sm:grid-cols-2">
                  <MetricCard
                    label="Overall Risk"
                    value="—"
                    subtext="Coordinator final assessment"
                  />
                  <MetricCard
                    label="ML Risk Probability"
                    value="—"
                    subtext="Predictive analytics score"
                  />
                  <MetricCard
                    label="Risk Label"
                    value="—"
                    subtext="Model prediction"
                  />
                  <MetricCard
                    label="Confidence"
                    value="—"
                    subtext="Product agent confidence"
                  />
                </div>
              </div>
            ) : (
              <>
                <div className="grid gap-4 sm:grid-cols-2">
                  <MetricCard
                    label="Overall Risk"
                    value={result.overall_risk_level.toUpperCase()}
                    />

                    <MetricCard
                    label="ML Risk"
                    value={`${(result.ml_risk_probability * 100).toFixed(0)}%`}
                    />

                    <MetricCard
                    label="Risk Label"
                    value={result.ml_risk_label.toUpperCase()}
                    />

                    <MetricCard
                    label="Consensus"
                    value={`${(result.consensus_score * 100).toFixed(0)}%`}
                    />

                    <MetricCard
                    label="Agreement"
                    value={result.agent_agreement.toUpperCase()}
                    />

                    <MetricCard
                    label="Processing Time"
                    value={`${result.processing_time_seconds}s`}
                    />
                </div>

                <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
                  <h2 className="text-2xl font-semibold text-slate-900">
                    Executive Summary
                  </h2>
                  <p className="mt-3 leading-7 text-slate-700">
                    {result.executive_summary}
                  </p>
                </div>

                <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
                  <h2 className="text-2xl font-semibold text-slate-900">
                    Final Decision
                  </h2>
                  <p className="mt-3 text-slate-700">{result.final_decision}</p>
                </div>

                <Section title="Priority Actions" items={result.priority_actions} />
                <Section title="Product Risks" items={result.risks} />
                <Section title="Product Recommendations" items={result.recommendations} />
                <Section title="Engineering Insights" items={result.engineering_insights} />
                <Section title="Engineering Risks" items={result.engineering_risks} />
                <Section
                  title="Engineering Recommendations"
                  items={result.engineering_recommendations}
                />
                <Section title="Finance Insights" items={result.finance_insights} />
                <Section title="Finance Risks" items={result.finance_risks} />
                <Section
                  title="Finance Recommendations"
                  items={result.finance_recommendations}
                />
                <Section title="Risk Insights" items={result.risk_insights} />
                <Section title="Risk Recommendations" items={result.risk_recommendations} />

                <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
                  <h2 className="text-2xl font-semibold text-slate-900">
                    Coordinator Notes
                  </h2>
                  <ul className="mt-4 space-y-2">
                    {result.coordinator_notes.map((note, index) => (
                      <li
                        key={index}
                        className="rounded-2xl bg-slate-50 px-4 py-3 text-sm leading-6 text-slate-700"
                      >
                        {note}
                      </li>
                    ))}
                  </ul>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}