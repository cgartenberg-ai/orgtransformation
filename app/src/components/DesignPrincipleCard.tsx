import type { DesignPrinciple, PrincipleGroup, Conversation } from '../types/library';
import { PrincipleGroupIcon } from './PrincipleGroupIcon';
import { abbreviateInsight } from '../utils/abbreviateInsight';
import { ConversationPanel } from './ConversationPanel';
import { usePrincipleConversation } from '../hooks/useConversation';

interface DesignPrincipleCardProps {
  principle: DesignPrinciple;
  group?: PrincipleGroup;
  isStarred: boolean;
  onToggleStar: () => void;
  onExpand: () => void;
}

export function DesignPrincipleCard({
  principle,
  group,
  isStarred,
  onToggleStar,
  onExpand,
}: DesignPrincipleCardProps) {
  const keyPhrase = abbreviateInsight(principle.insight, 5);
  const groupColor = group?.color || '#94a3b8';

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start gap-3">
        {/* Group icon */}
        <div className="flex-shrink-0">
          <PrincipleGroupIcon groupId={principle.group} color={groupColor} className="w-10 h-10" />
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between mb-1">
            <h3 className="font-semibold text-gray-900 pr-2 text-sm">{principle.title}</h3>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onToggleStar();
              }}
              className={`p-1 rounded transition-colors flex-shrink-0 ${
                isStarred ? 'text-amber-500 hover:text-amber-600' : 'text-gray-300 hover:text-gray-400'
              }`}
              aria-label={isStarred ? 'Unstar principle' : 'Star principle'}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill={isStarred ? 'currentColor' : 'none'}
                stroke="currentColor"
                strokeWidth={2}
                className="w-5 h-5"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z"
                />
              </svg>
            </button>
          </div>

          {/* Abbreviated insight */}
          {keyPhrase && <p className="text-xs text-gray-600 mb-2 italic">"{keyPhrase}"</p>}

          <div className="flex items-center justify-between">
            <span
              className="text-xs px-2 py-1 rounded"
              style={{ backgroundColor: `${groupColor}20`, color: groupColor }}
            >
              {group?.name || principle.group}
            </span>
            <button
              onClick={onExpand}
              className="text-sm text-indigo-600 hover:text-indigo-800 font-medium"
            >
              Details →
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

interface DesignPrincipleExpandedViewProps {
  principle: DesignPrinciple;
  group?: PrincipleGroup;
  isStarred: boolean;
  onToggleStar: () => void;
  onClose: () => void;
  onConversationUpdate?: (conversations: Conversation[]) => void;
}

export function DesignPrincipleExpandedView({
  principle,
  group,
  isStarred,
  onToggleStar,
  onClose,
  onConversationUpdate,
}: DesignPrincipleExpandedViewProps) {
  const groupColor = group?.color || '#94a3b8';
  const { conversations, isLoading, error, askQuestion } = usePrincipleConversation(
    principle,
    onConversationUpdate
  );

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-gray-200 p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <PrincipleGroupIcon groupId={principle.group} color={groupColor} className="w-10 h-10" />
            <div>
              <h2 className="text-xl font-bold text-gray-900">{principle.title}</h2>
              <span
                className="text-sm px-2 py-0.5 rounded"
                style={{ backgroundColor: `${groupColor}20`, color: groupColor }}
              >
                {group?.name || principle.group}
              </span>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={onToggleStar}
              className={`p-2 rounded transition-colors ${
                isStarred ? 'text-amber-500 hover:text-amber-600' : 'text-gray-300 hover:text-gray-400'
              }`}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill={isStarred ? 'currentColor' : 'none'}
                stroke="currentColor"
                strokeWidth={2}
                className="w-6 h-6"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z"
                />
              </svg>
            </button>
            <button onClick={onClose} className="p-2 text-gray-400 hover:text-gray-600 rounded">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth={2}
                className="w-6 h-6"
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <div className="p-6 space-y-6">
          <div className="bg-purple-50 border-l-4 border-purple-400 p-4">
            <h3 className="font-semibold text-purple-700 mb-1">Core Insight</h3>
            <p className="text-purple-900">{principle.insight}</p>
          </div>

          {principle.manifestations && principle.manifestations.length > 0 && (
            <div>
              <h3 className="font-semibold text-gray-700 mb-2">Manifestations</h3>
              <ul className="space-y-2">
                {principle.manifestations.map((item: string, i: number) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="text-purple-500 mt-1">•</span>
                    <span className="text-gray-600">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {principle.test && (
            <div className="bg-amber-50 border-l-4 border-amber-400 p-4">
              <h3 className="font-semibold text-amber-700 mb-1">Diagnostic Test</h3>
              <p className="text-amber-900">{principle.test}</p>
            </div>
          )}

          {/* Conversation Panel */}
          <ConversationPanel
            conversations={conversations}
            onAsk={askQuestion}
            isLoading={isLoading}
            error={error}
          />
        </div>
      </div>
    </div>
  );
}
