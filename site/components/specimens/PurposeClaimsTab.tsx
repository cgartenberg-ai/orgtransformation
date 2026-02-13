"use client";

import { useState, useCallback, useEffect } from "react";
import Link from "next/link";
import type { PurposeClaim, ClaimType, SpecimenEnrichment } from "@/lib/types/purpose-claims";
import { EnrichmentSummary } from "./EnrichmentSummary";
import {
  CLAIM_TYPE_LABELS,
  CLAIM_TYPE_COLORS,
  CLAIM_TYPES_ORDER,
} from "@/components/purpose-claims/claim-constants";

const STORAGE_KEY = "purpose-claims-starred";

function useStarredClaims() {
  const [starred, setStarred] = useState<Set<string>>(new Set());

  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) setStarred(new Set(JSON.parse(stored)));
    } catch {}
  }, []);

  const toggle = useCallback((claimId: string) => {
    setStarred((prev) => {
      const next = new Set(prev);
      if (next.has(claimId)) next.delete(claimId);
      else next.add(claimId);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(Array.from(next)));
      return next;
    });
  }, []);

  return { starred, toggle };
}

export function PurposeClaimsTab({
  claims,
  claimTypeDefinitions,
  specimenId,
  enrichment = null,
}: {
  claims: PurposeClaim[];
  claimTypeDefinitions: Record<ClaimType, string>;
  specimenId: string;
  enrichment?: SpecimenEnrichment | null;
}) {
  const { starred, toggle: toggleStar } = useStarredClaims();

  if (claims.length === 0) {
    return (
      <div className="rounded-lg border border-sage-200 bg-cream-50 p-6 text-center">
        <p className="text-sm text-charcoal-400">
          No purpose claims collected yet for this specimen.
        </p>
      </div>
    );
  }

  // Group by type
  const grouped = new Map<ClaimType, PurposeClaim[]>();
  for (const c of claims) {
    const list = grouped.get(c.claimType) || [];
    list.push(c);
    grouped.set(c.claimType, list);
  }

  const speakers = new Set(claims.map((c) => c.speaker)).size;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <p className="text-sm text-charcoal-500">
          {claims.length} claim{claims.length !== 1 ? "s" : ""} from{" "}
          {speakers} speaker{speakers !== 1 ? "s" : ""}
        </p>
        <Link
          href={`/purpose-claims?specimen=${specimenId}`}
          className="text-xs text-charcoal-400 hover:text-forest"
        >
          View in full browser &rarr;
        </Link>
      </div>

      {enrichment && (
        <EnrichmentSummary enrichment={enrichment} specimenId={specimenId} />
      )}

      {CLAIM_TYPES_ORDER.filter((t) => grouped.has(t)).map((type) => {
        const typeClaims = grouped.get(type)!;
        const colors = CLAIM_TYPE_COLORS[type];
        return (
          <div key={type}>
            <div className="mb-3 flex items-center gap-2">
              <span className={`rounded px-2 py-0.5 text-xs font-medium ${colors.bg} ${colors.text}`}>
                {CLAIM_TYPE_LABELS[type]}
              </span>
              <span className="text-xs text-charcoal-400">({typeClaims.length})</span>
            </div>
            <p className="mb-3 text-[11px] text-charcoal-400">
              {claimTypeDefinitions[type]}
            </p>
            <div className="space-y-3">
              {typeClaims.map((claim) => (
                <TabClaimCard
                  key={claim.id}
                  claim={claim}
                  colors={colors}
                  isStarred={starred.has(claim.id)}
                  onToggleStar={() => toggleStar(claim.id)}
                />
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function TabClaimCard({
  claim,
  colors,
  isStarred,
  onToggleStar,
}: {
  claim: PurposeClaim;
  colors: { bg: string; text: string; border: string };
  isStarred: boolean;
  onToggleStar: () => void;
}) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className={`rounded-lg border ${colors.border} border-l-4 bg-white p-4`}>
      <div className="flex items-start gap-2">
        <button
          onClick={onToggleStar}
          className={`mt-0.5 shrink-0 text-sm transition-colors ${
            isStarred ? "text-amber-500" : "text-charcoal-200 hover:text-amber-400"
          }`}
          title={isStarred ? "Unstar claim" : "Star claim"}
        >
          {isStarred ? "\u2605" : "\u2606"}
        </button>
        <p className="font-serif text-sm leading-relaxed text-charcoal-700 italic">
          &ldquo;{claim.text}&rdquo;
        </p>
      </div>
      <p className="mt-2 text-xs text-charcoal-500">
        — {claim.speaker}, {claim.speakerTitle}
      </p>
      <p className="mt-2 text-xs leading-relaxed text-charcoal-500">
        {claim.rhetoricalFunction}
      </p>
      <div className="mt-2 flex items-center justify-between">
        <div className="flex items-center gap-2 text-[10px] text-charcoal-300">
          <span>{claim.sourceType}</span>
          <span>&middot;</span>
          <span>{claim.sourceDate}</span>
          <span>&middot;</span>
          <a
            href={claim.sourceUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-forest"
          >
            Source &#8599;
          </a>
        </div>
        {claim.notes && (
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-[10px] text-charcoal-300 hover:text-forest"
          >
            {expanded ? "Hide notes" : "Notes"}
          </button>
        )}
      </div>
      {expanded && claim.notes && (
        <p className="mt-2 rounded bg-cream-50 px-2 py-1.5 text-[11px] text-charcoal-500">
          {claim.notes}
        </p>
      )}
    </div>
  );
}
