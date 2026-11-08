import React, { useState } from 'react';
import { Share2, Download, Copy, Check, GitPullRequest, Code2, Sparkles } from 'lucide-react';
import { EvalPack } from '../types';

interface ShareCommunityProps {
  activePack: EvalPack;
}

export const ShareCommunity: React.FC<ShareCommunityProps> = ({ activePack }) => {
  const [copied, setCopied] = useState(false);

  const packJson = JSON.stringify(activePack, null, 2);

  const handleCopy = () => {
    navigator.clipboard.writeText(packJson);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([packJson], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${activePack.id}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <div className="flex items-center space-x-2 text-sky-400 font-semibold text-xs tracking-wider uppercase mb-1">
          <Share2 className="w-3.5 h-3.5" />
          <span>Open-Source Contribution</span>
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Share with the AI Community</h1>
        <p className="text-sm text-slate-400 mt-1">
          Publish your evaluation pack to the open community. Help other AI builders test tool-calling agents, guardrails, and complex workflows.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-slate-300">
              <Code2 className="w-4 h-4 text-sky-400" />
              <span>Eval Pack Manifest: {activePack.id}.json</span>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={handleCopy}
                className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? 'Copied' : 'Copy JSON'}</span>
              </button>
              <button
                onClick={handleDownload}
                className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-sky-500 hover:bg-sky-400 text-white transition shadow-sm"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download JSON</span>
              </button>
            </div>
          </div>

          <pre className="p-4 rounded-lg bg-slate-950 border border-slate-800 text-xs text-sky-300 font-mono overflow-x-auto max-h-[500px] leading-relaxed">
            {packJson}
          </pre>
        </div>

        <div className="space-y-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-slate-300">
              <GitPullRequest className="w-4 h-4 text-indigo-400" />
              <span>How to Contribute via GitHub</span>
            </div>
            <ol className="space-y-3 text-xs text-slate-300 list-decimal list-inside leading-relaxed">
              <li>
                <span className="font-semibold text-white">Fork the repository:</span>
                <p className="pl-4 text-[11px] text-slate-400 mt-0.5">
                  Visit <a href="https://github.com/krishnamurthi-ramesh/AgentEval-Studio" target="_blank" rel="noopener noreferrer" className="text-sky-400 underline">krishnamurthi-ramesh/AgentEval-Studio</a> and click Fork.
                </p>
              </li>
              <li>
                <span className="font-semibold text-white">Add your pack:</span>
                <p className="pl-4 text-[11px] text-slate-400 mt-0.5 font-mono">
                  agenteval/library/packs/{activePack.id}.json
                </p>
              </li>
              <li>
                <span className="font-semibold text-white">Open a Pull Request:</span>
                <p className="pl-4 text-[11px] text-slate-400 mt-0.5">
                  Submit your PR using the Community Eval Pack template. Automated CI will validate schemas and tests!
                </p>
              </li>
            </ol>
          </div>

          <div className="p-4 rounded-xl bg-gradient-to-br from-indigo-950/40 to-slate-900 border border-indigo-500/20 text-xs text-slate-300 space-y-2">
            <div className="flex items-center space-x-2 text-indigo-400 font-semibold">
              <Sparkles className="w-4 h-4" />
              <span>Community Impact</span>
            </div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              When you publish an evaluation pack, other AI builders can run it locally in 1-click to test their prompts and models against your real-world scenarios and edge cases.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

