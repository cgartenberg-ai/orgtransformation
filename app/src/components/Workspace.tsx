import type { PrincipleState } from '../types/userState';

interface WorkspaceProps {
  principleId: string;
  principleName: string;
  state: PrincipleState;
  onNotesChange: (notes: string) => void;
  onDraftChange: (draft: string) => void;
  onCrystallize: () => void;
}

export function Workspace({
  principleId,
  principleName,
  state,
  onNotesChange,
  onDraftChange,
  onCrystallize,
}: WorkspaceProps) {
  const canCrystallize = state.draftStance.trim().length > 0 && !state.crystallizedStance;

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        Your Workspace: {principleName}
      </h2>

      {/* Starred Items Summary */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-sm font-medium text-gray-700 mb-2">Starred Items</h3>
        <div className="flex gap-4 text-sm">
          <div className="flex items-center gap-1">
            <span className="text-amber-500">★</span>
            <span className="text-gray-600">{state.starredCases.length} cases</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="text-amber-500">★</span>
            <span className="text-gray-600">{state.starredPrinciples.length} principles</span>
          </div>
        </div>
      </div>

      {/* Notes Section */}
      <div className="mb-6">
        <label htmlFor={`notes-${principleId}`} className="block text-sm font-medium text-gray-700 mb-2">
          Notes & Observations
        </label>
        <textarea
          id={`notes-${principleId}`}
          value={state.notes}
          onChange={(e) => onNotesChange(e.target.value)}
          placeholder="Capture your thoughts, questions, and observations as you explore..."
          className="w-full h-32 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none"
        />
      </div>

      {/* Draft Stance Section */}
      <div className="mb-6">
        <label htmlFor={`draft-${principleId}`} className="block text-sm font-medium text-gray-700 mb-2">
          Draft Stance
        </label>
        <p className="text-xs text-gray-500 mb-2">
          Write your organization's position on this architectural principle. What will you do? Why?
        </p>
        <textarea
          id={`draft-${principleId}`}
          value={state.draftStance}
          onChange={(e) => onDraftChange(e.target.value)}
          placeholder="Our organization will... because..."
          className="w-full h-40 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none"
          disabled={!!state.crystallizedStance}
        />
      </div>

      {/* Crystallized Stance */}
      {state.crystallizedStance ? (
        <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="w-5 h-5 text-emerald-600"
            >
              <path
                fillRule="evenodd"
                d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm13.36-1.814a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z"
                clipRule="evenodd"
              />
            </svg>
            <h3 className="font-semibold text-emerald-700">Crystallized Stance</h3>
          </div>
          <p className="text-emerald-900">{state.crystallizedStance}</p>
        </div>
      ) : (
        <button
          onClick={onCrystallize}
          disabled={!canCrystallize}
          className={`w-full py-3 px-4 rounded-lg font-medium transition-colors ${
            canCrystallize
              ? 'bg-emerald-600 text-white hover:bg-emerald-700'
              : 'bg-gray-100 text-gray-400 cursor-not-allowed'
          }`}
        >
          {canCrystallize ? 'Crystallize Stance' : 'Write a draft stance to crystallize'}
        </button>
      )}

      {/* Last Modified */}
      <p className="text-xs text-gray-400 mt-4 text-right">
        Last modified: {new Date(state.lastModified).toLocaleString()}
      </p>
    </div>
  );
}
