# Case Visuals & Conversation Interface Implementation Plan

> **For Claude:** Use /superpowers-execute-plan to implement this plan task-by-task.

**Goal:** Fix two bugs: (1) Add visual diagrams to case cards that visually distinguish structural patterns, with abbreviated key phrases instead of full core insights; (2) Enable AI-powered conversations at the card level that expand the library data over time.

**Architecture:**
- Phase 1: Create 9 SVG diagram templates as React components (each visually distinctive to convey the structural pattern), update CaseCard to show diagram + auto-abbreviated key phrase, move full core insight to expanded view only
- Phase 2: Add conversation UI to expanded views with 3-tier knowledge system: (1) stored data first, (2) AI reasoning second, (3) web search fallback - conversations expand the JSON data files

**Tech Stack:** React 19, TypeScript, Tailwind CSS, Claude API (Anthropic SDK), Web Search API (user-provided)

---

## Design Decisions (from conversation)

### Bug 1: Visual Diagrams & Abbreviated Insights

**The 9 structural templates** map to cases as follows (some models share templates):

| Template | Pattern | Companies |
|----------|---------|-----------|
| Centralized Lab | Dedicated unit, separate from operations | Google X, Samsung C-Lab, Sanofi AI Factory |
| Distributed Hubs | Multiple semi-autonomous units | Eli Lilly (domain hubs) |
| Embedded/Universal | AI capability expected everywhere, no separate lab | Shopify, Moderna, NVIDIA |
| Center of Excellence | Central team serving the whole org | JPMorgan ML CoE, Bank of America |
| Product as Lab | Deployed products generate learning | Tesla Fleet |
| Hybrid (Labs + Core) | Separate exploration team + core product | Anthropic |
| Tight Loop | Rapid iteration between prediction and validation | Roche/Genentech, Recursion |
| External Acquisition | Capability acquired from outside | McKinsey/QuantumBlack |
| Broad Deployment | Skip pilots, deploy widely immediately | P&G ChatPG |

**Core Insight handling:**
- Card view: Show auto-abbreviated 3-5 word key phrase (extracted from full insight)
- Expanded view: Show full core insight
- The same approach applies to design principles

### Bug 2: Conversation Interface

**3-tier knowledge system:**
1. **Stored data first** - Check existing conversations and extendedContent in the JSON
2. **AI reasoning** - Use Claude to answer based on the case context
3. **Web search fallback** - If Claude indicates it needs more info, search the web

**Data expansion:**
- Conversations are persisted to localStorage
- Valuable learnings (flagged by AI as new information) are marked for potential JSON expansion
- Future: ability to export enriched JSON back to files

---

## Phase 1: Visual Diagrams & Abbreviated Insights

### Task 1: Create DiagramIcon Component

**Files:**
- Create: `app/src/components/DiagramIcon.tsx`

**Step 1: Create the component file**

Create a component that renders different SVG diagrams based on template ID. Each diagram should be a simple, distinctive visual that conveys the structural pattern.

