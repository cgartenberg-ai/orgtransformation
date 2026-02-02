"use client";

import { useState, useMemo } from "react";
import { AnimatePresence } from "framer-motion";
import type { Specimen, StructuralModel, Orientation } from "@/lib/types/specimen";
import { STRUCTURAL_MODELS, ORIENTATIONS } from "@/lib/types/taxonomy";
import { SpecimenCard } from "./SpecimenCard";

export function SpecimenBrowser({
  specimens,
  industries,
  initialModel = null,
}: {
  specimens: Specimen[];
  industries: string[];
  initialModel?: StructuralModel | null;
}) {
  const [modelFilter, setModelFilter] = useState<StructuralModel | null>(initialModel);
  const [orientationFilter, setOrientationFilter] = useState<Orientation | null>(null);
  const [industryFilter, setIndustryFilter] = useState<string | null>(null);
  const [completenessFilter, setCompletenessFilter] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  const filtered = useMemo(() => {
    return specimens.filter((s) => {
      if (s.meta.status === "Archived") return false;
      if (modelFilter && s.classification.structuralModel !== modelFilter) return false;
      if (orientationFilter && s.classification.orientation !== orientationFilter) return false;
      if (industryFilter && s.habitat.industry !== industryFilter) return false;
      if (completenessFilter && s.meta.completeness !== completenessFilter) return false;
      if (searchQuery) {
        const q = searchQuery.toLowerCase();
        return (
          s.name.toLowerCase().includes(q) ||
          s.title.toLowerCase().includes(q) ||
          s.description.toLowerCase().includes(q) ||
          s.habitat.industry.toLowerCase().includes(q)
        );
      }
      return true;
    });
  }, [specimens, modelFilter, orientationFilter, industryFilter, completenessFilter, searchQuery]);

  const hasFilters = modelFilter || orientationFilter || industryFilter || completenessFilter || searchQuery;

  return (
    <div className="mt-6 grid gap-8 lg:grid-cols-[260px_1fr]">
      {/* Sidebar filters */}
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
            placeholder="Search specimens..."
            className="w-full rounded border border-sage-200 bg-cream-50 px-3 py-2 text-sm text-charcoal-700 placeholder:text-charcoal-300 focus:border-forest focus:outline-none focus:ring-1 focus:ring-forest"
          />
        </div>

        {/* Structural Model */}
        <FilterGroup label="Structural Model">
          <FilterButton
            active={modelFilter === null}
            onClick={() => setModelFilter(null)}
          >
            All
          </FilterButton>
          {([1, 2, 3, 4, 5, 6, 7] as StructuralModel[]).map((m) => (
            <FilterButton
              key={m}
              active={modelFilter === m}
              onClick={() => setModelFilter(modelFilter === m ? null : m)}
            >
              M{m}: {STRUCTURAL_MODELS[m].name}
            </FilterButton>
          ))}
        </FilterGroup>

        {/* Orientation */}
        <FilterGroup label="Orientation">
          <FilterButton
            active={orientationFilter === null}
            onClick={() => setOrientationFilter(null)}
          >
            All
          </FilterButton>
          {ORIENTATIONS.map((o) => (
            <FilterButton
              key={o}
              active={orientationFilter === o}
              onClick={() =>
                setOrientationFilter(orientationFilter === o ? null : o)
              }
            >
              {o}
            </FilterButton>
          ))}
        </FilterGroup>

        {/* Industry */}
        <FilterGroup label="Industry">
          <select
            value={industryFilter ?? ""}
            onChange={(e) =>
              setIndustryFilter(e.target.value || null)
            }
            className="w-full rounded border border-sage-200 bg-cream-50 px-2 py-1.5 text-sm text-charcoal-700 focus:border-forest focus:outline-none"
          >
            <option value="">All industries</option>
            {industries.map((ind) => (
              <option key={ind} value={ind}>
                {ind}
              </option>
            ))}
          </select>
        </FilterGroup>

        {/* Completeness */}
        <FilterGroup label="Completeness">
          <FilterButton
            active={completenessFilter === null}
            onClick={() => setCompletenessFilter(null)}
          >
            All
          </FilterButton>
          {["High", "Medium", "Low"].map((c) => (
            <FilterButton
              key={c}
              active={completenessFilter === c}
              onClick={() =>
                setCompletenessFilter(completenessFilter === c ? null : c)
              }
            >
              {c}
            </FilterButton>
          ))}
        </FilterGroup>

        {hasFilters && (
          <button
            onClick={() => {
              setModelFilter(null);
              setOrientationFilter(null);
              setIndustryFilter(null);
              setCompletenessFilter(null);
              setSearchQuery("");
            }}
            className="text-xs text-charcoal-400 underline hover:text-forest"
          >
            Clear all filters
          </button>
        )}
      </aside>

      {/* Results */}
      <div>
        {modelFilter && (
          <div className="mb-6 rounded-xl border border-sage-200 bg-white p-6 shadow-sm">
            <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-sage-500">
              {STRUCTURAL_MODELS[modelFilter].shortName}
            </p>
            <h2 className="mt-1 font-serif text-xl font-semibold text-forest">
              {STRUCTURAL_MODELS[modelFilter].name}
            </h2>
            <p className="mt-2 text-sm leading-relaxed text-charcoal-600">
              {STRUCTURAL_MODELS[modelFilter].characteristics}
            </p>
          </div>
        )}
        <p className="mb-4 text-sm text-charcoal-500">
          {filtered.length} specimen{filtered.length !== 1 ? "s" : ""}
          {hasFilters ? " matching filters" : ""}
        </p>
        <AnimatePresence mode="popLayout">
          <div className="grid gap-4 md:grid-cols-2">
            {filtered.map((s) => (
              <SpecimenCard key={s.id} specimen={s} />
            ))}
          </div>
        </AnimatePresence>
        {filtered.length === 0 && (
          <p className="mt-8 text-center text-sm text-charcoal-400">
            No specimens match the current filters.
          </p>
        )}
      </div>
    </div>
  );
}

function FilterGroup({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <label className="mb-1.5 block text-xs font-medium uppercase tracking-wide text-charcoal-400">
        {label}
      </label>
      <div className="flex flex-wrap gap-1.5">{children}</div>
    </div>
  );
}

function FilterButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      className={`rounded px-2 py-1 text-xs transition-colors ${
        active
          ? "bg-forest text-cream"
          : "bg-cream-50 text-charcoal-600 hover:bg-sage-100"
      }`}
    >
      {children}
    </button>
  );
}
