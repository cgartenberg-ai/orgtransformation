import { useState } from 'react';
import { useLibrary } from './hooks/useLibrary';
import { useUserState } from './hooks/useUserState';
import { StackView } from './components/StackView';
import { PrincipleDeepDive } from './components/PrincipleDeepDive';
import { SettingsPanel } from './components/SettingsPanel';

function SettingsButton({ onClick }: { onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="fixed top-4 right-4 p-2 bg-white rounded-full shadow-md hover:shadow-lg transition-shadow z-40"
      aria-label="Settings"
    >
      <svg className="w-6 h-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
        />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    </button>
  );
}

function App() {
  const { library, lookups, isLoading } = useLibrary();
  const {
    getPrincipleState,
    updatePrincipleStatus,
    toggleStarredCase,
    toggleStarredPrinciple,
    updateNotes,
    updateDraftStance,
    crystallizeStance,
  } = useUserState();

  const [selectedPrincipleId, setSelectedPrincipleId] = useState<string | null>(null);
  const [showSettings, setShowSettings] = useState(false);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  const selectedPrinciple = selectedPrincipleId
    ? lookups.getArchitecturalPrinciple(selectedPrincipleId)
    : null;

  const handlePrincipleClick = (principleId: string) => {
    setSelectedPrincipleId(principleId);
    // Mark as in-progress if unexplored
    const state = getPrincipleState(principleId);
    if (state.status === 'unexplored') {
      updatePrincipleStatus(principleId, 'in-progress');
    }
  };

  const handleBack = () => {
    setSelectedPrincipleId(null);
  };

  // Stack View
  if (!selectedPrinciple) {
    return (
      <div className="min-h-screen bg-gray-50">
        <SettingsButton onClick={() => setShowSettings(true)} />
        <StackView
          layers={library.layers}
          architecturalPrinciples={library.architecturalPrinciples}
          getPrincipleState={getPrincipleState}
          onPrincipleClick={handlePrincipleClick}
        />
        <SettingsPanel isOpen={showSettings} onClose={() => setShowSettings(false)} />
      </div>
    );
  }

  // Principle Deep-Dive View
  const cases = lookups.getCasesForPrinciple(selectedPrincipleId!);
  const designPrinciples = lookups.getDesignPrinciplesForPrinciple(selectedPrincipleId!);
  const principleState = getPrincipleState(selectedPrincipleId!);

  return (
    <div className="min-h-screen bg-gray-50">
      <SettingsButton onClick={() => setShowSettings(true)} />
      <PrincipleDeepDive
        principle={selectedPrinciple}
        cases={cases}
        designPrinciples={designPrinciples}
        principleGroups={library.principleGroups}
        principleState={principleState}
        onBack={handleBack}
        onToggleStarCase={(caseId) => toggleStarredCase(selectedPrincipleId!, caseId)}
        onToggleStarPrinciple={(principleId) => toggleStarredPrinciple(selectedPrincipleId!, principleId)}
        onNotesChange={(notes) => updateNotes(selectedPrincipleId!, notes)}
        onDraftChange={(draft) => updateDraftStance(selectedPrincipleId!, draft)}
        onCrystallize={() => crystallizeStance(selectedPrincipleId!)}
      />
      <SettingsPanel isOpen={showSettings} onClose={() => setShowSettings(false)} />
    </div>
  );
}

export default App;