```tsx
// app/src/components/DiagramIcon.tsx
import type { FC } from 'react';

interface DiagramIconProps {
  templateId: string;
  className?: string;
}

export const DiagramIcon: FC<DiagramIconProps> = ({ templateId, className = 'w-16 h-16' }) => {
  const diagrams: Record<string, JSX.Element> = {
    'centralized-lab': (
      // Single large circle (lab) separate from grid of small circles (operations)
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="20" cy="32" r="14" fill="#6366f1" opacity="0.8" />
        <rect x="40" y="16" width="6" height="6" rx="1" fill="#94a3b8" />
        <rect x="48" y="16" width="6" height="6" rx="1" fill="#94a3b8" />
        <rect x="40" y="24" width="6" height="6" rx="1" fill="#94a3b8" />
        <rect x="48" y="24" width="6" height="6" rx="1" fill="#94a3b8" />
        <rect x="40" y="32" width="6" height="6" rx="1" fill="#94a3b8" />
        <rect x="48" y="32" width="6" height="6" rx="1" fill="#94a3b8" />
        <rect x="40" y="40" width="6" height="6" rx="1" fill="#94a3b8" />
        <rect x="48" y="40" width="6" height="6" rx="1" fill="#94a3b8" />
        <line x1="34" y1="32" x2="38" y2="32" stroke="#cbd5e1" strokeWidth="2" strokeDasharray="2 2" />
      </svg>
    ),
    'distributed-hubs': (
      // Multiple medium circles spread out, connected by lines
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="16" cy="16" r="8" fill="#6366f1" opacity="0.7" />
        <circle cx="48" cy="16" r="8" fill="#6366f1" opacity="0.7" />
        <circle cx="16" cy="48" r="8" fill="#6366f1" opacity="0.7" />
        <circle cx="48" cy="48" r="8" fill="#6366f1" opacity="0.7" />
        <circle cx="32" cy="32" r="6" fill="#94a3b8" opacity="0.5" />
        <line x1="24" y1="16" x2="40" y2="16" stroke="#cbd5e1" strokeWidth="1.5" />
        <line x1="16" y1="24" x2="16" y2="40" stroke="#cbd5e1" strokeWidth="1.5" />
        <line x1="48" y1="24" x2="48" y2="40" stroke="#cbd5e1" strokeWidth="1.5" />
        <line x1="24" y1="48" x2="40" y2="48" stroke="#cbd5e1" strokeWidth="1.5" />
      </svg>
    ),
    'embedded-universal': (
      // Grid of identical circles all with AI indicator
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="16" cy="16" r="6" fill="#6366f1" opacity="0.6" />
        <circle cx="32" cy="16" r="6" fill="#6366f1" opacity="0.6" />
        <circle cx="48" cy="16" r="6" fill="#6366f1" opacity="0.6" />
        <circle cx="16" cy="32" r="6" fill="#6366f1" opacity="0.6" />
        <circle cx="32" cy="32" r="6" fill="#6366f1" opacity="0.6" />
        <circle cx="48" cy="32" r="6" fill="#6366f1" opacity="0.6" />
        <circle cx="16" cy="48" r="6" fill="#6366f1" opacity="0.6" />
        <circle cx="32" cy="48" r="6" fill="#6366f1" opacity="0.6" />
        <circle cx="48" cy="48" r="6" fill="#6366f1" opacity="0.6" />
        <text x="16" y="19" textAnchor="middle" fontSize="8" fill="white">AI</text>
        <text x="32" y="19" textAnchor="middle" fontSize="8" fill="white">AI</text>
        <text x="48" y="19" textAnchor="middle" fontSize="8" fill="white">AI</text>
        <text x="16" y="35" textAnchor="middle" fontSize="8" fill="white">AI</text>
        <text x="32" y="35" textAnchor="middle" fontSize="8" fill="white">AI</text>
        <text x="48" y="35" textAnchor="middle" fontSize="8" fill="white">AI</text>
        <text x="16" y="51" textAnchor="middle" fontSize="8" fill="white">AI</text>
        <text x="32" y="51" textAnchor="middle" fontSize="8" fill="white">AI</text>
        <text x="48" y="51" textAnchor="middle" fontSize="8" fill="white">AI</text>
      </svg>
    ),
    'center-of-excellence': (
      // Central circle with spokes radiating to outer circles
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="32" cy="32" r="10" fill="#6366f1" opacity="0.8" />
        <circle cx="32" cy="8" r="5" fill="#94a3b8" />
        <circle cx="56" cy="32" r="5" fill="#94a3b8" />
        <circle cx="32" cy="56" r="5" fill="#94a3b8" />
        <circle cx="8" cy="32" r="5" fill="#94a3b8" />
        <line x1="32" y1="22" x2="32" y2="13" stroke="#6366f1" strokeWidth="2" />
        <line x1="42" y1="32" x2="51" y2="32" stroke="#6366f1" strokeWidth="2" />
        <line x1="32" y1="42" x2="32" y2="51" stroke="#6366f1" strokeWidth="2" />
        <line x1="22" y1="32" x2="13" y2="32" stroke="#6366f1" strokeWidth="2" />
      </svg>
    ),
    'product-as-lab': (
      // Product box with arrows cycling back (data flywheel)
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="18" y="22" width="28" height="20" rx="2" fill="#6366f1" opacity="0.7" />
        <text x="32" y="35" textAnchor="middle" fontSize="8" fill="white">PRODUCT</text>
        <path d="M32 8 L40 16 L36 16 L36 20 L28 20 L28 16 L24 16 Z" fill="#10b981" />
        <path d="M32 56 L24 48 L28 48 L28 44 L36 44 L36 48 L40 48 Z" fill="#10b981" />
        <path d="M8 32 L16 24 L16 28 L18 28 L18 36 L16 36 L16 40 Z" fill="#94a3b8" opacity="0.6" />
        <path d="M56 32 L48 40 L48 36 L46 36 L46 28 L48 28 L48 24 Z" fill="#94a3b8" opacity="0.6" />
      </svg>
    ),
    'hybrid-labs-core': (
      // Two connected circles - one labeled Labs, one Core
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="20" cy="32" r="12" fill="#6366f1" opacity="0.8" />
        <circle cx="44" cy="32" r="12" fill="#10b981" opacity="0.7" />
        <ellipse cx="32" cy="32" rx="4" ry="8" fill="#6366f1" opacity="0.3" />
        <text x="20" y="35" textAnchor="middle" fontSize="6" fill="white">Labs</text>
        <text x="44" y="35" textAnchor="middle" fontSize="6" fill="white">Core</text>
      </svg>
    ),
    'tight-loop': (
      // Two boxes with circular arrows between them
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="6" y="22" width="20" height="20" rx="2" fill="#6366f1" opacity="0.7" />
        <rect x="38" y="22" width="20" height="20" rx="2" fill="#10b981" opacity="0.7" />
        <text x="16" y="35" textAnchor="middle" fontSize="5" fill="white">Predict</text>
        <text x="48" y="35" textAnchor="middle" fontSize="5" fill="white">Validate</text>
        <path d="M28 28 C32 24, 34 24, 36 28" stroke="#f59e0b" strokeWidth="2" fill="none" markerEnd="url(#arrowhead)" />
        <path d="M36 36 C34 40, 32 40, 28 36" stroke="#f59e0b" strokeWidth="2" fill="none" markerEnd="url(#arrowhead)" />
        <defs>
          <marker id="arrowhead" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
            <polygon points="0 0, 6 3, 0 6" fill="#f59e0b" />
          </marker>
        </defs>
      </svg>
    ),
    'external-acquisition': (
      // Arrow coming from outside into org boundary
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="24" y="12" width="32" height="40" rx="2" stroke="#94a3b8" strokeWidth="2" strokeDasharray="4 2" fill="none" />
        <circle cx="40" cy="32" r="10" fill="#6366f1" opacity="0.7" />
        <circle cx="10" cy="32" r="8" fill="#10b981" opacity="0.8" />
        <path d="M18 32 L22 32" stroke="#10b981" strokeWidth="3" />
        <polygon points="24,32 20,28 20,36" fill="#10b981" />
      </svg>
    ),
    'broad-deployment': (
      // Single source spreading to many targets simultaneously
      <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="32" r="8" fill="#6366f1" opacity="0.8" />
        <circle cx="44" cy="12" r="5" fill="#94a3b8" />
        <circle cx="52" cy="24" r="5" fill="#94a3b8" />
        <circle cx="56" cy="38" r="5" fill="#94a3b8" />
        <circle cx="52" cy="52" r="5" fill="#94a3b8" />
        <circle cx="40" cy="56" r="5" fill="#94a3b8" />
        <line x1="20" y1="28" x2="39" y2="14" stroke="#6366f1" strokeWidth="1.5" />
        <line x1="20" y1="30" x2="47" y2="24" stroke="#6366f1" strokeWidth="1.5" />
        <line x1="20" y1="32" x2="51" y2="38" stroke="#6366f1" strokeWidth="1.5" />
        <line x1="20" y1="34" x2="47" y2="50" stroke="#6366f1" strokeWidth="1.5" />
        <line x1="20" y1="36" x2="35" y2="54" stroke="#6366f1" strokeWidth="1.5" />
      </svg>
    ),
  };

  return diagrams[templateId] || (
    <svg viewBox="0 0 64 64" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="8" y="8" width="48" height="48" rx="4" stroke="#94a3b8" strokeWidth="2" fill="none" />
      <text x="32" y="36" textAnchor="middle" fontSize="10" fill="#94a3b8">?</text>
    </svg>
  );
};
```

