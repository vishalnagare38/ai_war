'use client';

import { useMemo, useState } from 'react';

import MetricCard from '@/components/MetricCard';
import Section from '@/components/Section';
import TrendBadge from '@/components/TrendBadge';
import Pill from '@/components/Pill';
import PageHeader from '@/components/PageHeader';

type AnalyzeResponse = {
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

  consensus_score: number;
  agent_agreement: string;
  consensus_factors: string[];

  meeting_health_score: number;
  meeting_health_label: string;

  history_summary: string;
  recurring_blockers: string[];

  risk_trend: string;
  health_trend: string;
  project_momentum: string;

  processing_time_seconds: number;

  agent_timings: Record<string, number>;

  consensus_reason: string;

  executive_summary: string;

  final_decision: string;

  priority_actions: string[];

  overall_risk_level: string;

  coordinator_notes: string[];
};

const DEMO_MEETING_TITLE = 'Product Review Meeting';

const DEMO_TRANSCRIPT = `We need to finalize the MVP scope this week. The backend integration is blocked by the API delay. We should assign ownership for frontend tasks and follow up on the database schema. Budget is limited, so cost control matters. Testing is behind, and we need to avoid deadline risk.`;

const pipeline = [
  {
    id: '01',
    title: 'Transcript',
    desc: 'Input',
  },
  {
    id: '02',
    title: 'Product',
    desc: 'Agent',
  },
  {
    id: '03',
    title: 'Engineering',
    desc: 'Agent',
  },
  {
    id: '04',
    title: 'Finance',
    desc: 'Agent',
  },
  {
    id: '05',
    title: 'Risk',
    desc: 'Agent',
  },
  {
    id: '06',
    title: 'ML',
    desc: 'Scorer',
  },
  {
    id: '07',
    title: 'Consensus',
    desc: 'Engine',
  },
  {
    id: '08',
    title: 'Coordinator',
    desc: 'Agent',
  },
];

function PipelineCard({ id, title, desc }: { id: string; title: string; desc: string }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5 transition-all duration-300 hover:border-blue-200 hover:bg-white">
      <div className="text-xs font-semibold tracking-wider text-blue-600">{id}</div>

      <h3 className="mt-4 text-lg font-semibold text-slate-900">{title}</h3>

      <p className="mt-1 text-sm text-slate-500">{desc}</p>
    </div>
  );
}

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

