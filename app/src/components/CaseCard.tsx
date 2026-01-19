import type { Case, Conversation } from '../types/library';
import { DiagramIcon } from './DiagramIcon';
import { abbreviateInsight } from '../utils/abbreviateInsight';
import { ConversationPanel } from './ConversationPanel';
import { useCaseConversation } from '../hooks/useConversation';

interface CaseCardProps {
  caseStudy: Case;
  isStarred: boolean;
  onToggleStar: () => void;
  onExpand: () => void;
}

export function CaseCard({ caseStudy, isStarred, onToggleStar, onExpand }: CaseCardProps) {
  const abbreviatedInsight = abbreviateInsight(caseStudy.content.coreInsight || '');

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-start gap-3">
          <DiagramIcon templateId={caseStudy.diagramTemplate} className="w-12 h-12 flex-shrink-0" />
          <div>
            <h3 className="font-semibold text-gray-900">{caseStudy.company}</h3>
            <p className="text-sm text-gray-500">{caseStudy.title}</p>
          </div>
        </div>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onToggleStar();
          }}
          className={`p-1 rounded transition-colors ${
            isStarred
              ? 'text-amber-500 hover:text-amber-600'
              : 'text-gray-300 hover:text-gray-400'
          }`}
          aria-label={isStarred ? 'Unstar case' : 'Star case'}
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

      <p className="text-sm text-gray-600 mb-3 line-clamp-2">{caseStudy.summary}</p>

      {abbreviatedInsight && (
        <div className="bg-indigo-50 border-l-2 border-indigo-400 px-2 py-1 mb-3">
          <p className="text-sm text-indigo-800 font-medium italic">"{abbreviatedInsight}"</p>
        </div>
      )}

      <div className="flex items-center justify-end">
        <button
          onClick={onExpand}
          className="text-sm text-indigo-600 hover:text-indigo-800 font-medium"
        >
          Read More →
        </button>
      </div>
    </div>
  );
}

interface CaseExpandedViewProps {
  caseStudy: Case;
  isStarred: boolean;
  onToggleStar: () => void;
  onClose: () => void;
  onConversationUpdate?: (conversations: Conversation[]) => void;
}

export function CaseExpandedView({
  caseStudy,
  isStarred,
  onToggleStar,
  onClose,
  onConversationUpdate,
}: CaseExpandedViewProps) {
  const { conversations, isLoading, error, askQuestion } = useCaseConversation(
    caseStudy,
    onConversationUpdate
  );

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-gray-200 p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <DiagramIcon templateId={caseStudy.diagramTemplate} className="w-12 h-12" />
            <div>
              <h2 className="text-xl font-bold text-gray-900">{caseStudy.company}</h2>
              <p className="text-gray-500">{caseStudy.title}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={onToggleStar}
              className={`p-2 rounded transition-colors ${
                isStarred
                  ? 'text-amber-500 hover:text-amber-600'
                  : 'text-gray-300 hover:text-gray-400'
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
            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-gray-600 rounded"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth={2}
                className="w-6 h-6"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>

        <div className="p-6 space-y-6">
          <div>
            <h3 className="font-semibold text-gray-700 mb-2">What It Is</h3>
            <p className="text-gray-600">{caseStudy.content.whatItIs}</p>
          </div>

          {caseStudy.content.coreInsight && (
            <div className="bg-indigo-50 border-l-4 border-indigo-400 p-4">
              <h3 className="font-semibold text-indigo-700 mb-1">Core Insight</h3>
              <p className="text-indigo-900">{caseStudy.content.coreInsight}</p>
            </div>
          )}

          {caseStudy.content.howItWorks && caseStudy.content.howItWorks.length > 0 && (
            <div>
              <h3 className="font-semibold text-gray-700 mb-2">How It Works</h3>
              <ul className="space-y-2">
                {caseStudy.content.howItWorks.map((item: string, i: number) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="text-indigo-500 mt-1">•</span>
                    <span className="text-gray-600">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {caseStudy.content.keyMetrics && (
            <div className="bg-emerald-50 border-l-4 border-emerald-400 p-4">
              <h3 className="font-semibold text-emerald-700 mb-1">Key Metrics</h3>
              <p className="text-emerald-900">{caseStudy.content.keyMetrics}</p>
            </div>
          )}

          {caseStudy.content.sources && caseStudy.content.sources.length > 0 && (
            <div className="pt-4 border-t border-gray-200">
              <h3 className="font-semibold text-gray-500 text-sm mb-2">Sources</h3>
              <ul className="text-xs text-gray-400 space-y-1">
                {caseStudy.content.sources.map((source: string, i: number) => (
                  <li key={i}>{source}</li>
                ))}
              </ul>
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