**Step 2: Verify the component compiles**

Run: `cd app && npm run build 2>&1 | head -20`
Expected: No TypeScript errors related to DiagramIcon

**Step 3: Commit**

```bash
git add app/src/components/DiagramIcon.tsx
git commit -m "feat: add DiagramIcon component with 9 structural pattern SVGs"
```

---

### Task 2: Create Insight Abbreviation Utility

**Files:**
- Create: `app/src/utils/abbreviateInsight.ts`

**Step 1: Create the utility function**

This function extracts a 3-5 word key phrase from a longer insight text.

```typescript
// app/src/utils/abbreviateInsight.ts

/**
 * Extracts a 3-5 word key phrase from a longer insight.
 * Strategy: Find the most meaningful short phrase, prioritizing:
 * 1. Quoted text (often the key message)
 * 2. Text after colons (often the punchline)
 * 3. First significant clause
 */
export function abbreviateInsight(fullInsight: string, maxWords: number = 5): string {
  if (!fullInsight) return '';

  // Strategy 1: Look for quoted text (CEO quotes, key phrases)
  const quotedMatch = fullInsight.match(/'([^']+)'/);
  if (quotedMatch && quotedMatch[1]) {
    const quoted = quotedMatch[1];
    const words = quoted.split(/\s+/);
    if (words.length <= maxWords + 2) {
      // Return the quoted portion, possibly truncated
      return words.slice(0, maxWords).join(' ') + (words.length > maxWords ? '...' : '');
    }
  }

  // Strategy 2: Look for text after a colon (often the key insight)
  const colonIndex = fullInsight.indexOf(':');
  if (colonIndex !== -1 && colonIndex < fullInsight.length - 10) {
    const afterColon = fullInsight.slice(colonIndex + 1).trim();
    // Take first phrase/clause
    const firstClause = afterColon.split(/[.;,]/)[0].trim();
    const words = firstClause.split(/\s+/);
    if (words.length >= 3) {
      return words.slice(0, maxWords).join(' ') + (words.length > maxWords ? '...' : '');
    }
  }

  // Strategy 3: Extract key verb phrase or first meaningful chunk
  // Remove common filler starts
  let processed = fullInsight
    .replace(/^(The insight is that|The core insight is|CEO [^:]+:|[A-Z][a-z]+ [A-Z][a-z]+:)\s*/i, '')
    .trim();

  // Take first clause
  const firstClause = processed.split(/[.;]/)[0].trim();
  const words = firstClause.split(/\s+/);

  // If very short, use as-is
  if (words.length <= maxWords) {
    return firstClause;
  }

  // Otherwise truncate and add ellipsis
  return words.slice(0, maxWords).join(' ') + '...';
}
```

**Step 2: Verify the utility compiles**

Run: `cd app && npm run build 2>&1 | head -20`
Expected: No TypeScript errors

