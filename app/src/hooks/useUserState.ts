import { useState, useEffect, useCallback } from 'react';
import type { UserState, PrincipleState, PrincipleStatus } from '../types/userState';
import { createEmptyPrincipleState } from '../types/userState';

const STORAGE_KEY = 'ai-transformation-user-state';

export interface UseUserStateResult {
  userState: UserState;
  getPrincipleState: (principleId: string) => PrincipleState;
  updatePrincipleStatus: (principleId: string, status: PrincipleStatus) => void;
  toggleStarredCase: (principleId: string, caseId: string) => void;
  toggleStarredPrinciple: (principleId: string, designPrincipleId: string) => void;
  updateNotes: (principleId: string, notes: string) => void;
  updateDraftStance: (principleId: string, draft: string) => void;
  crystallizeStance: (principleId: string) => void;
  resetPrinciple: (principleId: string) => void;
  resetAll: () => void;
}

function loadFromStorage(): UserState {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      return JSON.parse(stored);
    }
  } catch (e) {
    console.error('Failed to load user state from localStorage:', e);
  }
  return {};
}

function saveToStorage(state: UserState): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (e) {
    console.error('Failed to save user state to localStorage:', e);
  }
}

export function useUserState(): UseUserStateResult {
  const [userState, setUserState] = useState<UserState>(() => loadFromStorage());

  // Persist to localStorage whenever state changes
  useEffect(() => {
    saveToStorage(userState);
  }, [userState]);

  const getPrincipleState = useCallback(
    (principleId: string): PrincipleState => {
      return userState[principleId] || createEmptyPrincipleState();
    },
    [userState]
  );

  const updatePrincipleState = useCallback(
    (principleId: string, updates: Partial<PrincipleState>) => {
      setUserState((prev) => ({
        ...prev,
        [principleId]: {
          ...(prev[principleId] || createEmptyPrincipleState()),
          ...updates,
          lastModified: new Date().toISOString(),
        },
      }));
    },
    []
  );

  const updatePrincipleStatus = useCallback(
    (principleId: string, status: PrincipleStatus) => {
      updatePrincipleState(principleId, { status });
    },
    [updatePrincipleState]
  );

  const toggleStarredCase = useCallback(
    (principleId: string, caseId: string) => {
      setUserState((prev) => {
        const current = prev[principleId] || createEmptyPrincipleState();
        const starredCases = current.starredCases.includes(caseId)
          ? current.starredCases.filter((id) => id !== caseId)
          : [...current.starredCases, caseId];
        return {
          ...prev,
          [principleId]: {
            ...current,
            starredCases,
            lastModified: new Date().toISOString(),
          },
        };
      });
    },
    []
  );

  const toggleStarredPrinciple = useCallback(
    (principleId: string, designPrincipleId: string) => {
      setUserState((prev) => {
        const current = prev[principleId] || createEmptyPrincipleState();
        const starredPrinciples = current.starredPrinciples.includes(designPrincipleId)
          ? current.starredPrinciples.filter((id) => id !== designPrincipleId)
          : [...current.starredPrinciples, designPrincipleId];
        return {
          ...prev,
          [principleId]: {
            ...current,
            starredPrinciples,
            lastModified: new Date().toISOString(),
          },
        };
      });
    },
    []
  );

  const updateNotes = useCallback(
    (principleId: string, notes: string) => {
      updatePrincipleState(principleId, { notes });
    },
    [updatePrincipleState]
  );

  const updateDraftStance = useCallback(
    (principleId: string, draftStance: string) => {
      updatePrincipleState(principleId, { draftStance });
    },
    [updatePrincipleState]
  );

  const crystallizeStance = useCallback(
    (principleId: string) => {
      setUserState((prev) => {
        const current = prev[principleId] || createEmptyPrincipleState();
        return {
          ...prev,
          [principleId]: {
            ...current,
            crystallizedStance: current.draftStance,
            status: 'stance-taken' as PrincipleStatus,
            lastModified: new Date().toISOString(),
          },
        };
      });
    },
    []
  );

  const resetPrinciple = useCallback((principleId: string) => {
    setUserState((prev) => {
      const { [principleId]: _, ...rest } = prev;
      return rest;
    });
  }, []);

  const resetAll = useCallback(() => {
    setUserState({});
  }, []);

  return {
    userState,
    getPrincipleState,
    updatePrincipleStatus,
    toggleStarredCase,
    toggleStarredPrinciple,
    updateNotes,
    updateDraftStance,
    crystallizeStance,
    resetPrinciple,
    resetAll,
  };
}
