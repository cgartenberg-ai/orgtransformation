"use client";

import { useState, useMemo, useCallback, useEffect } from "react";
import Link from "next/link";
import type { PurposeClaim, ClaimType } from "@/lib/types/purpose-claims";
import {
  CLAIM_TYPE_LABELS,
  CLAIM_TYPE_COLORS,
  CLAIM_TYPES_ORDER,
  type SpecimenInfo,
} from "./claim-constants";
import { ClaimsHeatmap } from "./ClaimsHeatmap";
import { ClaimsDotMap } from "./ClaimsDotMap";

type ViewMode = "by-specimen" | "by-type" | "heatmap" | "dotmap";

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

const VIEW_MODES: { key: ViewMode; label: string }[] = [
  { key: "by-specimen", label: "By Specimen" },
  { key: "by-type", label: "By Type" },
  { key: "heatmap", label: "Heatmap" },
  { key: "dotmap", label: "Dot Map" },
];

export function PurposeClaimsBrowser({
  claims,
  claimTypeDefinitions,
  specimens,
  initialSpecimen = null,
}: {
  claims: PurposeClaim[];
  claimTypeDefinitions: Record<ClaimType, string>;
  specimens: SpecimenInfo[];
  initialSpecimen?: string | null;
}) {
  const [viewMode, setViewMode] = useState<ViewMode>(
    initialSpecimen ? "by-specimen" : "by-specimen"
  );
  const [selectedSpecimen, setSelectedSpecimen] = useState<string | null>(initialSpecimen);
  const [selectedType, setSelectedType] = useState<ClaimType | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [starredOnly, setStarredOnly] = useState(false);
  const { starred, toggle: toggleStar } = useStarredClaims();

  const isVizMode = viewMode === "heatmap" || viewMode === "dotmap";

  // Build specimen lookup
  const specimenMap = useMemo(() => {
    const map = new Map<string, SpecimenInfo>();
    for (const s of specimens) map.set(s.id, s);
    return map;
  }, [specimens]);

  // Specimens that have claims, sorted by count
  const specimensWithClaims = useMemo(() => {
    const counts = new Map<string, number>();
    for (const c of claims) {
      counts.set(c.specimenId, (counts.get(c.specimenId) || 0) + 1);
    }
    return Array.from(counts.entries())
      .map(([id, count]) => ({
        id,
        name: specimenMap.get(id)?.name || id,
        industry: specimenMap.get(id)?.industry || "",
        count,
      }))
      .sort((a, b) => b.count - a.count);
  }, [claims, specimenMap]);

  // Claim type counts
  const typeCounts = useMemo(() => {
    const counts = new Map<ClaimType, number>();
    for (const c of claims) {
      counts.set(c.claimType, (counts.get(c.claimType) || 0) + 1);
    }
    return counts;
  }, [claims]);

  // Filter claims
  const filteredClaims = useMemo(() => {
    return claims.filter((c) => {
      if (starredOnly && !starred.has(c.id)) return false;
      if (viewMode === "by-specimen" && selectedSpecimen && c.specimenId !== selectedSpecimen)
        return false;
      if (viewMode === "by-type" && selectedType && c.claimType !== selectedType) return false;
      if (searchQuery) {
        const q = searchQuery.toLowerCase();
        return (
          c.text.toLowerCase().includes(q) ||
          c.speaker.toLowerCase().includes(q) ||
          c.rhetoricalFunction.toLowerCase().includes(q) ||
          c.context.toLowerCase().includes(q)
        );
      }
      return true;
    });
  }, [claims, viewMode, selectedSpecimen, selectedType, searchQuery, starredOnly, starred]);

  // Group filtered claims by type (for by-specimen view)
  const claimsByType = useMemo(() => {
    if (viewMode !== "by-specimen") return null;
    const groups = new Map<ClaimType, PurposeClaim[]>();
    for (const c of filteredClaims) {
      const list = groups.get(c.claimType) || [];
      list.push(c);
      groups.set(c.claimType, list);
    }
    return CLAIM_TYPES_ORDER
      .filter((t) => groups.has(t))
      .map((t) => ({ type: t, claims: groups.get(t)! }));
  }, [filteredClaims, viewMode]);

  // Handlers for viz drill-down
  const handleHeatmapCellClick = useCallback((...args: [string, ClaimType]) => {
    setViewMode("by-specimen");
    setSelectedSpecimen(args[0]);
    setSelectedType(null);
    setSearchQuery("");
    setStarredOnly(false);
  }, []);

  const handleDotMapSpecimenClick = useCallback((specimenId: string) => {
    setViewMode("by-specimen");
    setSelectedSpecimen(specimenId);
    setSelectedType(null);
    setSearchQuery("");
    setStarredOnly(false);
  }, []);

  const switchViewMode = useCallback((mode: ViewMode) => {
    setViewMode(mode);
    if (mode === "by-specimen") {
      setSelectedType(null);
    } else if (mode === "by-type") {
      setSelectedSpecimen(null);
    }
    // heatmap/dotmap don't need clearing
  }, []);

  // Build specimens list for viz components (only those with claims)
  const specimensForViz = useMemo(() => {
    const withClaims = new Set(claims.map((c) => c.specimenId));
    return specimens.filter((s) => withClaims.has(s.id));
  }, [claims, specimens]);

  return (
    <div>
      {/* View mode toggle — always visible at top */}
      <div className="mb-6 flex rounded border border-sage-200 bg-cream-50">
        {VIEW_MODES.map((mode, i) => (
          <button
            key={mode.key}
            onClick={() => switchViewMode(mode.key)}
            className={`flex-1 px-3 py-2 text-xs font-medium transition-colors ${
              i === 0 ? "rounded-l" : ""
            } ${i === VIEW_MODES.length - 1 ? "rounded-r" : ""} ${
              viewMode === mode.key
                ? "bg-forest text-cream"
                : "text-charcoal-600 hover:bg-sage-100"
            }`}
          >
            {mode.label}
          </button>
        ))}
      </div>

      {/* Visualization views (full width, no sidebar) */}
      {viewMode === "heatmap" && (
        <ClaimsHeatmap
          claims={claims}
          specimens={specimensForViz}
          onCellClick={handleHeatmapCellClick}
        />
      )}

      {viewMode === "dotmap" && (
        <ClaimsDotMap
          claims={claims}
          specimens={specimensForViz}
          onSpecimenClick={handleDotMapSpecimenClick}
        />
      )}

      {/* Browser views (sidebar + content) */}
      {!isVizMode && (
        <div className="grid gap-8 lg:grid-cols-[260px_1fr]">
          {/* Sidebar */}
          <aside className="space-y-6">
            {/* Search */}
            <div>
              <label className="mb-1.5 block text-xs font-medium uppercase tracking-wide text-charcoal-400">
                Search
              </label>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search claims..."
                className="w-full rounded border border-sage-200 bg-cream-50 px-3 py-2 text-sm text-charcoal-700 placeholder:text-charcoal-300 focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest"
              />
            </div>

            {/* Starred filter */}
            <button
              onClick={() => setStarredOnly(!starredOnly)}
              className={`flex w-full items-center gap-2 rounded px-2 py-1.5 text-xs transition-colors ${
                starredOnly
                  ? "bg-amber-50 text-amber-700"
                  : "text-charcoal-400 hover:bg-sage-100"
              }`}
            >
              <span>{starredOnly ? "\u2605" : "\u2606"}</span>
              Starred only
              {starred.size > 0 && (
                <span className="opacity-60">({starred.size})</span>
              )}
            </button>

            {/* Specimen list (by-specimen view) */}
            {viewMode === "by-specimen" && (
              <div>
                <label className="mb-1.5 block text-xs font-medium uppercase tracking-wide text-charcoal-400">
                  Specimens ({specimensWithClaims.length})
                </label>
                <div className="max-h-[60vh] space-y-0.5 overflow-y-auto">
                  <button
                    onClick={() => setSelectedSpecimen(null)}
                    className={`w-full rounded px-2 py-1.5 text-left text-xs transition-colors ${
                      selectedSpecimen === null
                        ? "bg-forest text-cream"
                        : "text-charcoal-600 hover:bg-sage-100"
                    }`}
                  >
                    All specimens
                    <span className="ml-1 opacity-60">({claims.length})</span>
                  </button>
                  {specimensWithClaims.map((s) => (
                    <button
                      key={s.id}
                      onClick={() => setSelectedSpecimen(s.id)}
                      className={`w-full rounded px-2 py-1.5 text-left text-xs transition-colors ${
                        selectedSpecimen === s.id
                          ? "bg-forest text-cream"
                          : "text-charcoal-600 hover:bg-sage-100"
                      }`}
                    >
                      {s.name}
                      <span className="ml-1 opacity-60">({s.count})</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Type list (by-type view) */}
            {viewMode === "by-type" && (
              <div>
                <label className="mb-1.5 block text-xs font-medium uppercase tracking-wide text-charcoal-400">
                  Claim Types
                </label>
                <div className="space-y-1">
                  <button
                    onClick={() => setSelectedType(null)}
                    className={`w-full rounded px-2 py-1.5 text-left text-xs transition-colors ${
                      selectedType === null
                        ? "bg-forest text-cream"
                        : "text-charcoal-600 hover:bg-sage-100"
                    }`}
                  >
                    All types
                    <span className="ml-1 opacity-60">({claims.length})</span>
                  </button>
                  {CLAIM_TYPES_ORDER.map((type) => {
                    const count = typeCounts.get(type) || 0;
                    const colors = CLAIM_TYPE_COLORS[type];
                    return (
                      <button
                        key={type}
                        onClick={() => setSelectedType(selectedType === type ? null : type)}
                        className={`w-full rounded px-2 py-1.5 text-left text-xs transition-colors ${
                          selectedType === type
                            ? "bg-forest text-cream"
                            : "text-charcoal-600 hover:bg-sage-100"
                        }`}
                      >
                        <span className={`mr-1.5 inline-block rounded px-1 py-0.5 text-[10px] ${colors.bg} ${colors.text}`}>
                          {CLAIM_TYPE_LABELS[type]}
                        </span>
                        <span className="opacity-60">({count})</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {(searchQuery || selectedSpecimen || selectedType || starredOnly) && (
              <button
                onClick={() => {
                  setSearchQuery("");
                  setSelectedSpecimen(null);
                  setSelectedType(null);
                  setStarredOnly(false);
                }}
                className="text-xs text-charcoal-400 underline hover:text-forest"
              >
                Clear all filters
              </button>
            )}
          </aside>

          {/* Results */}
          <div>
            {/* Header context */}
            {viewMode === "by-specimen" && selectedSpecimen && (() => {
              const info = specimenMap.get(selectedSpecimen);
              return info ? (
                <div className="mb-6 rounded-xl border border-sage-200 bg-white p-5 shadow-sm">
                  <Link
                    href={`/specimens/${selectedSpecimen}`}
                    className="font-serif text-xl font-semibold text-forest hover:underline"
                  >
                    {info.name}
                  </Link>
                  <div className="mt-1 flex gap-2 text-xs text-charcoal-400">
                    {info.industry && <span>{info.industry}</span>}
                    {info.structuralModelName && (
                      <>
                        <span>&middot;</span>
                        <span>{info.structuralModelName}</span>
                      </>
                    )}
                  </div>
                </div>
              ) : null;
            })()}

            {viewMode === "by-type" && selectedType && (
              <div className="mb-6 rounded-xl border border-sage-200 bg-white p-5 shadow-sm">
                <div className="flex items-center gap-2">
                  <span className={`rounded px-2 py-1 text-xs font-medium ${CLAIM_TYPE_COLORS[selectedType].bg} ${CLAIM_TYPE_COLORS[selectedType].text}`}>
                    {CLAIM_TYPE_LABELS[selectedType]}
                  </span>
                </div>
                <p className="mt-2 text-sm text-charcoal-600">
                  {claimTypeDefinitions[selectedType]}
                </p>
              </div>
            )}

            <p className="mb-4 text-sm text-charcoal-500">
              {filteredClaims.length} claim{filteredClaims.length !== 1 ? "s" : ""}
              {searchQuery ? " matching search" : ""}
            </p>

            {/* Claims display */}
            {viewMode === "by-specimen" && claimsByType ? (
              <div className="space-y-8">
                {claimsByType.map(({ type, claims: typedClaims }) => (
                  <div key={type}>
                    <div className="mb-3 flex items-center gap-2">
                      <span className={`rounded px-2 py-0.5 text-xs font-medium ${CLAIM_TYPE_COLORS[type].bg} ${CLAIM_TYPE_COLORS[type].text}`}>
                        {CLAIM_TYPE_LABELS[type]}
                      </span>
                      <span className="text-xs text-charcoal-400">({typedClaims.length})</span>
                    </div>
                    <div className="space-y-3">
                      {typedClaims.map((claim) => (
                        <ClaimCard
                          key={claim.id}
                          claim={claim}
                          specimenMap={specimenMap}
                          showSpecimen={!selectedSpecimen}
                          isStarred={starred.has(claim.id)}
                          onToggleStar={() => toggleStar(claim.id)}
                        />
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : viewMode === "by-type" ? (
              <div className="space-y-3">
                {filteredClaims.map((claim) => (
                  <ClaimCard
                    key={claim.id}
                    claim={claim}
                    specimenMap={specimenMap}
                    showSpecimen={true}
                    isStarred={starred.has(claim.id)}
                    onToggleStar={() => toggleStar(claim.id)}
                  />
                ))}
              </div>
            ) : null}

            {!isVizMode && filteredClaims.length === 0 && (
              <p className="mt-8 text-center text-sm text-charcoal-400">
                No claims match the current filters.
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function ClaimCard({
  claim,
  specimenMap,
  showSpecimen,
  isStarred,
  onToggleStar,
}: {
  claim: PurposeClaim;
  specimenMap: Map<string, SpecimenInfo>;
  showSpecimen: boolean;
  isStarred: boolean;
  onToggleStar: () => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const colors = CLAIM_TYPE_COLORS[claim.claimType];
  const specimen = specimenMap.get(claim.specimenId);

  return (
    <div className={`rounded-lg border ${colors.border} border-l-4 bg-white p-4`}>
      <div className="flex items-start justify-between gap-3">
        <button
          onClick={onToggleStar}
          className={`mt-0.5 shrink-0 text-sm transition-colors ${
            isStarred ? "text-amber-500" : "text-charcoal-200 hover:text-amber-400"
          }`}
          title={isStarred ? "Unstar claim" : "Star claim"}
        >
          {isStarred ? "\u2605" : "\u2606"}
        </button>
        <div className="flex-1">
          {showSpecimen && specimen && (
            <Link
              href={`/specimens/${claim.specimenId}`}
              className="mb-1 block text-xs font-medium text-forest hover:underline"
            >
              {specimen.name}
            </Link>
          )}
          <p className="font-serif text-sm leading-relaxed text-charcoal-700 italic">
            &ldquo;{claim.text}&rdquo;
          </p>
          <p className="mt-2 text-xs text-charcoal-500">
            — {claim.speaker}, {claim.speakerTitle}
          </p>
        </div>
        <div className="shrink-0 text-right">
          <span className={`rounded px-1.5 py-0.5 text-[10px] font-medium ${colors.bg} ${colors.text}`}>
            {CLAIM_TYPE_LABELS[claim.claimType]}
          </span>
          <p className="mt-1 text-[10px] text-charcoal-300">{claim.sourceDate}</p>
        </div>
      </div>

      <p className="mt-2 text-xs leading-relaxed text-charcoal-500">
        {claim.rhetoricalFunction}
      </p>

      <div className="mt-2 flex items-center justify-between">
        <div className="flex items-center gap-2 text-[10px] text-charcoal-300">
          <span>{claim.sourceType}</span>
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
