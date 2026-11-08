import React, { useState } from 'react';
import { ShieldCheck, AlertTriangle, XCircle, Info, Check, RefreshCw, FileCode2 } from 'lucide-react';
import { EvalPack } from '../types';
import { lintEvalPack, LintReport } from '../utils/linter';
import { exportToPromptfooYaml } from '../utils/promptfooExporter';

interface EvalLinterProps {
  activePack: EvalPack;
  onUpdatePack?: (pack: EvalPack) => void;
}

export const EvalLinter: React.FC<EvalLinterProps> = ({ activePack }) => {
  const [report, setReport] = useState<LintReport>(lintEvalPack(activePack));
  const [promptfooYaml, setPromptfooYaml] = useState<string>(exportToPromptfooYaml(activePack));
  const [activeSubTab, setActiveSubTab] = useState<'linter' | 'promptfoo'>('linter');
  const [copied, setCopied] = useState(false);

  const handleReLint = () => {
    const newReport = lintEvalPack(activePack);
    setReport(newReport);
    setPromptfooYaml(exportToPromptfooYaml(activePack));
  };

  const handleCopyYaml = () => {
    navigator.clipboard.writeText(promptfooYaml);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadYaml = () => {
    const blob = new Blob([promptfooYaml], { type: 'text/yaml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `promptfooconfig_${activePack.id}.yaml`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <div className="flex items-center space-x-2 text-sky-400 font-semibold text-xs tracking-wider uppercase mb-1">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Test Suite Assurance</span>
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Eval Quality Linter & Runner Exporter</h1>
        <p className="text-sm text-slate-400 mt-1">
          Never run defective evaluations. Detect missing negative cases, ambiguous schemas, and holdout leaks, then export directly to <strong>Promptfoo</strong> or <strong>DeepEval</strong>.
        </p>
      </div>

      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setActiveSubTab('linter')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
              activeSubTab === 'linter'
                ? 'bg-sky-500 text-white'
                : 'text-slate-400 hover:text-slate-200 bg-slate-900 border border-slate-800'
            }`}
          >
            🛡️ Quality Linter Report
          </button>
          <button
            onClick={() => setActiveSubTab('promptfoo')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
              activeSubTab === 'promptfoo'
                ? 'bg-sky-500 text-white'
                : 'text-slate-400 hover:text-slate-200 bg-slate-900 border border-slate-800'
            }`}
          >
            🚀 Export to Promptfoo YAML
          </button>
        </div>

        <button
          onClick={handleReLint}
          className="flex items-center space-x-1.5 text-xs text-slate-400 hover:text-slate-200"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Re-analyze Pack</span>
        </button>
      </div>

      {activeSubTab === 'linter' && (
        <div className="space-y-6">
          {/* Linter Score Banner */}
          <div
            className={`p-6 rounded-xl border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 ${
              report.passed
                ? 'bg-emerald-950/30 border-emerald-500/30'
                : 'bg-amber-950/30 border-amber-500/30'
            }`}
          >
            <div className="flex items-center space-x-4">
              <div
                className={`w-14 h-14 rounded-xl flex items-center justify-center font-mono font-bold text-2xl shrink-0 ${
                  report.grade === 'A'
                    ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                    : report.grade === 'B'
                    ? 'bg-sky-500/20 text-sky-400 border border-sky-500/30'
                    : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                }`}
              >
                {report.grade}
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <span className="text-lg font-bold text-white">Quality Score: {report.score} / 100</span>
                  <span
                    className={`text-xs px-2 py-0.5 rounded font-semibold ${
                      report.passed ? 'bg-emerald-500/20 text-emerald-300' : 'bg-amber-500/20 text-amber-300'
                    }`}
                  >
                    {report.passed ? 'PASSED QUALITY GATE' : 'DEFECTS DETECTED'}
                  </span>
                </div>
                <p className="text-xs text-slate-300 mt-1">
                  Active Pack: <strong>{activePack.name}</strong> ({activePack.cases.length} cases analyzed across 6 design rules)
                </p>
              </div>
            </div>

            <div className="text-right sm:border-l sm:border-slate-800 sm:pl-6 text-xs text-slate-400">
              <div>Negative Cases: <span className="font-mono text-white">{activePack.cases.filter(c => c.expected_trajectory.length === 0).length}</span></div>
              <div>High-Risk Tools: <span className="font-mono text-white">{activePack.recommended_gates?.zero_tolerance_tools?.length || 0}</span></div>
            </div>
          </div>

          {/* Issues List */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
            <div className="p-4 border-b border-slate-800">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
                Linter Findings & Diagnostic Checks ({report.issues.length} flagged)
              </h3>
            </div>

            {report.issues.length === 0 ? (
              <div className="p-8 text-center text-slate-400 text-xs">
                <Check className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
                <p className="font-medium text-white">Zero Defects Found!</p>
                <p className="text-[11px] text-slate-500 mt-0.5">This Eval Pack follows industry best practices for negative test coverage, holdout splits, and security constraints.</p>
              </div>
            ) : (
              <div className="divide-y divide-slate-800/60">
                {report.issues.map((issue) => (
                  <div key={issue.rule_id} className="p-4 flex items-start space-x-3 text-xs">
                    {issue.severity === 'error' ? (
                      <XCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                    ) : issue.severity === 'warning' ? (
                      <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                    ) : (
                      <Info className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
                    )}
                    <div className="space-y-1 flex-1">
                      <div className="flex items-center space-x-2">
                        <span className="font-semibold text-white">{issue.rule_id}</span>
                        <span
                          className={`text-[10px] uppercase font-bold px-1.5 py-0.2 rounded ${
                            issue.severity === 'error'
                              ? 'bg-rose-500/20 text-rose-300'
                              : issue.severity === 'warning'
                              ? 'bg-amber-500/20 text-amber-300'
                              : 'bg-sky-500/20 text-sky-300'
                          }`}
                        >
                          {issue.severity}
                        </span>
                      </div>
                      <p className="text-slate-300">{issue.message}</p>
                      <div className="p-2 rounded bg-slate-950 border border-slate-800 text-[11px] text-slate-400">
                        <span className="text-sky-400 font-medium">How to fix: </span>
                        {issue.suggestion}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {activeSubTab === 'promptfoo' && (
        <div className="space-y-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h3 className="text-sm font-semibold text-white flex items-center space-x-2">
                  <FileCode2 className="w-4 h-4 text-sky-400" />
                  <span>promptfooconfig.yaml</span>
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Production-ready YAML. Run with: <code className="text-sky-300 bg-slate-950 px-1.5 py-0.5 rounded">npx promptfoo eval</code>
                </p>
              </div>

              <div className="flex items-center space-x-2">
                <button
                  onClick={handleCopyYaml}
                  className="px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
                >
                  {copied ? 'Copied' : 'Copy YAML'}
                </button>
                <button
                  onClick={handleDownloadYaml}
                  className="px-3 py-1.5 rounded-lg text-xs font-medium bg-sky-500 hover:bg-sky-400 text-white transition shadow-sm"
                >
                  Download promptfooconfig.yaml
                </button>
              </div>
            </div>

            <pre className="p-4 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-300 font-mono overflow-x-auto max-h-[500px] leading-relaxed">
              {promptfooYaml}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};
