// app/src/hooks/useConversation.ts
import { useState, useCallback, useEffect } from 'react';
import type { Conversation, Case, DesignPrinciple } from '../types/library';
import { askAboutCase, askAboutPrinciple } from '../services/ai';
import {
  getCaseConversations,
  saveCaseConversations,
  getPrincipleConversations,
  savePrincipleConversations,
} from '../services/persistence';

interface UseConversationResult {
  conversations: Conversation[];
  isLoading: boolean;
  error: string | null;
  askQuestion: (question: string) => Promise<void>;
}

export function useCaseConversation(
  caseStudy: Case,
  onConversationUpdate?: (conversations: Conversation[]) => void
): UseConversationResult {
  // Merge stored conversations with JSON data
  const [conversations, setConversations] = useState<Conversation[]>(() => {
    const stored = getCaseConversations(caseStudy.id);
    const jsonConversations = caseStudy.conversations || [];
    // Merge, avoiding duplicates by id
    const existingIds = new Set(jsonConversations.map((c) => c.id));
    const newFromStorage = stored.filter((c) => !existingIds.has(c.id));
    return [...jsonConversations, ...newFromStorage];
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Persist conversations when they change
  useEffect(() => {
    if (conversations.length > 0) {
      saveCaseConversations(caseStudy.id, conversations);
    }
  }, [caseStudy.id, conversations]);

  const askQuestion = useCallback(
    async (question: string) => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await askAboutCase(caseStudy, question);

        const newConversation: Conversation = {
          id: `conv-${Date.now()}`,
          question,
          answer: response.answer,
          source: response.source,
          addedToContent: response.shouldPersist,
          timestamp: new Date().toISOString(),
        };

        const updated = [...conversations, newConversation];
        setConversations(updated);

        if (onConversationUpdate) {
          onConversationUpdate(updated);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setIsLoading(false);
      }
    },
    [caseStudy, conversations, onConversationUpdate]
  );

  return { conversations, isLoading, error, askQuestion };
}

export function usePrincipleConversation(
  principle: DesignPrinciple,
  onConversationUpdate?: (conversations: Conversation[]) => void
): UseConversationResult {
  // Merge stored conversations with JSON data
  const [conversations, setConversations] = useState<Conversation[]>(() => {
    const stored = getPrincipleConversations(principle.id);
    const jsonConversations = principle.conversations || [];
    // Merge, avoiding duplicates by id
    const existingIds = new Set(jsonConversations.map((c) => c.id));
    const newFromStorage = stored.filter((c) => !existingIds.has(c.id));
    return [...jsonConversations, ...newFromStorage];
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Persist conversations when they change
  useEffect(() => {
    if (conversations.length > 0) {
      savePrincipleConversations(principle.id, conversations);
    }
  }, [principle.id, conversations]);

  const askQuestion = useCallback(
    async (question: string) => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await askAboutPrinciple(principle, question);

        const newConversation: Conversation = {
          id: `conv-${Date.now()}`,
          question,
          answer: response.answer,
          source: response.source,
          addedToContent: response.shouldPersist,
          timestamp: new Date().toISOString(),
        };

        const updated = [...conversations, newConversation];
        setConversations(updated);

        if (onConversationUpdate) {
          onConversationUpdate(updated);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setIsLoading(false);
      }
    },
    [principle, conversations, onConversationUpdate]
  );

  return { conversations, isLoading, error, askQuestion };
}
