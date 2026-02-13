"use client";

import { useState, useMemo } from "react";
import type { PurposeClaim, ClaimType, SpecimenEnrichment } from "@/lib/types/purpose-claims";
import { type SpecimenInfo } from "./claim-constants";
import { SpiderChart } from "@/components/visualizations/SpiderChart";
import {
  normalizeDistribution,
  averageDistributions,
  computeDistributionFromClaims,
} from "@/lib/utils/spider-data";

type GroupBy = "model" | "industry";

interface SpiderGroup {
  key: string;
  label: string;
  count: number;
  averageValues: Record<ClaimType, number>;
  specimens: {
    id: string;
    name: string;
    values: Record<ClaimType, number>;
    claimCount: number;
  }[];
}

export function ClaimsSpiderGrid({
  claims,
  specimens,
  enrichments = {},
  onSpecimenClick,
}: {
  claims: PurposeClaim[];
  specimens: SpecimenInfo[];
  enrichments?: Record<string, SpecimenEnrichment>;
  onSpecimenClick: (specimenId: string) => void;
}) {
  const [groupBy, setGroupBy] = useState<GroupBy>("model");
  const [hoveredSpecimen, setHoveredSpecimen] = useState<string | null>(null);

  // Build specimen lookup
  const specimenMap = useMemo(() => {
    const map = new Map<string, SpecimenInfo>();
    for (const s of specimens) map.set(s.id, s);
    return map;
  }, [specimens]);

  // Claims grouped by specimen
  const claimsBySpecimen = useMemo(() => {
    const groups = new Map<string, PurposeClaim[]>();
    for (const c of claims) {
      const list = groups.get(c.specimenId) || [];
      list.push(c);
      groups.set(c.specimenId, list);
    }
    return groups;
  }, [claims]);

  // Per-specimen distributions: both display-ready (normalized+rescaled) and raw counts
  const specimenDistributions = useMemo(() => {
    const dists = new Map<string, {
      values: Record<ClaimType, number>;      // normalized+rescaled for display
      rawDist: Partial<Record<ClaimType, number>>; // raw counts for averaging
      claimCount: number;
    }>();
    Array.from(claimsBySpecimen.entries()).forEach(([specId, specClaims]) => {
      // Use enrichment data if available, otherwise compute from claims
      const enrichment = enrichments[specId];
      const rawDist = enrichment?.claimTypeDistribution || computeDistributionFromClaims(specClaims);
      const claimCount = enrichment?.claimCount || specClaims.length;
      dists.set(specId, {
        values: normalizeDistribution(rawDist),
        rawDist,
        claimCount,
      });
    });
    return dists;
  }, [claimsBySpecimen, enrichments]);

  // Build grouped data
  const groups = useMemo((): SpiderGroup[] => {
    const groupMap = new Map<string, { label: string; specimenIds: string[] }>();

    for (const specId of Array.from(claimsBySpecimen.keys())) {
      const info = specimenMap.get(specId);
      if (!info) continue;

      let key: string;
      let label: string;

      if (groupBy === "model") {
        if (info.structuralModel == null) {
          key = "unclassified";
          label = "Unclassified";
        } else {
          key = `m${info.structuralModel}`;
          label = info.structuralModelName
            ? `M${info.structuralModel}: ${info.structuralModelName}`
            : `Model ${info.structuralModel}`;
        }
      } else {
        key = info.industry || "unknown";
        label = info.industry || "Unknown Industry";
      }

      const existing = groupMap.get(key);
      if (existing) {
        existing.specimenIds.push(specId);
      } else {
        groupMap.set(key, { label, specimenIds: [specId] });
      }
    }

    // Build SpiderGroup array, sorted by specimen count descending
    const result: SpiderGroup[] = [];
    Array.from(groupMap.entries()).forEach(([key, { label, specimenIds }]) => {
      const groupSpecimens = specimenIds
        .map((id: string) => {
          const dist = specimenDistributions.get(id);
          const info = specimenMap.get(id);
          return {
            id,
            name: info?.name || id,
            values: dist?.values || normalizeDistribution({}),
            claimCount: dist?.claimCount || 0,
          };
        })
        .sort((a: { claimCount: number }, b: { claimCount: number }) => b.claimCount - a.claimCount);

      // Collect raw distributions for averaging (not already-rescaled display values)
      const rawDists = specimenIds
        .map((id: string) => specimenDistributions.get(id)?.rawDist)
        .filter((d): d is Partial<Record<ClaimType, number>> => !!d);
      const averageValues = averageDistributions(rawDists);

      result.push({
        key,
        label,
        count: groupSpecimens.length,
        averageValues,
        specimens: groupSpecimens,
      });
    });

    return result.sort((a, b) => b.count - a.count);
  }, [claimsBySpecimen, specimenMap, specimenDistributions, groupBy]);

  return (
    <div>
      {/* Group by toggle */}
      <div className="mb-6 flex items-center gap-3">
        <span className="text-[10px] font-medium uppercase tracking-wide text-charcoal-400">
          Group by
        </span>
        <div className="flex rounded border border-sage-200 bg-cream-50">
          {(["model", "industry"] as const).map((mode) => (
            <button
              key={mode}
              onClick={() => setGroupBy(mode)}
              className={`px-3 py-1.5 text-xs font-medium transition-colors ${
                groupBy === mode
                  ? "bg-forest text-cream"
                  : "text-charcoal-600 hover:bg-sage-100"
              } ${mode === "model" ? "rounded-l" : "rounded-r"}`}
            >
              {mode === "model" ? "Structural Model" : "Industry"}
            </button>
          ))}
        </div>
      </div>

      {/* Spider groups */}
      <div className="space-y-10">
        {groups.map((group) => (
          <div key={group.key}>
            {/* Group header */}
            <div className="mb-4 flex items-center gap-2 border-b border-sage-200 pb-2">
              <h3 className="font-serif text-base font-medium text-forest">
                {group.label}
              </h3>
              <span className="text-xs text-charcoal-400">
                ({group.count} specimen{group.count !== 1 ? "s" : ""})
              </span>
            </div>

            {/* Grid: average + individuals */}
            <div className="flex flex-wrap items-start gap-6">
              {/* Average spider — larger */}
              <div className="flex flex-col items-center">
                <SpiderChart
                  values={group.averageValues}
                  size={180}
                  showLabels={true}
                  showGrid={true}
                  interactive={true}
                  fillColor="#8BA69B"
                  strokeColor="#8BA69B"
                />
                <span className="mt-1 text-[10px] font-medium text-charcoal-500">
                  Average
                </span>
              </div>

              {/* Individual specimen spiders — smaller grid */}
              <div className="flex flex-1 flex-wrap gap-3">
                {group.specimens.map((spec) => {
                  const isHovered = hoveredSpecimen === spec.id;
                  return (
                    <button
                      key={spec.id}
                      className={`flex flex-col items-center rounded-lg border p-2 transition-all ${
                        isHovered
                          ? "border-forest bg-forest-50/30 shadow-sm"
                          : "border-transparent hover:border-sage-200 hover:bg-cream-50"
                      }`}
                      onClick={() => onSpecimenClick(spec.id)}
                      onMouseEnter={() => setHoveredSpecimen(spec.id)}
                      onMouseLeave={() => setHoveredSpecimen(null)}
                      title={`${spec.name} — ${spec.claimCount} claims`}
                    >
                      <SpiderChart
                        values={spec.values}
                        comparison={isHovered ? { label: "avg", values: group.averageValues } : null}
                        size={100}
                        showLabels={false}
                        showGrid={false}
                        interactive={false}
                      />
                      <span className="mt-0.5 max-w-[100px] truncate text-[9px] text-charcoal-500">
                        {spec.name}
                      </span>
                      <span className="text-[8px] text-charcoal-300">
                        {spec.claimCount} claims
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Legend at bottom */}
      <div className="mt-8 flex items-center justify-center gap-6 border-t border-sage-100 pt-4">
        <div className="flex items-center gap-1.5">
          <div className="h-3 w-3 rounded-sm bg-forest/20 border border-forest/60" />
          <span className="text-[10px] text-charcoal-500">Specimen profile</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="h-3 w-3 rounded-sm bg-sage-400/10 border border-sage-400/60 border-dashed" />
          <span className="text-[10px] text-charcoal-500">Group average (hover)</span>
        </div>
      </div>
    </div>
  );
}
