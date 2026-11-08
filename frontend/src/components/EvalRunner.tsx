import React, { useState } from 'react';
import { PlayCircle, CheckCircle2, XCircle, AlertTriangle } from 'lucide-react';
import { EvalPack, VariantScorecard } from '../types';
import { simulateAgentRun } from '../utils/evalEngine';

interface EvalRunnerProps {
  pack: EvalPack;
  baselineCard: VariantScorecard | null;
  candidateCard: VariantScorecard | null;
  onSetScorecards: (baseline: VariantScorecard, candidate: VariantScorecard) => void;
  onGoToGates: () => void;
}

export const EvalRunner: React.FC<EvalRunnerProps> = ({
  pack,
  baselineCard,
  candidateCard,
  onSetScorecards,
  onGoToGates,
}) => {
  const [selectedCandidate, setSelectedCandidate] = useState<'v2' | 'v3'>('v2');
  const [isRunning, setIsRunning] = useState(false);
  const [filterMode, setFilterMode] = useState<'all' | 'failing' | 'high_risk'>('all');

  const handleRun = () => {
    setIsRunning(true);
    setTimeout(() => {
      const base = simulateAgentRun(pack, 'v1');
      const cand = simulateAgentRun(pack, selectedCandidate);
      onSetScorecards(base, cand);
      setIsRunning(false);
    }, 400);
  };

  const filteredRows = candidateCard
    ? candidateCard.rows.filter((r) => {
        if (filterMode === 'failing') return !r.passed;
        if (filterMode === 'high_risk') return r.is_high_risk_failure;
        return true;
      })
    : [];

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <div className="flex items-center space-x-2 text-sky-400 font-semibold text-xs tracking-wider uppercase mb-1">
          <PlayCircle className="w-3.5 h-3.5" />
          <span>Multi-Variant Benchmark</span>
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Eval Runner & Comparison</h1>
        <p className="text-sm text-slate-400 mt-1">
          Execute candidate prompts and model configurations against <strong>{pack.name}</strong> to evaluate tool selection, argument accuracy, latency, and cost deltas.
        </p>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
          <div>
            <span className="block text-xs font-medium text-slate-400 mb-1">Baseline Variant</span>
            <div className="px-3.5 py-2 rounded-lg bg-slate-950 border border-slate-800 font-mono text-xs text-slate-200">
              router_prompt_v1 (Baseline)
            </div>
          </div>

          <div>
            <span className="block text-xs font-medium text-slate-400 mb-1">Candidate Variant</span>
            <select
              value={selectedCandidate}
              onChange={(e: any) => setSelectedCandidate(e.target.value)}
              className="w-full px-3.5 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono text-slate-200 focus:outline-none focus:border-sky-500"
            >
              <option value="v2">router_prompt_v2 (With security regression)</option>
              <option value="v3">router_prompt_v3 (Production hardened)</option>
            </select>
          </div>

          <div className="pt-5">
            <button
              onClick={handleRun}
              disabled={isRunning}
              className="w-full py-2.5 px-4 rounded-lg bg-sky-500 hover:bg-sky-400 font-medium text-xs text-white flex items-center justify-center space-x-2 transition shadow-lg shadow-sky-500/20 disabled:opacity-50"
            >
              <PlayCircle className="w-4 h-4" />
              <span>{isRunning ? 'Evaluating Test Rows...' : 'Run Benchmark Comparison'}</span>
            </button>
          </div>
        </div>
      </div>

      {baselineCard && candidateCard && (
        <div className="space-y-6 animate-in fade-in duration-300">
          {/* Top Metric Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider">Overall Pass Rate</span>
              <div className="mt-2 flex items-baseline justify-between">
                <span className="text-2xl font-bold text-white font-mono">
                  {(candidateCard.pass_rate * 100).toFixed(1)}%
                </span>
                <span
                  className={`text-xs font-mono font-medium ${
                    candidateCard.pass_rate >= baselineCard.pass_rate ? 'text-emerald-400' : 'text-rose-400'
                  }`}
                >
                  {candidateCard.pass_rate >= baselineCard.pass_rate ? '+' : ''}
                  {((candidateCard.pass_rate - baselineCard.pass_rate) * 100).toFixed(1)}%
                </span>
              </div>
              <p className="text-[11px] text-slate-500 mt-1">vs Baseline ({(baselineCard.pass_rate * 100).toFixed(1)}%)</p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider">Tool Routing Accuracy</span>
              <div className="mt-2 flex items-baseline justify-between">
                <span className="text-2xl font-bold text-white font-mono">
                  {(candidateCard.avg_tool_accuracy * 100).toFixed(1)}%
                </span>
                <span
                  className={`text-xs font-mono font-medium ${
                    candidateCard.avg_tool_accuracy >= baselineCard.avg_tool_accuracy ? 'text-emerald-400' : 'text-rose-400'
                  }`}
                >
                  {candidateCard.avg_tool_accuracy >= baselineCard.avg_tool_accuracy ? '+' : ''}
                  {((candidateCard.avg_tool_accuracy - baselineCard.avg_tool_accuracy) * 100).toFixed(1)}%
                </span>
              </div>
              <p className="text-[11px] text-slate-500 mt-1">
                Precision & Recall across {candidateCard.total_cases} tests
              </p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider">p50 Response Latency</span>
              <div className="mt-2 flex items-baseline justify-between">
                <span className="text-2xl font-bold text-white font-mono">{candidateCard.p50_latency_ms}ms</span>
                <span
                  className={`text-xs font-mono font-medium ${
                    candidateCard.p50_latency_ms <= baselineCard.p50_latency_ms ? 'text-emerald-400' : 'text-amber-400'
                  }`}
                >
                  {candidateCard.p50_latency_ms > baselineCard.p50_latency_ms ? '+' : ''}
                  {candidateCard.p50_latency_ms - baselineCard.p50_latency_ms}ms
                </span>
              </div>
              <p className="text-[11px] text-slate-500 mt-1">Baseline: {baselineCard.p50_latency_ms}ms</p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider">High-Risk Failures</span>
              <div className="mt-2 flex items-baseline justify-between">
                <span
                  className={`text-2xl font-bold font-mono ${
                    candidateCard.high_risk_failures > 0 ? 'text-rose-400' : 'text-emerald-400'
                  }`}
                >
                  {candidateCard.high_risk_failures}
                </span>
                {candidateCard.high_risk_failures > 0 ? (
                  <span className="text-[10px] uppercase font-bold px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300">
                    Hard Blocker
                  </span>
                ) : (
                  <span className="text-[10px] uppercase font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300">
                    Zero Flaws
                  </span>
                )}
              </div>
              <p className="text-[11px] text-slate-500 mt-1">Financial / Guardrail Errors</p>
            </div>
          </div>

          {/* Comparative Matrix */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
            <div className="p-4 border-b border-slate-800 flex items-center justify-between">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
                Evaluation Scorecard: Baseline vs Candidate
              </h3>
              <button
                onClick={onGoToGates}
                className="text-xs text-sky-400 hover:text-sky-300 font-medium flex items-center space-x-1"
              >
                <span>Check Release Gate Policies</span>
                <span aria-hidden="true">&rarr;</span>
              </button>
            </div>

            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-2.5 px-4 font-medium">Dimension</th>
                  <th className="py-2.5 px-4 font-medium">Baseline (v1)</th>
                  <th className="py-2.5 px-4 font-medium">Candidate ({candidateCard.variant_name})</th>
                  <th className="py-2.5 px-4 font-medium">Delta</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono text-xs">
                <tr>
                  <td className="py-2.5 px-4 text-slate-300 font-sans">Benchmark Pass Rate</td>
                  <td className="py-2.5 px-4 text-slate-400">{(baselineCard.pass_rate * 100).toFixed(1)}%</td>
                  <td className="py-2.5 px-4 text-white font-semibold">{(candidateCard.pass_rate * 100).toFixed(1)}%</td>
                  <td className="py-2.5 px-4 text-emerald-400">
                    {candidateCard.pass_rate >= baselineCard.pass_rate ? '+' : ''}
                    {((candidateCard.pass_rate - baselineCard.pass_rate) * 100).toFixed(1)}%
                  </td>
                </tr>
                <tr>
                  <td className="py-2.5 px-4 text-slate-300 font-sans">Tool Selection Accuracy</td>
                  <td className="py-2.5 px-4 text-slate-400">{(baselineCard.avg_tool_accuracy * 100).toFixed(1)}%</td>
                  <td className="py-2.5 px-4 text-white font-semibold">{(candidateCard.avg_tool_accuracy * 100).toFixed(1)}%</td>
                  <td className="py-2.5 px-4 text-emerald-400">
                    {candidateCard.avg_tool_accuracy >= baselineCard.avg_tool_accuracy ? '+' : ''}
                    {((candidateCard.avg_tool_accuracy - baselineCard.avg_tool_accuracy) * 100).toFixed(1)}%
                  </td>
                </tr>
                <tr>
                  <td className="py-2.5 px-4 text-slate-300 font-sans">Argument Entity Correctness</td>
                  <td className="py-2.5 px-4 text-slate-400">{(baselineCard.avg_argument_score * 100).toFixed(1)}%</td>
                  <td className="py-2.5 px-4 text-white font-semibold">{(candidateCard.avg_argument_score * 100).toFixed(1)}%</td>
                  <td className="py-2.5 px-4 text-emerald-400">
                    {candidateCard.avg_argument_score >= baselineCard.avg_argument_score ? '+' : ''}
                    {((candidateCard.avg_argument_score - baselineCard.avg_argument_score) * 100).toFixed(1)}%
                  </td>
                </tr>
                <tr>
                  <td className="py-2.5 px-4 text-slate-300 font-sans">Trajectory Flow Score</td>
                  <td className="py-2.5 px-4 text-slate-400">{(baselineCard.avg_trajectory_score * 100).toFixed(1)}%</td>
                  <td className="py-2.5 px-4 text-white font-semibold">{(candidateCard.avg_trajectory_score * 100).toFixed(1)}%</td>
                  <td className="py-2.5 px-4 text-emerald-400">
                    {candidateCard.avg_trajectory_score >= baselineCard.avg_trajectory_score ? '+' : ''}
                    {((candidateCard.avg_trajectory_score - baselineCard.avg_trajectory_score) * 100).toFixed(1)}%
                  </td>
                </tr>
                <tr>
                  <td className="py-2.5 px-4 text-slate-300 font-sans">Total Token Cost</td>
                  <td className="py-2.5 px-4 text-slate-400">${baselineCard.total_cost_usd.toFixed(4)}</td>
                  <td className="py-2.5 px-4 text-white font-semibold">${candidateCard.total_cost_usd.toFixed(4)}</td>
                  <td className="py-2.5 px-4 text-amber-400">
                    +{(((candidateCard.total_cost_usd - baselineCard.total_cost_usd) / baselineCard.total_cost_usd) * 100).toFixed(1)}%
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Row Level Inspection */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex flex-col sm:flex-row gap-3 items-start sm:items-center justify-between">
              <div>
                <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
                  Row-Level Failure Diagnostics ({candidateCard.variant_name})
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Inspect exact parameter errors, tool routing drift, and security failures.
                </p>
              </div>

              <div className="flex items-center space-x-1.5">
                <button
                  onClick={() => setFilterMode('all')}
                  className={`px-2.5 py-1 rounded text-xs transition ${
                    filterMode === 'all' ? 'bg-slate-800 text-white font-medium' : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  All ({candidateCard.rows.length})
                </button>
                <button
                  onClick={() => setFilterMode('failing')}
                  className={`px-2.5 py-1 rounded text-xs transition ${
                    filterMode === 'failing' ? 'bg-slate-800 text-rose-400 font-medium' : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  Failing Only ({candidateCard.rows.filter((r) => !r.passed).length})
                </button>
                <button
                  onClick={() => setFilterMode('high_risk')}
                  className={`px-2.5 py-1 rounded text-xs transition ${
                    filterMode === 'high_risk'
                      ? 'bg-rose-500/20 text-rose-300 font-medium border border-rose-500/30'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  High Risk ({candidateCard.rows.filter((r) => r.is_high_risk_failure).length})
                </button>
              </div>
            </div>

            <div className="overflow-x-auto border border-slate-800 rounded-lg">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800 font-mono text-[11px]">
                  <tr>
                    <th className="py-2.5 px-3">Case ID</th>
                    <th className="py-2.5 px-3">Status</th>
                    <th className="py-2.5 px-3">Tool Score</th>
                    <th className="py-2.5 px-3">Arg Score</th>
                    <th className="py-2.5 px-3">Trajectory</th>
                    <th className="py-2.5 px-3">Diagnostic Explanation</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
                  {filteredRows.map((r) => (
                    <tr key={r.case_id} className="hover:bg-slate-800/30">
                      <td className="py-2.5 px-3 text-sky-400">{r.case_id}</td>
                      <td className="py-2.5 px-3">
                        {r.passed ? (
                          <span className="inline-flex items-center space-x-1 text-emerald-400 font-semibold">
                            <CheckCircle2 className="w-3.5 h-3.5" />
                            <span>PASS</span>
                          </span>
                        ) : r.is_high_risk_failure ? (
                          <span className="inline-flex items-center space-x-1 text-rose-400 font-semibold bg-rose-500/10 px-1.5 py-0.5 rounded border border-rose-500/20">
                            <AlertTriangle className="w-3.5 h-3.5" />
                            <span>HIGH RISK</span>
                          </span>
                        ) : (
                          <span className="inline-flex items-center space-x-1 text-amber-400 font-semibold">
                            <XCircle className="w-3.5 h-3.5" />
                            <span>FAIL</span>
                          </span>
                        )}
                      </td>
                      <td className="py-2.5 px-3 text-slate-200">{(r.tool_selection_score * 100).toFixed(0)}%</td>
                      <td className="py-2.5 px-3 text-slate-200">{(r.argument_score * 100).toFixed(0)}%</td>
                      <td className="py-2.5 px-3 text-slate-200">{(r.trajectory_score * 100).toFixed(0)}%</td>
                      <td className="py-2.5 px-3 text-slate-300 font-sans text-xs max-w-md">
                        {r.diagnostic_notes.join(' • ')}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
