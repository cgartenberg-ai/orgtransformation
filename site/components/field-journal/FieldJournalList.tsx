"use client";

import { useState } from "react";
import type { FieldJournalEntry, FieldJournalTrack } from "@/lib/data/field-journal";
import { FieldJournalCard } from "./FieldJournalCard";

type Filter = "all" | "insights" | FieldJournalTrack;

const filters: { value: Filter; label: string }[] = [
  { value: "all", label: "All" },
  { value: "insights", label: "Insights Only" },
  { value: "research", label: "Research" },
  { value: "curation", label: "Curation" },
  { value: "synthesis", label: "Synthesis" },
  { value: "purpose-claims", label: "Purpose Claims" },
];

function formatDateHeading(dateStr: string): string {
  if (!dateStr) return "Undated";
  const [year, month, day] = dateStr.split("-");
  const months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
  ];
  return `${months[parseInt(month, 10) - 1]} ${parseInt(day, 10)}, ${year}`;
}

export function FieldJournalList({ entries }: { entries: FieldJournalEntry[] }) {
  const [filter, setFilter] = useState<Filter>("all");

  const filtered = entries.filter((entry) => {
    if (filter === "all") return true;
    if (filter === "insights") return entry.hasInsights;
    return entry.track === filter;
  });

  // Group by date
  const byDate = new Map<string, FieldJournalEntry[]>();
  for (const entry of filtered) {
    const dateKey = entry.date || "undated";
    if (!byDate.has(dateKey)) byDate.set(dateKey, []);
    byDate.get(dateKey)!.push(entry);
  }

  const insightCount = entries.filter((e) => e.hasInsights).length;

  return (
    <>
      <div className="mb-6 flex flex-wrap items-center gap-2">
        {filters.map((f) => (
          <button
            key={f.value}
            onClick={() => setFilter(f.value)}
            className={`rounded-full px-3 py-1.5 text-xs font-medium transition-colors ${
              filter === f.value
                ? "bg-forest text-cream-50"
                : "bg-cream-100 text-charcoal-500 hover:bg-cream-200"
            }`}
          >
            {f.label}
            {f.value === "insights" && (
              <span className="ml-1 opacity-70">{insightCount}</span>
            )}
            {f.value === "all" && (
              <span className="ml-1 opacity-70">{entries.length}</span>
            )}
          </button>
        ))}
      </div>

      {filtered.length === 0 ? (
        <p className="py-12 text-center text-sm text-charcoal-400">
          No entries match this filter.
        </p>
      ) : (
        <div className="space-y-8">
          {Array.from(byDate.entries()).map(([dateKey, dateEntries]) => (
            <section key={dateKey}>
              <h2 className="mb-3 border-b border-sage-200 pb-1 font-mono text-sm text-charcoal-400">
                {formatDateHeading(dateKey)}
              </h2>
              <div className="space-y-3">
                {dateEntries.map((entry) => (
                  <FieldJournalCard key={entry.id} entry={entry} />
                ))}
              </div>
            </section>
          ))}
        </div>
      )}
    </>
  );
}
