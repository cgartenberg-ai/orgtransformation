import { useState } from 'react';
import { useLibrary } from './hooks/useLibrary';
import { useUserState } from './hooks/useUserState';
import { StackView } from './components/StackView';
import { PrincipleDeepDive } from './components/PrincipleDeepDive';

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
        <StackView
          layers={library.layers}
          architecturalPrinciples={library.architecturalPrinciples}
          getPrincipleState={getPrincipleState}
          onPrincipleClick={handlePrincipleClick}
        />
      </div>
    );
  }

  // Principle Deep-Dive View
  const cases = lookups.getCasesForPrinciple(selectedPrincipleId!);
  const designPrinciples = lookups.getDesignPrinciplesForPrinciple(selectedPrincipleId!);
  const principleState = getPrincipleState(selectedPrincipleId!);

  return (
    <div className="min-h-screen bg-gray-50">
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
    </div>
  );
}

export default App;
