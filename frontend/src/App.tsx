import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { EvalCopilot } from './components/EvalCopilot';
import { EvalLinter } from './components/EvalLinter';
import { CommunityLibrary } from './components/CommunityLibrary';
import { EvalRunner } from './components/EvalRunner';
import { ReleaseGates } from './components/ReleaseGates';
import { ShareCommunity } from './components/ShareCommunity';
import { DEFAULT_PACKS } from './data/defaultPacks';
import { EvalPack, VariantScorecard } from './types';

export const App: React.FC = () => {
  const [packs, setPacks] = useState<EvalPack[]>(DEFAULT_PACKS);
  const [activePack, setActivePack] = useState<EvalPack>(DEFAULT_PACKS[0]);
  const [currentTab, setCurrentTab] = useState<string>('copilot');

  const [baselineCard, setBaselineCard] = useState<VariantScorecard | null>(null);
  const [candidateCard, setCandidateCard] = useState<VariantScorecard | null>(null);

  const handleSavePack = (newPack: EvalPack) => {
    setPacks((prev) => [newPack, ...prev]);
    setActivePack(newPack);
  };

  const handleLoadIntoRunner = (targetPack: EvalPack) => {
    setActivePack(targetPack);
    setCurrentTab('runner');
  };

  const handleSetScorecards = (base: VariantScorecard, cand: VariantScorecard) => {
    setBaselineCard(base);
    setCandidateCard(cand);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Navbar activePack={activePack} />

      <div className="flex-1 flex overflow-hidden">
        <Sidebar currentTab={currentTab} onSelectTab={setCurrentTab} />

        <main className="flex-1 overflow-y-auto p-6 lg:p-8">
          {currentTab === 'copilot' && (
            <EvalCopilot
              onSavePack={handleSavePack}
              onLoadIntoRunner={handleLoadIntoRunner}
            />
          )}

          {currentTab === 'linter' && (
            <EvalLinter activePack={activePack} />
          )}

          {currentTab === 'library' && (
            <CommunityLibrary
              packs={packs}
              activePack={activePack}
              onSelectPack={setActivePack}
              onLoadIntoRunner={handleLoadIntoRunner}
            />
          )}

          {currentTab === 'runner' && (
            <EvalRunner
              pack={activePack}
              baselineCard={baselineCard}
              candidateCard={candidateCard}
              onSetScorecards={handleSetScorecards}
              onGoToGates={() => setCurrentTab('gates')}
            />
          )}

          {currentTab === 'gates' && (
            <ReleaseGates
              candidateCard={candidateCard}
              baselineCard={baselineCard}
            />
          )}

          {currentTab === 'share' && (
            <ShareCommunity activePack={activePack} />
          )}
        </main>
      </div>
    </div>
  );
};

export default App;
