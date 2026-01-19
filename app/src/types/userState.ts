export type PrincipleStatus = 'unexplored' | 'in-progress' | 'stance-taken';

export interface PrincipleState {
  status: PrincipleStatus;
  starredCases: string[];
  starredPrinciples: string[];
  notes: string;
  draftStance: string;
  crystallizedStance: string | null;
  lastModified: string;
}

export interface UserState {
  [principleId: string]: PrincipleState;
}

export const createEmptyPrincipleState = (): PrincipleState => ({
  status: 'unexplored',
  starredCases: [],
  starredPrinciples: [],
  notes: '',
  draftStance: '',
  crystallizedStance: null,
  lastModified: new Date().toISOString(),
});
