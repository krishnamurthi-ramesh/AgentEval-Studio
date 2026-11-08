import React from 'react';
import { Sparkles, Github, ShieldCheck, Box } from 'lucide-react';
import { EvalPack } from '../types';

interface NavbarProps {
  activePack: EvalPack;
}

export const Navbar: React.FC<NavbarProps> = ({ activePack }) => {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50 px-6 flex items-center justify-between">
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2.5">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg tracking-tight text-white">AgentEval</span>
              <span className="text-xs px-2 py-0.5 rounded-full font-semibold bg-sky-500/10 text-sky-400 border border-sky-500/20">Studio</span>
            </div>
            <p className="text-[11px] text-slate-400 -mt-0.5">ChatPRD for AI Evals</p>
          </div>
        </div>

        <div className="hidden md:flex items-center space-x-2 pl-4 border-l border-slate-800 text-xs">
          <span className="text-slate-400">Active Pack:</span>
          <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-slate-800 border border-slate-700 text-slate-200 font-mono text-[11px]">
            <Box className="w-3.5 h-3.5 text-sky-400" />
            <span className="font-medium truncate max-w-[200px]">{activePack.name}</span>
            <span className="text-slate-500">({activePack.cases.length} cases)</span>
          </div>
        </div>
      </div>

      <div className="flex items-center space-x-3">
        <div className="hidden sm:flex items-center space-x-1.5 text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1 rounded-md">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Local Engine: Deterministic</span>
        </div>

        <a
          href="https://github.com/krishnamurthi-ramesh/AgentEval-Studio"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
        >
          <Github className="w-4 h-4" />
          <span>GitHub</span>
          <span className="bg-slate-900 text-slate-400 px-1.5 py-0.5 rounded text-[10px] ml-1">Star</span>
        </a>
      </div>
    </header>
  );
};
