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
 * Heatmap matrix: specimens (rows, grouped by structural model OR industry) × claim types (columns).
 * Cell intensity shows claim count. Click a cell to drill into those claims.
 */
export function ClaimsHeatmap({
  claims,
  specimens,
  onCellClick,
}: {
  claims: PurposeClaim[];
  specimens: SpecimenInfo[];
  onCellClick: (specimenId: string, claimType: ClaimType) => void;
}) {
  const [groupBy, setGroupBy] = useState<GroupBy>("model");
  // Build count matrix: specimenId → claimType → count
  const { matrix, specimenTotals, typeTotals, grandTotal } = useMemo(() => {
    const m = new Map<string, Map<ClaimType, number>>();
    const sTotals = new Map<string, number>();
    const tTotals = new Map<ClaimType, number>();
    let total = 0;

    for (const c of claims) {
      if (!m.has(c.specimenId)) m.set(c.specimenId, new Map());
      const row = m.get(c.specimenId)!;
      row.set(c.claimType, (row.get(c.claimType) || 0) + 1);
      sTotals.set(c.specimenId, (sTotals.get(c.specimenId) || 0) + 1);
      tTotals.set(c.claimType, (tTotals.get(c.claimType) || 0) + 1);
      total++;
    }

    return { matrix: m, specimenTotals: sTotals, typeTotals: tTotals, grandTotal: total };
  }, [claims]);

  // Group specimens by structural model or industry
  const specimenGroups = useMemo(() => {
    const groups = new Map<string, SpecimenInfo[]>();
    for (const s of specimens) {
      if (!matrix.has(s.id)) continue; // skip specimens with no claims

      let key: string;
      if (groupBy === "model") {
        key = s.structuralModel != null
          ? `M${s.structuralModel}: ${s.structuralModelName || "Unknown"}`
          : "Unclassified";
      } else {
        key = s.industry || "Unknown";
      }

      const list = groups.get(key) || [];
      list.push(s);
      groups.set(key, list);
    }
    // Sort groups alphabetically, specimens within by total claims desc
    return Array.from(groups.entries())
      .sort((a, b) => a[0].localeCompare(b[0]))
      .map(([label, specs]) => ({
        label,
        specimens: specs.sort(
          (a, b) => (specimenTotals.get(b.id) || 0) - (specimenTotals.get(a.id) || 0)
        ),
      }));
  }, [specimens, matrix, specimenTotals, groupBy]);

  function cellOpacity(count: number): number {
    if (count === 0) return 0;
    if (count === 1) return 0.2;
    if (count <= 3) return 0.4;
    if (count <= 5) return 0.6;
    return 0.8;
  }

  return (
    <div className="overflow-x-auto">
      <div className="min-w-[800px]">
        {/* Group by toggle */}
        <div className="mb-4 flex items-center gap-4">
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

        {/* Column headers */}
        <div className="mb-1 grid" style={{ gridTemplateColumns: "200px repeat(7, 1fr) 50px" }}>
          <div className="px-2 py-1 text-[10px] font-medium uppercase tracking-wide text-charcoal-400">
            Specimen
          </div>
          {CLAIM_TYPES_ORDER.map((type) => (
            <div
              key={type}
              className="px-1 py-1 text-center"
            >
              <span className={`inline-block rounded px-1.5 py-0.5 text-[9px] font-medium ${CLAIM_TYPE_COLORS[type].bg} ${CLAIM_TYPE_COLORS[type].text}`}>
                {CLAIM_TYPE_LABELS[type]}
              </span>
            </div>
          ))}
          <div className="px-1 py-1 text-center text-[10px] font-medium text-charcoal-400">
            Total
          </div>
        </div>

        {/* Rows grouped by model */}
        {specimenGroups.map((group) => (
          <div key={group.label} className="mb-4">
            {/* Group header */}
            <div className="mb-1 rounded bg-sage-50 px-2 py-1.5 text-[11px] font-semibold text-sage-700">
              {group.label}
              <span className="ml-2 font-normal text-sage-500">
                ({group.specimens.length} specimen{group.specimens.length !== 1 ? "s" : ""})
              </span>
            </div>

            {/* Specimen rows */}
            {group.specimens.map((specimen) => {
              const row = matrix.get(specimen.id);
              const total = specimenTotals.get(specimen.id) || 0;

              return (
                <div
                  key={specimen.id}
                  className="grid items-center border-b border-sage-100"
                  style={{ gridTemplateColumns: "200px repeat(7, 1fr) 50px" }}
                >
                  {/* Specimen label */}
                  <div className="flex items-baseline gap-1.5 px-2 py-2">
                    <span className="truncate text-xs font-medium text-charcoal-700">
                      {specimen.name}
                    </span>
                    <span className="shrink-0 text-[9px] text-charcoal-300">
                      {groupBy === "model"
                        ? specimen.industry
                        : specimen.structuralModel != null
                          ? `M${specimen.structuralModel}`
                          : ""}
                    </span>
                  </div>

                  {/* Cells */}
                  {CLAIM_TYPES_ORDER.map((type) => {
                    const count = row?.get(type) || 0;
                    const opacity = cellOpacity(count);
                    const hex = CLAIM_TYPE_COLORS[type].hex;

                    return (
                      <button
                        key={type}
                        onClick={() => count > 0 && onCellClick(specimen.id, type)}
                        className={`mx-0.5 my-1 flex h-8 items-center justify-center rounded text-[10px] font-medium transition-all ${
                          count > 0
                            ? "cursor-pointer hover:ring-1 hover:ring-charcoal-300"
                            : "cursor-default"
                        }`}
                        style={{
                          backgroundColor: count > 0 ? hex : "transparent",
                          opacity: count > 0 ? undefined : 1,
                          ...(count > 0 ? { opacity } : {}),
                        }}
                        title={count > 0 ? `${specimen.name}: ${count} ${CLAIM_TYPE_LABELS[type]} claim${count !== 1 ? "s" : ""}` : ""}
                      >
                        {count > 0 && (
                          <span className="font-semibold text-white" style={{ textShadow: "0 0 3px rgba(0,0,0,0.3)" }}>
                            {count}
                          </span>
                        )}
                      </button>
                    );
                  })}

                  {/* Row total */}
                  <div className="px-1 py-2 text-center text-xs font-semibold text-charcoal-600">
                    {total}
                  </div>
                </div>
              );
            })}
          </div>
        ))}

        {/* Column totals */}
        <div
          className="mt-2 grid items-center border-t-2 border-sage-300 pt-2"
          style={{ gridTemplateColumns: "200px repeat(7, 1fr) 50px" }}
        >
          <div className="px-2 text-xs font-semibold text-charcoal-600">
            Total
          </div>
          {CLAIM_TYPES_ORDER.map((type) => (
            <div key={type} className="text-center text-xs font-semibold text-charcoal-600">
              {typeTotals.get(type) || 0}
            </div>
          ))}
          <div className="text-center text-xs font-bold text-forest">
            {grandTotal}
          </div>
        </div>
      </div>
    </div>
  );
}
