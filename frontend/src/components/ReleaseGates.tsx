import React, { useState } from 'react';
import { ShieldAlert, CheckCircle2, XCircle, AlertTriangle, Copy, Download, Check, FileText } from 'lucide-react';
import { VariantScorecard, ReleaseGatePolicy } from '../types';
import { evaluateReleaseGates } from '../utils/evalEngine';

interface ReleaseGatesProps {
  candidateCard: VariantScorecard | null;
  baselineCard: VariantScorecard | null;
}

export const ReleaseGates: React.FC<ReleaseGatesProps> = ({ candidateCard, baselineCard }) => {
  const [minToolAcc, setMinToolAcc] = useState(0.90);
  const [minPassRate, setMinPassRate] = useState(0.85);
  const [maxLatDelta, setMaxLatDelta] = useState(20.0);
  const [maxCostDelta, setMaxCostDelta] = useState(25.0);
  const [copied, setCopied] = useState(false);

  if (!candidateCard) {
    return (
      <div className="max-w-4xl mx-auto p-12 text-center bg-slate-900 border border-slate-800 rounded-xl space-y-3">
        <ShieldAlert className="w-10 h-10 text-slate-500 mx-auto" />
        <h3 className="text-base font-semibold text-white">No Evaluation Data Loaded</h3>
        <p className="text-xs text-slate-400">
          Please run an evaluation benchmark in Tab 3 (Eval Runner) to evaluate policy gates.
        </p>
      </div>
    );
  }

  const policy: ReleaseGatePolicy = {
    min_pass_rate: minPassRate,
    min_tool_accuracy: minToolAcc,
    min_argument_score: 0.85,
    min_trajectory_score: 0.80,
    max_latency_regression_pct: maxLatDelta,
    max_cost_regression_pct: maxCostDelta,
    zero_tolerance_tools: ['transfer_funds', 'freeze_debit_card', 'dispute_charge'],
  };

  const brief = evaluateReleaseGates(candidateCard, baselineCard || undefined, policy);

  const handleCopy = () => {
    navigator.clipboard.writeText(brief.markdown_content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([brief.markdown_content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `release_decision_brief_${candidateCard.variant_name}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <div className="flex items-center space-x-2 text-sky-400 font-semibold text-xs tracking-wider uppercase mb-1">
          <ShieldAlert className="w-3.5 h-3.5" />
          <span>Release Readiness</span>
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Release Policy Gates & Brief</h1>
        <p className="text-sm text-slate-400 mt-1">
          Bridge the gap from metric soup to product decision. Configure policy thresholds and generate an auditable release brief.
        </p>
      </div>

      {/* Policy Gate Sliders */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
          Configure Release Gate Policies
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
          <div>
            <div className="flex justify-between text-slate-300 mb-1">
              <span>Min Tool Accuracy</span>
              <span className="font-mono text-sky-400">{(minToolAcc * 100).toFixed(0)}%</span>
            </div>
            <input
              type="range"
              min="0.70"
              max="1.0"
              step="0.05"
              value={minToolAcc}
              onChange={(e) => setMinToolAcc(parseFloat(e.target.value))}
              className="w-full accent-sky-500"
            />
          </div>

          <div>
            <div className="flex justify-between text-slate-300 mb-1">
              <span>Min Pass Rate</span>
              <span className="font-mono text-sky-400">{(minPassRate * 100).toFixed(0)}%</span>
            </div>
            <input
              type="range"
              min="0.60"
              max="1.0"
              step="0.05"
              value={minPassRate}
              onChange={(e) => setMinPassRate(parseFloat(e.target.value))}
              className="w-full accent-sky-500"
            />
          </div>

          <div>
            <div className="flex justify-between text-slate-300 mb-1">
              <span>Max Latency Regression</span>
              <span className="font-mono text-sky-400">+{maxLatDelta.toFixed(0)}%</span>
            </div>
            <input
              type="range"
              min="5"
              max="50"
              step="5"
              value={maxLatDelta}
              onChange={(e) => setMaxLatDelta(parseFloat(e.target.value))}
              className="w-full accent-sky-500"
            />
          </div>

          <div>
            <div className="flex justify-between text-slate-300 mb-1">
              <span>Max Cost Regression</span>
              <span className="font-mono text-sky-400">+{maxCostDelta.toFixed(0)}%</span>
            </div>
            <input
              type="range"
              min="10"
              max="100"
              step="5"
              value={maxCostDelta}
              onChange={(e) => setMaxCostDelta(parseFloat(e.target.value))}
              className="w-full accent-sky-500"
            />
          </div>
        </div>
      </div>

      {/* Decision Status Banner */}
      <div
        className={`p-5 rounded-xl border flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
          brief.status === 'READY_TO_SHIP'
            ? 'bg-emerald-950/40 border-emerald-500/30'
            : brief.status === 'BLOCKED'
            ? 'bg-rose-950/40 border-rose-500/30'
            : 'bg-amber-950/40 border-amber-500/30'
        }`}
      >
        <div className="flex items-center space-x-3.5">
          <div
            className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 ${
              brief.status === 'READY_TO_SHIP'
                ? 'bg-emerald-500/20 text-emerald-400'
                : brief.status === 'BLOCKED'
                ? 'bg-rose-500/20 text-rose-400'
                : 'bg-amber-500/20 text-amber-400'
            }`}
          >
            {brief.status === 'READY_TO_SHIP' ? (
              <CheckCircle2 className="w-6 h-6" />
            ) : brief.status === 'BLOCKED' ? (
              <XCircle className="w-6 h-6" />
            ) : (
              <AlertTriangle className="w-6 h-6" />
            )}
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-base font-bold text-white">
                {brief.status === 'READY_TO_SHIP'
                  ? 'READY TO SHIP'
                  : brief.status === 'BLOCKED'
                  ? 'RELEASE BLOCKED'
                  : 'REQUIRES PM REVIEW'}
              </span>
              <span className="text-xs px-2 py-0.5 rounded bg-slate-900 font-mono text-slate-300">
                {brief.passed_gates} / {brief.total_gates} Gates Passed
              </span>
            </div>
            <p className="text-xs text-slate-300 mt-0.5">
              {brief.status === 'READY_TO_SHIP'
                ? 'All quality, latency, and zero-tolerance tool safety criteria verified.'
                : brief.hard_blockers.length > 0
                ? `Critical: ${brief.hard_blockers.join(' • ')}`
                : 'One or more policy thresholds violated. Review deltas below.'}
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2 shrink-0">
          <button
            onClick={handleCopy}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy Brief'}</span>
          </button>
          <button
            onClick={handleDownload}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-sky-500 hover:bg-sky-400 text-white transition shadow-sm"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download .md</span>
          </button>
        </div>
      </div>

      {/* Evaluated Gates Breakdown */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-slate-800">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
            Policy Gate Evaluation Breakdown
          </h3>
        </div>
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
            <tr>
              <th className="py-2.5 px-4 font-medium">Gate Name</th>
              <th className="py-2.5 px-4 font-medium">Status</th>
              <th className="py-2.5 px-4 font-medium">Required Threshold</th>
              <th className="py-2.5 px-4 font-medium">Actual Result</th>
              <th className="py-2.5 px-4 font-medium">Policy Note</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 font-mono text-xs">
            {brief.gates_evaluated.map((g) => (
              <tr key={g.gate_name} className="hover:bg-slate-800/30">
                <td className="py-2.5 px-4 text-slate-200 font-sans font-medium">{g.gate_name}</td>
                <td className="py-2.5 px-4">
                  {g.passed ? (
                    <span className="text-emerald-400 font-semibold flex items-center space-x-1">
                      <CheckCircle2 className="w-3 h-3" />
                      <span>PASS</span>
                    </span>
                  ) : g.is_hard_blocker ? (
                    <span className="text-rose-400 font-semibold bg-rose-500/10 px-1.5 py-0.5 rounded border border-rose-500/20">
                      BLOCKED
                    </span>
                  ) : (
                    <span className="text-amber-400 font-semibold flex items-center space-x-1">
                      <XCircle className="w-3 h-3" />
                      <span>FAIL</span>
                    </span>
                  )}
                </td>
                <td className="py-2.5 px-4 text-slate-400">{g.threshold}</td>
                <td className="py-2.5 px-4 text-white font-semibold">{g.actual_value}</td>
                <td className="py-2.5 px-4 text-slate-300 font-sans text-xs">{g.message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Generated Markdown Preview */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
        <div className="flex items-center space-x-2 text-slate-300 font-medium text-xs">
          <FileText className="w-4 h-4 text-sky-400" />
          <span>Release Decision Brief (Markdown Preview)</span>
        </div>
        <pre className="p-4 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-300 font-mono overflow-x-auto whitespace-pre-wrap leading-relaxed">
          {brief.markdown_content}
        </pre>
      </div>
    </div>
  );
};