**Step 3: Commit**

```bash
git add app/src/utils/abbreviateInsight.ts
git commit -m "feat: add abbreviateInsight utility for 3-5 word key phrases"
```

---

### Task 3: Update CaseCard to Use Diagram and Abbreviated Insight

**Files:**
- Modify: `app/src/components/CaseCard.tsx`

**Step 1: Update the CaseCard component**

Replace the current core insight display with the diagram and abbreviated insight.

```tsx
// app/src/components/CaseCard.tsx
import type { Case } from '../types/library';
import { DiagramIcon } from './DiagramIcon';
import { abbreviateInsight } from '../utils/abbreviateInsight';

interface CaseCardProps {
  caseStudy: Case;
  isStarred: boolean;
  onToggleStar: () => void;
  onExpand: () => void;
}

export function CaseCard({ caseStudy, isStarred, onToggleStar, onExpand }: CaseCardProps) {
  const keyPhrase = abbreviateInsight(caseStudy.content.coreInsight || '', 5);

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start gap-3">
        {/* Visual diagram */}
        <div className="flex-shrink-0">
          <DiagramIcon templateId={caseStudy.diagramTemplate} className="w-14 h-14" />
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between mb-1">
            <div>
              <h3 className="font-semibold text-gray-900">{caseStudy.company}</h3>
              <p className="text-sm text-gray-500">{caseStudy.title}</p>
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onToggleStar();
              }}
              className={`p-1 rounded transition-colors flex-shrink-0 ${
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

          <p className="text-sm text-gray-600 mb-2 line-clamp-2">{caseStudy.summary}</p>

          {/* Abbreviated key phrase instead of full core insight */}
          {keyPhrase && (
            <p className="text-xs text-indigo-600 font-medium mb-2 italic">"{keyPhrase}"</p>
          )}

          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-400 bg-gray-100 px-2 py-1 rounded">
              {caseStudy.diagramTemplate.replace(/-/g, ' ')}
            </span>
            <button
              onClick={onExpand}
              className="text-sm text-indigo-600 hover:text-indigo-800 font-medium"
            >
              Read More
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// CaseExpandedView stays the same (full core insight visible there)
interface CaseExpandedViewProps {
  caseStudy: Case;
  isStarred: boolean;
  onToggleStar: () => void;
  onClose: () => void;
}

export function CaseExpandedView({
  caseStudy,
  isStarred,
  onToggleStar,
  onClose,
}: CaseExpandedViewProps) {
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

          <div className="pt-4 border-t border-gray-200">
            <p className="text-xs text-gray-400">
              Diagram Template: {caseStudy.diagramTemplate}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
```

**Step 2: Verify the app compiles and runs**

Run: `cd app && npm run build`
Expected: Build completes successfully

**Step 3: Manual test**

Run: `cd app && npm run dev`
- Open browser to localhost:5173
- Navigate to a principle deep dive
- Verify case cards show diagram icons and abbreviated insights
- Click "Read More" and verify full core insight appears in expanded view

**Step 4: Commit**

```bash
git add app/src/components/CaseCard.tsx
git commit -m "feat: update CaseCard with visual diagrams and abbreviated insights"
```

---

### Task 4: Add Diagram Icons to Design Principle Cards

**Files:**
- Create: `app/src/components/PrincipleGroupIcon.tsx`
- Modify: `app/src/components/DesignPrincipleCard.tsx`

**Step 1: Create PrincipleGroupIcon component**

Each principle group gets a distinctive visual based on its theme.

```tsx
// app/src/components/PrincipleGroupIcon.tsx
import type { FC } from 'react';

interface PrincipleGroupIconProps {
  groupId: string;
  color: string;
  className?: string;
}

export const PrincipleGroupIcon: FC<PrincipleGroupIconProps> = ({
  groupId,
  color,
  className = 'w-10 h-10'
}) => {
  const icons: Record<string, JSX.Element> = {
    'protection': (
      // Shield icon
      <svg viewBox="0 0 48 48" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M24 4L6 12v12c0 11 8 18 18 20 10-2 18-9 18-20V12L24 4z" fill={color} opacity="0.2" stroke={color} strokeWidth="2" />
        <path d="M16 24l6 6 10-12" stroke={color} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    'lab-to-org': (
      // Connection/handoff icon
      <svg viewBox="0 0 48 48" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="24" r="8" fill={color} opacity="0.3" stroke={color} strokeWidth="2" />
        <circle cx="36" cy="24" r="8" fill={color} opacity="0.3" stroke={color} strokeWidth="2" />
        <path d="M20 24h8" stroke={color} strokeWidth="2" />
        <path d="M25 20l4 4-4 4" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    'incentives': (
      // Target/measurement icon
      <svg viewBox="0 0 48 48" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="24" cy="24" r="16" stroke={color} strokeWidth="2" opacity="0.3" />
        <circle cx="24" cy="24" r="10" stroke={color} strokeWidth="2" opacity="0.5" />
        <circle cx="24" cy="24" r="4" fill={color} />
      </svg>
    ),
    'culture': (
      // People/community icon
      <svg viewBox="0 0 48 48" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="24" cy="14" r="6" fill={color} opacity="0.7" />
        <circle cx="12" cy="20" r="5" fill={color} opacity="0.5" />
        <circle cx="36" cy="20" r="5" fill={color} opacity="0.5" />
        <path d="M8 40c0-8 7-12 16-12s16 4 16 12" stroke={color} strokeWidth="2" fill={color} opacity="0.2" />
      </svg>
    ),
    'resources': (
      // Talent/people with star icon
      <svg viewBox="0 0 48 48" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="20" cy="18" r="8" fill={color} opacity="0.3" stroke={color} strokeWidth="2" />
        <path d="M6 42c0-8 6-14 14-14s14 6 14 14" stroke={color} strokeWidth="2" />
        <path d="M36 12l2 4 4 1-3 3 1 4-4-2-4 2 1-4-3-3 4-1z" fill={color} />
      </svg>
    ),
    'speed': (
      // Fast forward / clock icon
      <svg viewBox="0 0 48 48" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="24" cy="24" r="16" stroke={color} strokeWidth="2" opacity="0.3" />
        <path d="M24 12v12l8 4" stroke={color} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M36 18l6 6-6 6" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  };

  return icons[groupId] || (
    <svg viewBox="0 0 48 48" className={className} fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="24" cy="24" r="16" stroke={color} strokeWidth="2" />
    </svg>
  );
};
```

**Step 2: Update DesignPrincipleCard to include icon**

```tsx
// app/src/components/DesignPrincipleCard.tsx
import type { DesignPrinciple, PrincipleGroup } from '../types/library';
import { PrincipleGroupIcon } from './PrincipleGroupIcon';
import { abbreviateInsight } from '../utils/abbreviateInsight';

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
          <PrincipleGroupIcon
            groupId={principle.group}
            color={groupColor}
            className="w-10 h-10"
          />
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
                isStarred
                  ? 'text-amber-500 hover:text-amber-600'
                  : 'text-gray-300 hover:text-gray-400'
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
          {keyPhrase && (
            <p className="text-xs text-gray-600 mb-2 italic">"{keyPhrase}"</p>
          )}

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
              Details
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
}

export function DesignPrincipleExpandedView({
  principle,
  group,
  isStarred,
  onToggleStar,
  onClose,
}: DesignPrincipleExpandedViewProps) {
  const groupColor = group?.color || '#94a3b8';

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b border-gray-200 p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <PrincipleGroupIcon
              groupId={principle.group}
              color={groupColor}
              className="w-10 h-10"
            />
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
        </div>
      </div>
    </div>
  );
}
```

**Step 3: Update PrincipleDeepDive to pass group to DesignPrincipleCard**

Check `app/src/components/PrincipleDeepDive.tsx` and ensure it passes the `group` prop to `DesignPrincipleCard`. This may require looking up the group from the library.

**Step 4: Verify and commit**

Run: `cd app && npm run build && npm run dev`
- Verify design principle cards show group icons and abbreviated insights

```bash
git add app/src/components/PrincipleGroupIcon.tsx app/src/components/DesignPrincipleCard.tsx
git commit -m "feat: add visual icons to design principle cards"
```

---

## Phase 2: Conversation Interface

### Task 5: Create API Service Layer

**Files:**
- Create: `app/src/services/ai.ts`
- Create: `app/src/services/config.ts`

**Step 1: Create config service for API keys**

```typescript
// app/src/services/config.ts

export interface AppConfig {
  anthropicApiKey: string | null;
  webSearchApiKey: string | null;
  webSearchApiUrl: string | null;
}

const CONFIG_KEY = 'orgtransformation-config';

export function getConfig(): AppConfig {
  const stored = localStorage.getItem(CONFIG_KEY);
  if (stored) {
    return JSON.parse(stored);
  }
  return {
    anthropicApiKey: null,
    webSearchApiKey: null,
    webSearchApiUrl: null,
  };
}

export function setConfig(config: Partial<AppConfig>): void {
  const current = getConfig();
  const updated = { ...current, ...config };
  localStorage.setItem(CONFIG_KEY, JSON.stringify(updated));
}

export function hasRequiredConfig(): boolean {
  const config = getConfig();
  return !!config.anthropicApiKey;
}
```

**Step 2: Create AI service**

```typescript
// app/src/services/ai.ts

import { getConfig } from './config';
import type { Case, DesignPrinciple, Conversation } from '../types/library';

interface AIResponse {
  answer: string;
  source: 'stored' | 'reasoning' | 'web-search';
  shouldPersist: boolean;
}

/**
 * 3-tier knowledge system:
 * 1. Check stored data (conversations, extendedContent)
 * 2. Use AI reasoning with context
 * 3. Fall back to web search if needed
 */
export async function askAboutCase(
  caseStudy: Case,
  question: string
): Promise<AIResponse> {
  // Tier 1: Check if we have a stored answer
  const existingConversation = caseStudy.conversations.find(
    (c) => c.question.toLowerCase() === question.toLowerCase()
  );
  if (existingConversation) {
    return {
      answer: existingConversation.answer,
      source: 'stored',
      shouldPersist: false,
    };
  }

  // Check extendedContent for relevant info
  const relevantExtended = Object.entries(caseStudy.extendedContent)
    .filter(([key]) =>
      key.toLowerCase().includes(question.toLowerCase().split(' ')[0])
    )
    .map(([, value]) => value)
    .join('\n');

  // Tier 2: AI reasoning with context
  const config = getConfig();
  if (!config.anthropicApiKey) {
    throw new Error('Anthropic API key not configured. Please set it in Settings.');
  }

  const context = buildCaseContext(caseStudy, relevantExtended);
  const aiResponse = await callClaude(config.anthropicApiKey, context, question);

  // Check if AI indicates it needs more information
  if (aiResponse.needsWebSearch && config.webSearchApiKey && config.webSearchApiUrl) {
    // Tier 3: Web search
    const searchResults = await performWebSearch(
      config.webSearchApiKey,
      config.webSearchApiUrl,
      `${caseStudy.company} AI transformation ${question}`
    );

    const enrichedResponse = await callClaude(
      config.anthropicApiKey,
      context + '\n\nAdditional research:\n' + searchResults,
      question
    );

    return {
      answer: enrichedResponse.answer,
      source: 'web-search',
      shouldPersist: true,
    };
  }

  return {
    answer: aiResponse.answer,
    source: 'reasoning',
    shouldPersist: aiResponse.isNewInfo,
  };
}

export async function askAboutPrinciple(
  principle: DesignPrinciple,
  question: string
): Promise<AIResponse> {
  // Similar implementation for principles
  const existingConversation = principle.conversations.find(
    (c) => c.question.toLowerCase() === question.toLowerCase()
  );
  if (existingConversation) {
    return {
      answer: existingConversation.answer,
      source: 'stored',
      shouldPersist: false,
    };
  }

  const config = getConfig();
  if (!config.anthropicApiKey) {
    throw new Error('Anthropic API key not configured. Please set it in Settings.');
  }

  const context = buildPrincipleContext(principle);
  const aiResponse = await callClaude(config.anthropicApiKey, context, question);

  if (aiResponse.needsWebSearch && config.webSearchApiKey && config.webSearchApiUrl) {
    const searchResults = await performWebSearch(
      config.webSearchApiKey,
      config.webSearchApiUrl,
      `${principle.title} organizational design ${question}`
    );

    const enrichedResponse = await callClaude(
      config.anthropicApiKey,
      context + '\n\nAdditional research:\n' + searchResults,
      question
    );

    return {
      answer: enrichedResponse.answer,
      source: 'web-search',
      shouldPersist: true,
    };
  }

  return {
    answer: aiResponse.answer,
    source: 'reasoning',
    shouldPersist: aiResponse.isNewInfo,
  };
}

function buildCaseContext(caseStudy: Case, extendedContent: string): string {
  return `
You are an expert on organizational AI transformation. You have deep knowledge about the following case study:

**Company:** ${caseStudy.company}
**Model:** ${caseStudy.title}

**What It Is:**
${caseStudy.content.whatItIs}

**How It Works:**
${caseStudy.content.howItWorks.map((h) => `- ${h}`).join('\n')}

**Core Insight:**
${caseStudy.content.coreInsight}

${caseStudy.content.keyMetrics ? `**Key Metrics:**\n${caseStudy.content.keyMetrics}` : ''}

**Sources:**
${caseStudy.content.sources.join(', ')}

${extendedContent ? `**Additional Context:**\n${extendedContent}` : ''}

Previous conversations about this case:
${caseStudy.conversations.map((c) => `Q: ${c.question}\nA: ${c.answer}`).join('\n\n')}
`.trim();
}

function buildPrincipleContext(principle: DesignPrinciple): string {
  return `
You are an expert on organizational design principles for AI transformation. You have deep knowledge about the following principle:

**Principle:** ${principle.title}

**Core Insight:**
${principle.insight}

**Manifestations:**
${principle.manifestations.map((m) => `- ${m}`).join('\n')}

**Diagnostic Test:**
${principle.test}

Previous conversations about this principle:
${principle.conversations.map((c) => `Q: ${c.question}\nA: ${c.answer}`).join('\n\n')}
`.trim();
}

interface ClaudeResponse {
  answer: string;
  needsWebSearch: boolean;
  isNewInfo: boolean;
}

async function callClaude(
  apiKey: string,
  context: string,
  question: string
): Promise<ClaudeResponse> {
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true',
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1024,
      system: `${context}

You are answering questions about this organizational case/principle. Be concise but thorough.

If you don't have enough information to answer the question well, respond with exactly:
"[NEEDS_RESEARCH] I need more current information to answer this accurately."

If you're providing information that goes beyond what's in the context (new insights, connections), start your response with "[NEW_INFO]" (this will be stripped from the final answer).

Otherwise, provide a helpful, specific answer based on the context provided.`,
      messages: [
        {
          role: 'user',
          content: question,
        },
      ],
    }),
  });

  if (!response.ok) {
    throw new Error(`Claude API error: ${response.statusText}`);
  }

  const data = await response.json();
  const content = data.content[0].text;

  if (content.startsWith('[NEEDS_RESEARCH]')) {
    return {
      answer: content.replace('[NEEDS_RESEARCH] ', ''),
      needsWebSearch: true,
      isNewInfo: false,
    };
  }

  if (content.startsWith('[NEW_INFO]')) {
    return {
      answer: content.replace('[NEW_INFO] ', ''),
      needsWebSearch: false,
      isNewInfo: true,
    };
  }

  return {
    answer: content,
    needsWebSearch: false,
    isNewInfo: false,
  };
}

