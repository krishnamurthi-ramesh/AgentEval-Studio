import React from 'react';
import { Sparkles, Library, PlayCircle, ShieldAlert, Share2 } from 'lucide-react';

interface SidebarProps {
  currentTab: string;
  onSelectTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentTab, onSelectTab }) => {
  const navItems = [
    { id: 'copilot', label: 'Eval Copilot', icon: Sparkles, badge: 'New', desc: 'AI-assisted generation' },
    { id: 'library', label: 'Community Library', icon: Library, desc: 'Reusable Eval Packs' },
    { id: 'runner', label: 'Eval Runner & Diffs', icon: PlayCircle, desc: 'Multi-variant benchmarks' },
    { id: 'gates', label: 'Release Gates & Brief', icon: ShieldAlert, desc: 'Ship / Hold policy engine' },
    { id: 'share', label: 'Share with Community', icon: Share2, desc: 'Export & contribute' },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900/40 p-4 flex flex-col justify-between shrink-0">
      <div className="space-y-6">
        <div>
          <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider px-3">
            Workbench Modules
          </span>
          <nav className="mt-2 space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => onSelectTab(item.id)}
                  className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-left transition ${
                    isActive
                      ? 'bg-sky-500/10 text-sky-400 font-medium border border-sky-500/20'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-sky-400' : 'text-slate-400'}`} />
                    <div>
                      <div className="text-xs">{item.label}</div>
                      <div className="text-[10px] text-slate-500">{item.desc}</div>
                    </div>
                  </div>
                  {item.badge && (
                    <span className="px-1.5 py-0.5 rounded text-[9px] font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        <div className="p-3.5 rounded-xl bg-gradient-to-b from-slate-800/80 to-slate-900/80 border border-slate-800 text-xs">
          <div className="flex items-center space-x-2 text-sky-400 font-semibold mb-1">
            <Sparkles className="w-3.5 h-3.5" />
            <span>ChatPRD for Evals</span>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Generate benchmark packs in seconds, run offline with zero token spend, and export auditable release briefs.
          </p>
        </div>
      </div>

      <div className="pt-4 border-t border-slate-800 text-[11px] text-slate-500 flex items-center justify-between px-2">
        <span>v0.1.0 • Apache-2.0</span>
        <span className="flex items-center space-x-1 text-emerald-400">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Ready</span>
        </span>
      </div>
    </aside>
  );
};
