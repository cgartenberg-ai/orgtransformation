"use client";

import { useState, useMemo } from "react";
import type { PurposeClaim, ClaimType } from "@/lib/types/purpose-claims";
import {
  CLAIM_TYPE_LABELS,
  CLAIM_TYPE_COLORS,
  CLAIM_TYPES_ORDER,
  type SpecimenInfo,
} from "./claim-constants";

type GroupBy = "model" | "industry";

/**
 * Specimen Dot Map: each specimen as a mini stacked horizontal bar
 * showing claim-type proportions. Grouped by model or industry.
 */
export function ClaimsDotMap({
  claims,
  specimens,
  onSpecimenClick,
}: {
  claims: PurposeClaim[];
  specimens: SpecimenInfo[];
  onSpecimenClick: (specimenId: string) => void;
}) {
  const [groupBy, setGroupBy] = useState<GroupBy>("model");
  const [hoveredSpecimen, setHoveredSpecimen] = useState<string | null>(null);

  // Build per-specimen distributions
  const distributions = useMemo(() => {
    const dist = new Map<string, Map<ClaimType, number>>();
    const totals = new Map<string, number>();

    for (const c of claims) {
      if (!dist.has(c.specimenId)) dist.set(c.specimenId, new Map());
      const row = dist.get(c.specimenId)!;
      row.set(c.claimType, (row.get(c.claimType) || 0) + 1);
      totals.set(c.specimenId, (totals.get(c.specimenId) || 0) + 1);
    }

    return { dist, totals };
  }, [claims]);

  // Group specimens
  const groups = useMemo(() => {
    const grouped = new Map<string, SpecimenInfo[]>();

    for (const s of specimens) {
      if (!distributions.totals.has(s.id)) continue;

      let key: string;
      if (groupBy === "model") {
        key = s.structuralModel != null
          ? `M${s.structuralModel}: ${s.structuralModelName || "Unknown"}`
          : "Unclassified";
      } else {
        key = s.industry || "Unknown";
      }

      const list = grouped.get(key) || [];
      list.push(s);
      grouped.set(key, list);
    }

    return Array.from(grouped.entries())
      .sort((a, b) => a[0].localeCompare(b[0]))
      .map(([label, specs]) => ({
        label,
        specimens: specs.sort(
          (a, b) => (distributions.totals.get(b.id) || 0) - (distributions.totals.get(a.id) || 0)
        ),
        total: specs.reduce((sum, s) => sum + (distributions.totals.get(s.id) || 0), 0),
      }));
  }, [specimens, distributions, groupBy]);

  return (
    <div>
      {/* Group by toggle */}
      <div className="mb-6 flex items-center gap-4">
        <span className="text-xs font-medium uppercase tracking-wide text-charcoal-400">
          Group by
        </span>
        <div className="flex rounded border border-sage-200 bg-cream-50">
          <button
            onClick={() => setGroupBy("model")}
            className={`rounded-l px-3 py-1.5 text-xs font-medium transition-colors ${
              groupBy === "model"
                ? "bg-forest text-cream"
                : "text-charcoal-600 hover:bg-sage-100"
            }`}
          >
            Structural Model
          </button>
          <button
            onClick={() => setGroupBy("industry")}
            className={`rounded-r px-3 py-1.5 text-xs font-medium transition-colors ${
              groupBy === "industry"
                ? "bg-forest text-cream"
                : "text-charcoal-600 hover:bg-sage-100"
            }`}
          >
            Industry
          </button>
        </div>
      </div>

      {/* Legend */}
      <div className="mb-4 flex flex-wrap gap-3">
        {CLAIM_TYPES_ORDER.map((type) => (
          <div key={type} className="flex items-center gap-1">
            <div
              className="h-3 w-3 rounded-sm"
              style={{ backgroundColor: CLAIM_TYPE_COLORS[type].hex }}
            />
            <span className="text-[10px] text-charcoal-500">{CLAIM_TYPE_LABELS[type]}</span>
          </div>
        ))}
      </div>

      {/* Groups */}
      <div className="space-y-6">
        {groups.map((group) => (
          <div key={group.label}>
            {/* Group header */}
            <div className="mb-2 flex items-baseline gap-2">
              <span className="text-sm font-semibold text-charcoal-700">
                {group.label}
              </span>
              <span className="text-xs text-charcoal-400">
                {group.total} claims
              </span>
            </div>

            {/* Specimen bars */}
            <div className="space-y-1.5">
              {group.specimens.map((specimen) => {
                const dist = distributions.dist.get(specimen.id);
                const total = distributions.totals.get(specimen.id) || 0;
                const isHovered = hoveredSpecimen === specimen.id;

                return (
                  <div
                    key={specimen.id}
                    className="group flex items-center gap-3"
                    onMouseEnter={() => setHoveredSpecimen(specimen.id)}
                    onMouseLeave={() => setHoveredSpecimen(null)}
                  >
                    {/* Specimen name + complementary tag */}
                    <div className="flex w-[180px] shrink-0 items-baseline justify-end gap-1">
                      <span className="shrink-0 text-[9px] text-charcoal-300">
                        {groupBy === "model"
                          ? specimen.industry
                          : specimen.structuralModel != null
                            ? `M${specimen.structuralModel}`
                            : ""}
                      </span>
                      <button
                        onClick={() => onSpecimenClick(specimen.id)}
                        className="truncate text-right text-xs text-charcoal-600 hover:text-forest hover:underline"
                        title={specimen.name}
                      >
                        {specimen.name}
                      </button>
                    </div>

                    {/* Stacked bar */}
                    <div className="relative flex h-6 flex-1 overflow-hidden rounded">
                      {CLAIM_TYPES_ORDER.map((type) => {
                        const count = dist?.get(type) || 0;
                        if (count === 0) return null;
                        const pct = (count / total) * 100;

                        return (
                          <div
                            key={type}
                            className="flex items-center justify-center transition-all"
                            style={{
                              width: `${pct}%`,
                              backgroundColor: CLAIM_TYPE_COLORS[type].hex,
                              opacity: isHovered ? 1 : 0.7,
                            }}
                            title={`${CLAIM_TYPE_LABELS[type]}: ${count}`}
                          >
                            {pct > 8 && (
                              <span className="text-[9px] font-medium text-white" style={{ textShadow: "0 0 2px rgba(0,0,0,0.3)" }}>
                                {count}
                              </span>
                            )}
                          </div>
                        );
                      })}
                    </div>

                    {/* Total */}
                    <span className="w-8 shrink-0 text-right text-xs font-medium text-charcoal-500">
                      {total}
                    </span>
                  </div>
                );
              })}
            </div>

            {/* Tooltip for hovered specimen */}
            {hoveredSpecimen && group.specimens.some((s) => s.id === hoveredSpecimen) && (() => {
              const spec = group.specimens.find((s) => s.id === hoveredSpecimen);
              const dist = distributions.dist.get(hoveredSpecimen);
              if (!spec || !dist) return null;

              return (
                <div className="mt-2 rounded border border-sage-200 bg-white p-3 shadow-sm">
                  <p className="text-xs font-semibold text-charcoal-700">{spec.name}</p>
                  <p className="text-[10px] text-charcoal-400">
                    {spec.industry} &middot; {spec.structuralModelName || `M${spec.structuralModel}`}
                  </p>
                  <div className="mt-2 flex flex-wrap gap-2">
                    {CLAIM_TYPES_ORDER.map((type) => {
                      const count = dist.get(type) || 0;
                      if (count === 0) return null;
                      return (
                        <span
                          key={type}
                          className={`rounded px-1.5 py-0.5 text-[10px] font-medium ${CLAIM_TYPE_COLORS[type].bg} ${CLAIM_TYPE_COLORS[type].text}`}
                        >
                          {CLAIM_TYPE_LABELS[type]}: {count}
                        </span>
                      );
                    })}
                  </div>
                </div>
              );
            })()}
          </div>
        ))}
      </div>
    </div>
  );
}
