// app/src/components/ConversationPanel.tsx
import { useState } from 'react';
import type { Conversation } from '../types/library';

interface ConversationPanelProps {
  conversations: Conversation[];
  onAsk: (question: string) => Promise<void>;
  isLoading: boolean;
  error?: string | null;
}

export function ConversationPanel({ conversations, onAsk, isLoading, error }: ConversationPanelProps) {
  const [question, setQuestion] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || isLoading) return;

    const q = question;
    setQuestion('');
    await onAsk(q);
  };

  const suggestedQuestions = [
    'How exactly does this work in practice?',
    'What are the key success factors?',
    'What challenges did they face?',
    'How does this apply to our context?',
  ];

  return (
    <div className="border-t border-gray-200 mt-6 pt-6">
      <h3 className="font-semibold text-gray-700 mb-4 flex items-center gap-2">
        <svg className="w-5 h-5 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
          />
        </svg>
        Ask a Question
      </h3>

      {/* Error message */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-3 mb-4">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      {/* Previous conversations */}
      {conversations.length > 0 && (
        <div className="space-y-4 mb-4 max-h-60 overflow-y-auto">
          {conversations.map((conv) => (
            <div key={conv.id} className="bg-gray-50 rounded-lg p-3">
              <p className="text-sm font-medium text-gray-700 mb-1">Q: {conv.question}</p>
              <p className="text-sm text-gray-600">{conv.answer}</p>
              {conv.source && (
                <p className="text-xs text-gray-400 mt-1 flex items-center gap-1">
                  <span
                    className={`w-2 h-2 rounded-full ${
                      conv.source === 'stored'
                        ? 'bg-green-400'
                        : conv.source === 'reasoning'
                          ? 'bg-blue-400'
                          : 'bg-purple-400'
                    }`}
                  />
                  {conv.source === 'stored'
                    ? 'From stored data'
                    : conv.source === 'reasoning'
                      ? 'AI reasoning'
                      : 'Web search'}
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Quick suggestions */}
      {conversations.length === 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {suggestedQuestions.map((sq) => (
            <button
              key={sq}
              onClick={() => setQuestion(sq)}
              className="text-xs bg-indigo-50 text-indigo-600 px-2 py-1 rounded hover:bg-indigo-100 transition-colors"
            >
              {sq}
            </button>
          ))}
        </div>
      )}

      {/* Input form */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about this case..."
          className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={!question.trim() || isLoading}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? (
            <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
                fill="none"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
          ) : (
            'Ask'
          )}
        </button>
      </form>
    </div>
  );
}
