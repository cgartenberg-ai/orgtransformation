"use client";

import { useState } from "react";
import type { SpecimenEnrichment } from "@/lib/types/purpose-claims";
import { SpiderChart } from "@/components/visualizations/SpiderChart";
import { normalizeDistribution, rawProportions } from "@/lib/utils/spider-data";

function CollapsibleSection({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(false);
  return (
    <div>
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1.5 text-xs font-medium text-charcoal-500 hover:text-forest transition-colors"
      >
        <span className="text-[10px]">{open ? "\u25BE" : "\u25B8"}</span>
        {title}
      </button>
      {open && (
        <div className="mt-2 rounded-md bg-cream-50 border border-sage-200 px-3 py-2.5">
          {children}
        </div>
      )}
    </div>
  );
}

export function EnrichmentSummary({
  enrichment,
  specimenId,
}: {
  enrichment: SpecimenEnrichment;
  specimenId: string;
}) {
  const hasKeyFindings = enrichment.keyFindings.length > 0;
  const hasPatterns = enrichment.rhetoricalPatterns.length > 0;
  const hasComparative = !!enrichment.comparativeNotes;
  const hasAbsences = !!enrichment.notableAbsences;
  const hasCorrectedInfo = !!enrichment.correctedLeaderInfo;
  const hasAnyContent = hasKeyFindings || hasPatterns || hasComparative || hasAbsences || hasCorrectedInfo;

  // Don't render if there's nothing beyond the spider
  if (!hasAnyContent && enrichment.claimCount === 0) return null;

  const scanDate = enrichment.scannedDate
    ? new Date(enrichment.scannedDate + "T00:00:00").toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      })
    : null;

  // Build field journal link ID
  const journalId = enrichment.scanNarrative
    ? `purpose-claims--${enrichment.scannedDate}-scan-${specimenId}`
    : null;

  const normalizedValues = normalizeDistribution(enrichment.claimTypeDistribution);
  const rawProps = rawProportions(enrichment.claimTypeDistribution);

  return (
    <div className="mb-6 rounded-lg border border-sage-200 bg-white p-5">
      {/* Header */}
      <div className="mb-3 flex items-center justify-between">
        <h3 className="font-serif text-sm font-medium text-forest">
          Rhetorical Profile
        </h3>
        <div className="flex items-center gap-2 text-[10px] text-charcoal-400">
          {scanDate && <span>Scanned {scanDate}</span>}
          <span
            className={`rounded-full px-1.5 py-0.5 text-[9px] font-medium ${
              enrichment.quality === "rich"
                ? "bg-forest-50 text-forest"
                : enrichment.quality === "adequate"
                  ? "bg-amber-50 text-amber-700"
                  : "bg-charcoal-50 text-charcoal-500"
            }`}
          >
            {enrichment.quality}
          </span>
        </div>
      </div>

      {/* Spider diagram */}
      <div className="flex justify-center">
        <SpiderChart
          values={normalizedValues}
          rawProportions={rawProps}
          size={220}
          showLabels={true}
          showGrid={true}
          interactive={true}
        />
      </div>

      {/* Claim count summary below spider */}
      <p className="mt-1 text-center text-[10px] text-charcoal-400">
        {enrichment.claimCount} claims across {Object.values(enrichment.claimTypeDistribution).filter(v => v && v > 0).length} types
      </p>

      {/* Key Findings */}
      {hasKeyFindings && (
        <div className="mt-4">
          <h4 className="mb-2 text-xs font-medium text-charcoal-600">Key Findings</h4>
          <ul className="space-y-1.5">
            {enrichment.keyFindings.map((finding, i) => (
              <li key={i} className="flex gap-2 text-xs leading-relaxed text-charcoal-600">
                <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-forest/40" />
                <span>{finding}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Rhetorical Patterns */}
      {hasPatterns && (
        <div className="mt-4">
          <h4 className="mb-2 text-xs font-medium text-charcoal-600">Rhetorical Patterns</h4>
          <div className="flex flex-wrap gap-1.5">
            {enrichment.rhetoricalPatterns.map((pattern, i) => (
              <span
                key={i}
                className="inline-block rounded-md bg-sage-50 px-2 py-1 text-[11px] leading-tight text-charcoal-600 border border-sage-200"
              >
                {pattern}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Collapsible sections */}
      {(hasComparative || hasAbsences || hasCorrectedInfo) && (
        <div className="mt-4 space-y-2">
          {hasComparative && (
            <CollapsibleSection title="Comparative Notes">
              <p className="text-xs leading-relaxed text-charcoal-600">
                {enrichment.comparativeNotes}
              </p>
            </CollapsibleSection>
          )}
          {hasAbsences && (
            <CollapsibleSection title="Notable Absences">
              <p className="text-xs leading-relaxed text-charcoal-600">
                {enrichment.notableAbsences}
              </p>
            </CollapsibleSection>
          )}
          {hasCorrectedInfo && (
            <CollapsibleSection title="Leader Info Corrections">
              <p className="text-xs leading-relaxed text-charcoal-600">
                {enrichment.correctedLeaderInfo}
              </p>
            </CollapsibleSection>
          )}
        </div>
      )}

      {/* Footer: scan metadata + journal link */}
      <div className="mt-4 flex items-center justify-between border-t border-sage-100 pt-3">
        <span className="text-[10px] text-charcoal-400">
          {enrichment.searchesCompleted} searches &middot; {enrichment.urlsFetched} URLs fetched
          {enrichment.fetchFailures.length > 0 && (
            <> &middot; {enrichment.fetchFailures.length} blocked</>
          )}
        </span>
        {journalId && (
          <a
            href={`/field-journal/${encodeURIComponent(journalId)}`}
            className="text-[10px] text-charcoal-400 hover:text-forest transition-colors"
          >
            View scan journal &rarr;
          </a>
        )}
      </div>
    </div>
  );
}

/**
 * Compact enrichment display for the purpose claims browser sidebar/header.
 */
export function EnrichmentCompact({
  enrichment,
}: {
  enrichment: SpecimenEnrichment;
}) {
  const hasContent = enrichment.keyFindings.length > 0 || enrichment.rhetoricalPatterns.length > 0;
  if (!hasContent) return null;

  const normalizedValues = normalizeDistribution(enrichment.claimTypeDistribution);

  return (
    <div className="space-y-2">
      {/* Mini spider diagram */}
      <div className="flex justify-center">
        <SpiderChart
          values={normalizedValues}
          size={140}
          showLabels={true}
          showGrid={false}
          interactive={false}
        />
      </div>

      {/* First key finding only */}
      {enrichment.keyFindings.length > 0 && (
        <p className="text-[11px] leading-relaxed text-charcoal-500">
          {enrichment.keyFindings[0]}
        </p>
      )}

      {/* Pattern tags */}
      {enrichment.rhetoricalPatterns.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {enrichment.rhetoricalPatterns.slice(0, 3).map((p, i) => (
            <span
              key={i}
              className="inline-block rounded bg-sage-50 px-1.5 py-0.5 text-[9px] text-charcoal-500 border border-sage-200"
            >
              {p.length > 50 ? p.slice(0, 47) + "..." : p}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
