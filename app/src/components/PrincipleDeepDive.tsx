import { useState } from 'react';
import type { ArchitecturalPrinciple, Case, DesignPrinciple, PrincipleGroup } from '../types/library';
import type { PrincipleState } from '../types/userState';
import { CaseCard, CaseExpandedView } from './CaseCard';
import { DesignPrincipleCard, DesignPrincipleExpandedView } from './DesignPrincipleCard';
import { Workspace } from './Workspace';

interface PrincipleDeepDiveProps {
  principle: ArchitecturalPrinciple;
  cases: Case[];
  designPrinciples: DesignPrinciple[];
  principleGroups: PrincipleGroup[];
  principleState: PrincipleState;
  onBack: () => void;
  onToggleStarCase: (caseId: string) => void;
  onToggleStarPrinciple: (principleId: string) => void;
  onNotesChange: (notes: string) => void;
  onDraftChange: (draft: string) => void;
  onCrystallize: () => void;
}

type Tab = 'cases' | 'principles' | 'workspace';

export function PrincipleDeepDive({
  principle,
  cases,
  designPrinciples,
  principleGroups,
  principleState,
  onBack,
  onToggleStarCase,
  onToggleStarPrinciple,
  onNotesChange,
  onDraftChange,
  onCrystallize,
}: PrincipleDeepDiveProps) {
  const [activeTab, setActiveTab] = useState<Tab>('cases');
  const [expandedCase, setExpandedCase] = useState<Case | null>(null);
  const [expandedPrinciple, setExpandedPrinciple] = useState<DesignPrinciple | null>(null);

  // Group design principles by their group
  const principlesByGroup = principleGroups.map((group) => ({
    group,
    principles: designPrinciples.filter((p) => p.group === group.id),
  })).filter((g) => g.principles.length > 0);

  const tabs: { id: Tab; label: string; count?: number }[] = [
    { id: 'cases', label: 'Case Studies', count: cases.length },
    { id: 'principles', label: 'Design Principles', count: designPrinciples.length },
    { id: 'workspace', label: 'Workspace' },
  ];

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={onBack}
          className="flex items-center gap-1 text-gray-600 hover:text-gray-900 mb-4"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth={2}
            className="w-5 h-5"
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
          </svg>
          Back to Stack
        </button>

        <h1 className="text-2xl font-bold text-gray-900 mb-2">{principle.name}</h1>
        <p className="text-lg text-indigo-600 mb-2">{principle.coreQuestion}</p>
        <p className="text-gray-600">{principle.whyArchitectural}</p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="flex gap-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-3 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === tab.id
                  ? 'border-indigo-600 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab.label}
              {tab.count !== undefined && (
                <span className={`ml-2 px-2 py-0.5 rounded-full text-xs ${
                  activeTab === tab.id
                    ? 'bg-indigo-100 text-indigo-600'
                    : 'bg-gray-100 text-gray-500'
                }`}>
                  {tab.count}
                </span>
              )}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === 'cases' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {cases.map((caseStudy) => (
            <CaseCard
              key={caseStudy.id}
              caseStudy={caseStudy}
              isStarred={principleState.starredCases.includes(caseStudy.id)}
              onToggleStar={() => onToggleStarCase(caseStudy.id)}
              onExpand={() => setExpandedCase(caseStudy)}
            />
          ))}
          {cases.length === 0 && (
            <p className="text-gray-500 col-span-full text-center py-8">
              No case studies available for this principle yet.
            </p>
          )}
        </div>
      )}

      {activeTab === 'principles' && (
        <div className="space-y-8">
          {principlesByGroup.map(({ group, principles }) => (
            <div key={group.id}>
              <h3 className="text-lg font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <span
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: group.color }}
                />
                {group.name}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {principles.map((designPrinciple) => (
                  <DesignPrincipleCard
                    key={designPrinciple.id}
                    principle={designPrinciple}
                    group={group}
                    isStarred={principleState.starredPrinciples.includes(designPrinciple.id)}
                    onToggleStar={() => onToggleStarPrinciple(designPrinciple.id)}
                    onExpand={() => setExpandedPrinciple(designPrinciple)}
                  />
                ))}
              </div>
            </div>
          ))}
          {designPrinciples.length === 0 && (
            <p className="text-gray-500 text-center py-8">
              No design principles available for this architectural principle yet.
            </p>
          )}
        </div>
      )}

      {activeTab === 'workspace' && (
        <Workspace
          principleId={principle.id}
          principleName={principle.name}
          state={principleState}
          onNotesChange={onNotesChange}
          onDraftChange={onDraftChange}
          onCrystallize={onCrystallize}
        />
      )}

      {/* Expanded Case Modal */}
      {expandedCase && (
        <CaseExpandedView
          caseStudy={expandedCase}
          isStarred={principleState.starredCases.includes(expandedCase.id)}
          onToggleStar={() => onToggleStarCase(expandedCase.id)}
          onClose={() => setExpandedCase(null)}
        />
      )}

      {/* Expanded Principle Modal */}
      {expandedPrinciple && (
        <DesignPrincipleExpandedView
          principle={expandedPrinciple}
          group={principleGroups.find((g) => g.id === expandedPrinciple.group)}
          isStarred={principleState.starredPrinciples.includes(expandedPrinciple.id)}
          onToggleStar={() => onToggleStarPrinciple(expandedPrinciple.id)}
          onClose={() => setExpandedPrinciple(null)}
        />
      )}
    </div>
  );
}
