// app/src/services/persistence.ts
import type { Conversation } from '../types/library';

const CONVERSATIONS_KEY = 'orgtransformation-conversations';

interface StoredConversations {
  cases: Record<string, Conversation[]>;
  principles: Record<string, Conversation[]>;
}

export function getStoredConversations(): StoredConversations {
  const stored = localStorage.getItem(CONVERSATIONS_KEY);
  if (stored) {
    return JSON.parse(stored);
  }
  return { cases: {}, principles: {} };
}

export function saveCaseConversations(caseId: string, conversations: Conversation[]): void {
  const stored = getStoredConversations();
  stored.cases[caseId] = conversations;
  localStorage.setItem(CONVERSATIONS_KEY, JSON.stringify(stored));
}

export function savePrincipleConversations(principleId: string, conversations: Conversation[]): void {
  const stored = getStoredConversations();
  stored.principles[principleId] = conversations;
  localStorage.setItem(CONVERSATIONS_KEY, JSON.stringify(stored));
}

export function getCaseConversations(caseId: string): Conversation[] {
  const stored = getStoredConversations();
  return stored.cases[caseId] || [];
}

export function getPrincipleConversations(principleId: string): Conversation[] {
  const stored = getStoredConversations();
  return stored.principles[principleId] || [];
}
