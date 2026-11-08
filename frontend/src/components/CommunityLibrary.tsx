import React, { useState } from 'react';
import { Library, Search, Box, ArrowRight, Tag, Check } from 'lucide-react';
import { EvalPack } from '../types';

interface CommunityLibraryProps {
  packs: EvalPack[];
  activePack: EvalPack;
  onSelectPack: (pack: EvalPack) => void;
  onLoadIntoRunner: (pack: EvalPack) => void;
}

export const CommunityLibrary: React.FC<CommunityLibraryProps> = ({
  packs,
  activePack,
  onSelectPack,
  onLoadIntoRunner,
}) => {
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');

  const categories = ['All', 'Finance', 'Developer Tools', 'Security'];

  const filteredPacks = packs.filter((p) => {
    const matchesSearch =
      p.name.toLowerCase().includes(search.toLowerCase()) ||
      p.description.toLowerCase().includes(search.toLowerCase()) ||
      p.tags.some((t) => t.toLowerCase().includes(search.toLowerCase()));
    const matchesCategory = selectedCategory === 'All' || p.category.toLowerCase() === selectedCategory.toLowerCase();
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div>
        <div className="flex items-center space-x-2 text-sky-400 font-semibold text-xs tracking-wider uppercase mb-1">
          <Library className="w-3.5 h-3.5" />
          <span>Shared Ecosystem</span>
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Community Eval Library</h1>
        <p className="text-sm text-slate-400 mt-1">
          Discover, inspect, fork, and test standardized evaluation packs contributed by the open-source community.
        </p>
      </div>

      <div className="flex flex-col sm:flex-row gap-3 items-center justify-between">
        <div className="relative w-full sm:w-96">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search packs by keyword, tool, or tag..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-100 focus:outline-none focus:border-sky-500"
          />
        </div>

        <div className="flex items-center space-x-1.5 overflow-x-auto w-full sm:w-auto">
          {categories.map((c) => (
            <button
              key={c}
              onClick={() => setSelectedCategory(c)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                selectedCategory === c
                  ? 'bg-sky-500 text-white'
                  : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800'
              }`}
            >
              {c}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filteredPacks.map((pack) => {
          const isActive = activePack.id === pack.id;
          return (
            <div
              key={pack.id}
              className={`border rounded-xl p-5 flex flex-col justify-between transition ${
                isActive
                  ? 'bg-slate-900/90 border-sky-500/50 shadow-lg shadow-sky-500/5'
                  : 'bg-slate-900/40 border-slate-800 hover:border-slate-700 hover:bg-slate-900/80'
              }`}
            >
              <div className="space-y-3">
                <div className="flex items-start justify-between">
                  <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center border border-slate-700">
                    <Box className="w-4 h-4 text-sky-400" />
                  </div>
                  <div className="flex items-center space-x-1 text-[11px] text-slate-500 font-mono">
                    <span>v{pack.version}</span>
                    <span>•</span>
                    <span className="text-slate-400">{pack.category}</span>
                  </div>
                </div>

                <div>
                  <h3 className="font-semibold text-sm text-white">{pack.name}</h3>
                  <p className="text-xs text-slate-400 mt-1 leading-relaxed line-clamp-3">
                    {pack.description}
                  </p>
                </div>

                <div className="flex flex-wrap gap-1 pt-1">
                  {pack.tags.slice(0, 3).map((t) => (
                    <span
                      key={t}
                      className="inline-flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300 font-mono"
                    >
                      <Tag className="w-2.5 h-2.5 text-slate-400" />
                      <span>{t}</span>
                    </span>
                  ))}
                </div>
              </div>

              <div className="pt-5 mt-5 border-t border-slate-800/80 flex items-center justify-between text-xs">
                <span className="text-slate-400 font-mono text-[11px]">
                  {pack.cases.length} test cases
                </span>

                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => onSelectPack(pack)}
                    className={`px-2.5 py-1.5 rounded-lg font-medium transition ${
                      isActive
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : 'bg-slate-800 hover:bg-slate-700 text-slate-200'
                    }`}
                  >
                    {isActive ? (
                      <span className="flex items-center space-x-1">
                        <Check className="w-3 h-3" />
                        <span>Active</span>
                      </span>
                    ) : (
                      'Select'
                    )}
                  </button>

                  <button
                    onClick={() => onLoadIntoRunner(pack)}
                    className="p-1.5 rounded-lg bg-sky-500 hover:bg-sky-400 text-white transition shadow-sm"
                    title="Load into Runner"
                  >
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