export default function Home() {
  const [meetingTitle, setMeetingTitle] = useState(DEMO_MEETING_TITLE);

  const [transcript, setTranscript] = useState(DEMO_TRANSCRIPT);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const [loading, setLoading] = useState(false);

  const [pdfLoading, setPdfLoading] = useState(false);

  const [error, setError] = useState('');

  const [result, setResult] = useState<AnalyzeResponse | null>(null);

  const apiUrl = useMemo(() => process.env.NEXT_PUBLIC_API_URL ?? 'http://127.0.0.1:8000', []);

  function loadDemo() {
    setMeetingTitle(DEMO_MEETING_TITLE);

    setTranscript(DEMO_TRANSCRIPT);

    setSelectedFile(null);

    setResult(null);

    setError('');
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0] ?? null;

    setSelectedFile(file);

    setError('');
  }

  async function handleAnalyze(e: React.FormEvent) {
    e.preventDefault();

    setLoading(true);

    setError('');

    setResult(null);

    const hasTranscript = transcript.trim().length >= 20;

    const hasFile = selectedFile !== null;

    if (!hasTranscript && !hasFile) {
      setLoading(false);

      setError('Please paste a transcript or upload a PDF/TXT file.');

      return;
    }

    try {
      let response: Response;

      if (hasFile) {
        const formData = new FormData();

        formData.append('meeting_title', meetingTitle);

        formData.append('file', selectedFile as File);

        response = await fetch(`${apiUrl}/api/analyze-upload`, {
          method: 'POST',
          body: formData,
        });
      } else {
        response = await fetch(`${apiUrl}/api/analyze`, {
          method: 'POST',

          headers: {
            'Content-Type': 'application/json',
          },

          body: JSON.stringify({
            meeting_title: meetingTitle,

            transcript,
          }),
        });
      }

      if (!response.ok) {
        const data = await response.json();

        throw new Error(data.detail ?? 'Analysis failed.');
      }

      const data: AnalyzeResponse = await response.json();

      setResult(data);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Unexpected error.');
      }
    } finally {
      setLoading(false);
    }
  }

  async function downloadPdf() {
    if (!result) return;

    try {
      setPdfLoading(true);

      const response = await fetch(
        `${apiUrl}/api/report/pdf`,

        {
          method: 'POST',

          headers: {
            'Content-Type': 'application/json',
          },

          body: JSON.stringify(result),
        }
      );

      if (!response.ok) {
        throw new Error('PDF generation failed.');
      }

      const blob = await response.blob();

      const url = URL.createObjectURL(blob);

      const a = document.createElement('a');

      a.href = url;

      a.download = `${meetingTitle.replace(/\s+/g, '_')}.pdf`;

      document.body.appendChild(a);

      a.click();

      a.remove();

      URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);

      setError('Unable to download PDF.');
    } finally {
      setPdfLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <PageHeader
          badge="Enterprise AI Platform"
          title="Meeting War Room"
          description="Analyze meeting transcripts using Product, Engineering, Finance, Risk, Consensus, Historical Intelligence and Machine Learning to generate executive-ready reports."
        >
          <div className="flex flex-wrap gap-2">
            <Pill>FastAPI</Pill>

            <Pill>LangGraph</Pill>

            <Pill>Gemini</Pill>

            <Pill>MongoDB</Pill>

            <Pill>Machine Learning</Pill>

            <Pill>Historical Intelligence</Pill>
          </div>

          <div className="mt-8 grid gap-4 md:grid-cols-4 xl:grid-cols-8">
            {pipeline.map((step) => (
              <PipelineCard key={step.id} id={step.id} title={step.title} desc={step.desc} />
            ))}
          </div>
        </PageHeader>

        <div className="mt-10 grid gap-8 xl:grid-cols-[460px_1fr]">
          <form
            onSubmit={handleAnalyze}
            className="sticky top-28 h-fit rounded-[32px] border border-slate-200 bg-white p-8 shadow-sm"
          >
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-2xl font-semibold text-slate-900">Analyze Meeting</h2>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                  Upload a PDF/TXT meeting transcript or paste raw text for complete multi-agent
                  analysis.
                </p>
              </div>

              <button
                type="button"
                onClick={loadDemo}
                className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
              >
                Load Demo
              </button>
            </div>

            <div className="mt-8 space-y-6">
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">
                  Meeting Title
                </label>

                <input
                  value={meetingTitle}
                  onChange={(e) => setMeetingTitle(e.target.value)}
                  placeholder="Product Review Meeting"
                  className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 outline-none transition focus:border-blue-600"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">Upload File</label>

                <input
                  type="file"
                  accept=".pdf,.txt"
                  onChange={handleFileChange}
                  className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 file:mr-4 file:rounded-xl file:border-0 file:bg-blue-600 file:px-5 file:py-2 file:text-white file:transition hover:file:bg-blue-700"
                />

                {selectedFile && (
                  <div className="mt-3 rounded-2xl border border-blue-200 bg-blue-50 p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-slate-900">Selected File</p>

                        <p className="mt-1 text-sm text-slate-600">{selectedFile.name}</p>
                      </div>

                      <button
                        type="button"
                        onClick={() => setSelectedFile(null)}
                        className="text-sm font-medium text-blue-700 hover:underline"
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                )}
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">
                  Or Paste Transcript
                </label>

                <textarea
                  rows={16}
                  value={transcript}
                  onChange={(e) => setTranscript(e.target.value)}
                  placeholder="Paste meeting transcript..."
                  className="w-full resize-none rounded-2xl border border-slate-200 bg-white px-4 py-4 leading-7 outline-none transition focus:border-blue-600"
                />
              </div>

              {error && (
                <div className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                  {error}
                </div>
              )}

              <button
                disabled={loading}
                className="w-full rounded-2xl bg-blue-600 px-5 py-4 text-base font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? 'Running Multi-Agent Analysis...' : 'Run Analysis'}
              </button>

              <div className="grid grid-cols-2 gap-3">
                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <p className="text-xs uppercase tracking-wider text-slate-500">AI Agents</p>

                  <h3 className="mt-2 text-3xl font-semibold text-slate-900">5</h3>
                </div>

                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <p className="text-xs uppercase tracking-wider text-slate-500">Intelligence</p>

                  <h3 className="mt-2 text-3xl font-semibold text-slate-900">7 Layers</h3>
                </div>
              </div>
            </div>
          </form>

          <div className="space-y-8">
            {!result ? (
              <div className="rounded-[32px] border border-slate-200 bg-white p-10 shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-3xl font-semibold text-slate-900">Analysis Results</h2>

                    <p className="mt-2 text-slate-500">
                      Run an analysis to generate executive insights.
                    </p>
                  </div>
                </div>

                <div className="mt-8 grid gap-5 md:grid-cols-2 xl:grid-cols-4">
                  <MetricCard label="Overall Risk" value="—" subtext="Coordinator Assessment" />

                  <MetricCard label="ML Risk" value="—" subtext="Predictive Analytics" />

                  <MetricCard label="Consensus" value="—" subtext="Cross-Agent Agreement" />

                  <MetricCard label="Meeting Health" value="—" subtext="Overall Project Health" />

                  <MetricCard label="Risk Label" value="—" subtext="ML Classification" />

                  <MetricCard label="Agreement" value="—" subtext="Consensus Strength" />

                  <MetricCard label="Processing Time" value="—" subtext="Pipeline Runtime" />

                  <MetricCard label="Historical Trend" value="—" subtext="Meeting Intelligence" />
                </div>
              </div>
            ) : (
              <>
                <div className="flex items-center justify-end">
                  <button
                    type="button"
                    onClick={downloadPdf}
                    disabled={pdfLoading}
                    className="rounded-2xl bg-slate-900 px-6 py-3 font-medium text-white transition hover:bg-slate-800 disabled:opacity-50"
                  >
                    {pdfLoading ? 'Generating Report...' : 'Download Executive PDF'}
                  </button>
                </div>

                <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
                  <MetricCard
                    label="Overall Risk"
                    value={result.overall_risk_level.toUpperCase()}
                    subtext="Coordinator Final Assessment"
                  />

                  <MetricCard
                    label="ML Risk"
                    value={`${(result.ml_risk_probability * 100).toFixed(1)}%`}
                    subtext="Predictive Analytics"
                  />

                  <MetricCard
                    label="Risk Label"
                    value={result.ml_risk_label.toUpperCase()}
                    subtext="Machine Learning"
                  />

                  <MetricCard
                    label="Consensus"
                    value={`${(result.consensus_score * 100).toFixed(0)}%`}
                    subtext="Cross-Agent Agreement"
                  />

                  <MetricCard
                    label="Agreement"
                    value={result.agent_agreement.toUpperCase()}
                    subtext="Consensus Strength"
                  />

                  <MetricCard
                    label="Meeting Health"
                    value={`${result.meeting_health_score}/100`}
                    subtext={result.meeting_health_label}
                  />

                  <MetricCard
                    label="Processing Time"
                    value={`${result.processing_time_seconds.toFixed(2)}s`}
                    subtext="End-to-End Runtime"
                  />

                  <MetricCard
                    label="Momentum"
                    value={result.project_momentum}
                    subtext="Historical Intelligence"
                  />
                </div>

                <div className="rounded-[32px] border border-slate-200 bg-white p-8 shadow-sm">
                  <h2 className="text-3xl font-semibold text-slate-900">Executive Summary</h2>

                  <p className="mt-5 leading-8 text-slate-700">{result.executive_summary}</p>
                </div>

                <div className="rounded-[32px] border border-slate-200 bg-white p-8 shadow-sm">
                  <h2 className="text-3xl font-semibold text-slate-900">
                    Final Executive Decision
                  </h2>

                  <p className="mt-5 leading-8 text-slate-700">{result.final_decision}</p>
                </div>

                <div className="rounded-[32px] border border-slate-200 bg-white p-8 shadow-sm">
                  <h2 className="text-3xl font-semibold text-slate-900">Project Intelligence</h2>

                  <p className="mt-5 leading-8 text-slate-700">{result.history_summary}</p>

                  <div className="mt-8 grid gap-5 lg:grid-cols-3">
                    <TrendBadge title="Risk Trend" value={result.risk_trend} />

                    <TrendBadge title="Health Trend" value={result.health_trend} />

                    <TrendBadge title="Project Momentum" value={result.project_momentum} />
                  </div>
                </div>

                <div className="grid gap-8 xl:grid-cols-2">
                  <Section title="Priority Actions" items={result.priority_actions} />

                  <Section title="Recurring Blockers" items={result.recurring_blockers} />
                </div>

                <Section title="Consensus Factors" items={result.consensus_factors} />

                <div className="rounded-[32px] border border-slate-200 bg-white p-8 shadow-sm">
                  <h2 className="text-3xl font-semibold text-slate-900">Consensus Explanation</h2>

                  <p className="mt-5 leading-8 text-slate-700">{result.consensus_reason}</p>
                </div>
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

                <Section title="Finance Recommendations" items={result.finance_recommendations} />

                <Section title="Risk Insights" items={result.risk_insights} />

                <Section title="Risk Recommendations" items={result.risk_recommendations} />

                <div className="rounded-[32px] border border-slate-200 bg-white p-8 shadow-sm">
                  <h2 className="text-3xl font-semibold text-slate-900">
                    Agent Execution Timeline
                  </h2>

                  <p className="mt-2 text-slate-500">
                    Runtime contribution of every stage in the multi-agent pipeline.
                  </p>

                  <div className="mt-8 space-y-6">
                    {Object.entries(result.agent_timings).map(([agent, time]) => (
                      <TimelineCard
                        key={agent}
                        agent={agent}
                        time={Number(time)}
                        total={result.processing_time_seconds}
                      />
                    ))}
                  </div>
                </div>

                <Section title="Coordinator Notes" items={result.coordinator_notes} />
              </>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
