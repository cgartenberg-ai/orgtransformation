"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import type { Specimen } from "@/lib/types/specimen";

const TENSION_LABELS: Record<string, [string, string]> = {
  structuralVsContextual: ["Structural", "Contextual"],
  speedVsDepth: ["Depth", "Speed"],
  centralVsDistributed: ["Central", "Distributed"],
  namedVsQuiet: ["Named", "Quiet"],
  longVsShortHorizon: ["Long horizon", "Short horizon"],
};

export function ComparisonView({
  allSpecimens,
}: {
  allSpecimens: Specimen[];
}) {
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [searchQuery, setSearchQuery] = useState("");

  const selected = useMemo(
    () => selectedIds.map((id) => allSpecimens.find((s) => s.id === id)!).filter(Boolean),
    [selectedIds, allSpecimens]
  );

  const searchResults = useMemo(() => {
    if (!searchQuery) return [];
    const q = searchQuery.toLowerCase();
    return allSpecimens
      .filter(
        (s) =>
          !selectedIds.includes(s.id) &&
          (s.name.toLowerCase().includes(q) ||
            s.habitat.industry.toLowerCase().includes(q))
      )
      .slice(0, 8);
  }, [searchQuery, allSpecimens, selectedIds]);

  const addSpecimen = (id: string) => {
    if (selectedIds.length < 4 && !selectedIds.includes(id)) {
      setSelectedIds([...selectedIds, id]);
      setSearchQuery("");
    }
  };

  const removeSpecimen = (id: string) => {
    setSelectedIds(selectedIds.filter((sid) => sid !== id));
  };

  return (
    <div className="space-y-6">
      {/* Specimen selector */}
      <div className="flex flex-wrap items-center gap-3">
        {selected.map((s) => (
          <div
            key={s.id}
            className="flex items-center gap-2 rounded-lg border border-sage-200 bg-cream-50 px-3 py-2"
          >
            <span className="font-serif text-sm font-medium text-forest">
              {s.name}
            </span>
            <button
              onClick={() => removeSpecimen(s.id)}
              className="text-xs text-charcoal-400 hover:text-red-500"
            >
              x
            </button>
          </div>
        ))}
        {selectedIds.length < 4 && (
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="+ Add specimen..."
              className="rounded border border-sage-200 bg-cream-50 px-3 py-2 text-sm text-charcoal-700 placeholder:text-charcoal-300 focus:border-forest focus:outline-none"
            />
            {searchResults.length > 0 && (
              <div className="absolute left-0 top-full z-10 mt-1 w-64 rounded-lg border border-sage-200 bg-cream-50 shadow-lg">
                {searchResults.map((s) => (
                  <button
                    key={s.id}
                    onClick={() => addSpecimen(s.id)}
                    className="block w-full px-3 py-2 text-left text-sm text-charcoal-700 hover:bg-sage-50"
                  >
                    <span className="font-medium">{s.name}</span>
                    <span className="ml-2 text-xs text-charcoal-400">
                      M{s.classification.structuralModel} &middot;{" "}
                      {s.habitat.industry}
                    </span>
                  </button>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {selected.length === 0 && (
        <p className="text-sm text-charcoal-400">
          Search and add up to 4 specimens to compare side-by-side.
        </p>
      )}

      {selected.length >= 2 && (
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            {/* Header: specimen names */}
            <thead>
              <tr>
                <th className="w-40 p-3 text-left text-xs font-medium uppercase tracking-wide text-charcoal-400" />
                {selected.map((s) => (
                  <th key={s.id} className="p-3 text-center">
                    <Link
                      href={`/specimens/${s.id}`}
                      className="font-serif text-sm font-semibold text-forest hover:underline"
                    >
                      {s.name}
                    </Link>
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {/* Classification */}
              <ComparisonSection label="Classification">
                <ComparisonRow label="Model" specimens={selected}>
                  {(s) => (
                    <span className="font-mono text-xs">
                      M{s.classification.structuralModel}
                      {s.classification.secondaryModel &&
                        ` + M${s.classification.secondaryModel}`}
                    </span>
                  )}
                </ComparisonRow>
                <ComparisonRow label="Orientation" specimens={selected}>
                  {(s) => (
                    <span className="text-xs">
                      {s.classification.orientation ?? "—"}
                    </span>
                  )}
                </ComparisonRow>
                <ComparisonRow label="Industry" specimens={selected}>
                  {(s) => (
                    <span className="text-xs">{s.habitat.industry}</span>
                  )}
                </ComparisonRow>
              </ComparisonSection>

              {/* Contingencies */}
              <ComparisonSection label="Contingencies">
                <ComparisonRow label="Regulatory" specimens={selected}>
                  {(s) => (
                    <ContingencyBadge value={s.contingencies.regulatoryIntensity} />
                  )}
                </ComparisonRow>
                <ComparisonRow label="Time to Obsolescence" specimens={selected}>
                  {(s) => (
                    <ContingencyBadge value={s.contingencies.timeToObsolescence} />
                  )}
                </ComparisonRow>
                <ComparisonRow label="CEO Tenure" specimens={selected}>
                  {(s) => (
                    <ContingencyBadge value={s.contingencies.ceoTenure} />
                  )}
                </ComparisonRow>
                <ComparisonRow label="Talent Position" specimens={selected}>
                  {(s) => (
                    <ContingencyBadge value={s.contingencies.talentMarketPosition} />
                  )}
                </ComparisonRow>
                <ComparisonRow label="Technical Debt" specimens={selected}>
                  {(s) => (
                    <ContingencyBadge value={s.contingencies.technicalDebt} />
                  )}
                </ComparisonRow>
              </ComparisonSection>

              {/* Tensions */}
              <ComparisonSection label="Tension Positions">
                {Object.entries(TENSION_LABELS).map(
                  ([field, [negLabel, posLabel]]) => (
                    <ComparisonRow
                      key={field}
                      label={`${negLabel} vs ${posLabel}`}
                      specimens={selected}
                    >
                      {(s) => {
                        const val =
                          s.tensionPositions[
                            field as keyof typeof s.tensionPositions
                          ];
                        if (val === null || val === undefined)
                          return <span className="text-xs text-charcoal-300">—</span>;
                        return <TensionBar value={val} negLabel={negLabel} posLabel={posLabel} />;
                      }}
                    </ComparisonRow>
                  )
                )}
              </ComparisonSection>

              {/* Mechanisms */}
              <ComparisonSection label="Principles">
                {(() => {
                  const allMechIds = Array.from(
                    new Set(
                      selected.flatMap((s) => s.mechanisms.map((m) => m.id))
                    )
                  ).sort((a, b) => a - b);
                  return allMechIds.map((mechId) => {
                    const mechName =
                      selected
                        .flatMap((s) => s.mechanisms)
                        .find((m) => m.id === mechId)?.name ?? `#${mechId}`;
                    return (
                      <ComparisonRow
                        key={mechId}
                        label={`#${mechId} ${mechName}`}
                        specimens={selected}
                      >
                        {(s) => {
                          const mech = s.mechanisms.find(
                            (m) => m.id === mechId
                          );
                          if (!mech)
                            return (
                              <span className="text-xs text-charcoal-300">
                                —
                              </span>
                            );
                          return (
                            <span
                              className={`rounded px-1.5 py-0.5 text-[10px] font-medium ${
                                mech.strength === "Strong"
                                  ? "bg-forest-50 text-forest"
                                  : mech.strength === "Moderate"
                                    ? "bg-sage-50 text-sage-700"
                                    : "bg-amber-50 text-amber-700"
                              }`}
                            >
                              {mech.strength}
                            </span>
                          );
                        }}
                      </ComparisonRow>
                    );
                  });
                })()}
              </ComparisonSection>
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

function ComparisonSection({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <>
      <tr>
        <td
          colSpan={99}
          className="border-t border-sage-200 bg-sage-50 px-3 py-2 text-xs font-medium uppercase tracking-wide text-charcoal-500"
        >
          {label}
        </td>
      </tr>
      {children}
    </>
  );
}

function ComparisonRow({
  label,
  specimens,
  children,
}: {
  label: string;
  specimens: Specimen[];
  children: (specimen: Specimen) => React.ReactNode;
}) {
  return (
    <tr className="border-t border-sage-100">
      <td className="p-3 text-xs text-charcoal-500">{label}</td>
      {specimens.map((s) => (
        <td key={s.id} className="p-3 text-center">
          {children(s)}
        </td>
      ))}
    </tr>
  );
}

function ContingencyBadge({ value }: { value: string | null }) {
  if (!value) return <span className="text-xs text-charcoal-300">—</span>;
  return (
    <span className="rounded bg-forest-50 px-1.5 py-0.5 font-mono text-[10px] text-forest">
      {value}
    </span>
  );
}

function TensionBar({
  value,
}: {
  value: number;
  negLabel: string;
  posLabel: string;
}) {
  // value is -1 to 1, map to 0-100%
  const pct = ((value + 1) / 2) * 100;

  return (
    <div className="flex items-center gap-1">
      <div className="relative h-3 w-20 rounded-full bg-sage-100">
        <div
          className="absolute top-0 h-3 w-2 rounded-full bg-forest"
          style={{ left: `calc(${pct}% - 4px)` }}
        />
      </div>
    </div>
  );
}