async function performWebSearch(
  apiKey: string,
  apiUrl: string,
  query: string
): Promise<string> {
  // This is a placeholder - the actual implementation depends on the user's web search API
  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    throw new Error(`Web search error: ${response.statusText}`);
  }

  const data = await response.json();
  // Format depends on the specific API - this is a generic handler
  return typeof data.results === 'string'
    ? data.results
    : JSON.stringify(data.results, null, 2);
}
```

**Step 3: Commit**

```bash
git add app/src/services/config.ts app/src/services/ai.ts
git commit -m "feat: add AI service layer with 3-tier knowledge system"
```

---

### Task 6: Create Conversation Component

**Files:**
- Create: `app/src/components/ConversationPanel.tsx`

**Step 1: Create the conversation UI component**

```tsx
// app/src/components/ConversationPanel.tsx
import { useState } from 'react';
import type { Conversation } from '../types/library';

interface ConversationPanelProps {
  conversations: Conversation[];
  onAsk: (question: string) => Promise<void>;
  isLoading: boolean;
}

export function ConversationPanel({
  conversations,
  onAsk,
  isLoading,
}: ConversationPanelProps) {
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
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
        Ask a Question
      </h3>

      {/* Previous conversations */}
      {conversations.length > 0 && (
        <div className="space-y-4 mb-4 max-h-60 overflow-y-auto">
          {conversations.map((conv) => (
            <div key={conv.id} className="bg-gray-50 rounded-lg p-3">
              <p className="text-sm font-medium text-gray-700 mb-1">Q: {conv.question}</p>
              <p className="text-sm text-gray-600">{conv.answer}</p>
              {conv.source && (
                <p className="text-xs text-gray-400 mt-1">Source: {conv.source}</p>
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
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
          ) : (
            'Ask'
          )}
        </button>
      </form>
    </div>
  );
}
```

**Step 2: Commit**

```bash
git add app/src/components/ConversationPanel.tsx
git commit -m "feat: add ConversationPanel component for Q&A interface"
```

---

### Task 7: Integrate Conversation into Expanded Views

**Files:**
- Modify: `app/src/components/CaseCard.tsx`
- Create: `app/src/hooks/useConversation.ts`

**Step 1: Create useConversation hook**

```typescript
// app/src/hooks/useConversation.ts
import { useState, useCallback } from 'react';
import type { Conversation, Case, DesignPrinciple } from '../types/library';
import { askAboutCase, askAboutPrinciple } from '../services/ai';

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
  const [conversations, setConversations] = useState<Conversation[]>(
    caseStudy.conversations || []
  );
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const askQuestion = useCallback(async (question: string) => {
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

      if (response.shouldPersist && onConversationUpdate) {
        onConversationUpdate(updated);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  }, [caseStudy, conversations, onConversationUpdate]);

  return { conversations, isLoading, error, askQuestion };
}

export function usePrincipleConversation(
  principle: DesignPrinciple,
  onConversationUpdate?: (conversations: Conversation[]) => void
): UseConversationResult {
  const [conversations, setConversations] = useState<Conversation[]>(
    principle.conversations || []
  );
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const askQuestion = useCallback(async (question: string) => {
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

      if (response.shouldPersist && onConversationUpdate) {
        onConversationUpdate(updated);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  }, [principle, conversations, onConversationUpdate]);

  return { conversations, isLoading, error, askQuestion };
}
```

**Step 2: Update CaseExpandedView to include conversation**

Update `CaseExpandedView` in `app/src/components/CaseCard.tsx` to include the conversation panel:

```tsx
// Add to CaseCard.tsx - update CaseExpandedView

import { ConversationPanel } from './ConversationPanel';
import { useCaseConversation } from '../hooks/useConversation';

// Update props
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
        {/* ... existing header and content ... */}

        <div className="p-6 space-y-6">
          {/* ... existing content sections ... */}

          {/* Conversation panel at the bottom */}
          <ConversationPanel
            conversations={conversations}
            onAsk={askQuestion}
            isLoading={isLoading}
          />

          {error && (
            <p className="text-sm text-red-600 mt-2">{error}</p>
          )}
        </div>
      </div>
    </div>
  );
}
```

**Step 3: Similarly update DesignPrincipleExpandedView**

Add the same conversation capability to `DesignPrincipleExpandedView` in `app/src/components/DesignPrincipleCard.tsx`.

**Step 4: Commit**

```bash
git add app/src/hooks/useConversation.ts app/src/components/CaseCard.tsx app/src/components/DesignPrincipleCard.tsx
git commit -m "feat: integrate conversation interface into expanded views"
```

---

### Task 8: Create Settings Panel for API Keys

**Files:**
- Create: `app/src/components/SettingsPanel.tsx`
- Modify: `app/src/App.tsx`

**Step 1: Create SettingsPanel component**

```tsx
// app/src/components/SettingsPanel.tsx
import { useState, useEffect } from 'react';
import { getConfig, setConfig, type AppConfig } from '../services/config';

interface SettingsPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

export function SettingsPanel({ isOpen, onClose }: SettingsPanelProps) {
  const [config, setLocalConfig] = useState<AppConfig>(getConfig());
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setLocalConfig(getConfig());
      setSaved(false);
    }
  }, [isOpen]);

  const handleSave = () => {
    setConfig(config);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-md w-full p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900">Settings</h2>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 rounded"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Anthropic API Key
            </label>
            <input
              type="password"
              value={config.anthropicApiKey || ''}
              onChange={(e) => setLocalConfig({ ...config, anthropicApiKey: e.target.value })}
              placeholder="sk-ant-..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <p className="text-xs text-gray-500 mt-1">Required for AI-powered conversations</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Web Search API URL (Optional)
            </label>
            <input
              type="text"
              value={config.webSearchApiUrl || ''}
              onChange={(e) => setLocalConfig({ ...config, webSearchApiUrl: e.target.value })}
              placeholder="https://api.example.com/search"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Web Search API Key (Optional)
            </label>
            <input
              type="password"
              value={config.webSearchApiKey || ''}
              onChange={(e) => setLocalConfig({ ...config, webSearchApiKey: e.target.value })}
              placeholder="Your API key"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <p className="text-xs text-gray-500 mt-1">Enables web search fallback for unknown questions</p>
          </div>
        </div>

        <div className="mt-6 flex items-center justify-between">
          <button
            onClick={handleSave}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors"
          >
            Save Settings
          </button>
          {saved && (
            <span className="text-sm text-green-600">Saved!</span>
          )}
        </div>
      </div>
    </div>
  );
}
```

**Step 2: Add settings button to App.tsx**

Add a settings gear icon to the app header that opens the settings panel.

**Step 3: Commit**

```bash
git add app/src/components/SettingsPanel.tsx app/src/App.tsx
git commit -m "feat: add SettingsPanel for API key configuration"
```

---

### Task 9: Add Local Storage Persistence for Conversations

**Files:**
- Create: `app/src/services/persistence.ts`
- Modify: `app/src/hooks/useLibrary.ts`

**Step 1: Create persistence service**

```typescript
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
```

**Step 2: Update useLibrary to merge stored conversations**

Modify `useLibrary.ts` to merge localStorage conversations with the static JSON data.

**Step 3: Commit**

```bash
git add app/src/services/persistence.ts app/src/hooks/useLibrary.ts
git commit -m "feat: add localStorage persistence for conversations"
```

---

### Task 10: Final Integration & Testing

**Step 1: Build and type-check**

Run: `cd app && npm run build`
Expected: No errors

**Step 2: Manual testing checklist**

1. Open app at localhost:5173
2. Navigate to a principle deep dive (Locus of Innovation)
3. Verify:
   - [ ] Case cards show diagram icons
   - [ ] Case cards show abbreviated insights (3-5 words in quotes)
   - [ ] Full core insight only visible in expanded view
   - [ ] Design principle cards show group icons
   - [ ] Design principle cards show abbreviated insights
4. Click "Read More" on a case:
   - [ ] Expanded view shows diagram icon
   - [ ] Full core insight is displayed
   - [ ] Conversation panel is visible at bottom
   - [ ] Suggested questions are clickable
5. Configure API key in Settings:
   - [ ] Settings panel opens from gear icon
   - [ ] Can save Anthropic API key
   - [ ] Settings persist after page refresh
6. Ask a question about a case:
   - [ ] Question appears in conversation list
   - [ ] Loading spinner shows during API call
   - [ ] Answer appears from AI
   - [ ] Conversation persists after closing and reopening

**Step 3: Final commit**

```bash
git add -A
git commit -m "feat: complete Phase 2 - conversation interface with AI integration"
```

---

## Summary of Files Created/Modified

### Created:
- `app/src/components/DiagramIcon.tsx` - 9 SVG structural pattern diagrams
- `app/src/components/PrincipleGroupIcon.tsx` - 6 principle group icons
- `app/src/components/ConversationPanel.tsx` - Q&A interface
- `app/src/components/SettingsPanel.tsx` - API key configuration
- `app/src/utils/abbreviateInsight.ts` - Insight abbreviation utility
- `app/src/services/config.ts` - Configuration management
- `app/src/services/ai.ts` - 3-tier AI knowledge system
- `app/src/services/persistence.ts` - localStorage persistence
- `app/src/hooks/useConversation.ts` - Conversation state management

### Modified:
- `app/src/components/CaseCard.tsx` - Added diagram, abbreviated insight, conversation
- `app/src/components/DesignPrincipleCard.tsx` - Added icon, abbreviated insight, conversation
- `app/src/hooks/useLibrary.ts` - Merge stored conversations
- `app/src/App.tsx` - Settings button integration

---

**Plan complete and saved to `docs/plans/2026-01-19-case-visuals-and-conversation.md`. Ready to execute with `/superpowers-execute-plan`?**
