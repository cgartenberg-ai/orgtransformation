import { notFound } from "next/navigation";
import Link from "next/link";
import { getAllSpecimens, getSpecimenById } from "@/lib/data/specimens";
import { getMechanisms, getFindings } from "@/lib/data/synthesis";
import { getPurposeClaims, getSpecimenEnrichment } from "@/lib/data/purpose-claims";
import { ClassificationBadge } from "@/components/shared/ClassificationBadge";
import { SpecimenTabs } from "@/components/specimens/SpecimenTabs";
import type { Specimen } from "@/lib/types/specimen";

export async function generateStaticParams() {
  const specimens = await getAllSpecimens();
  return specimens.map((s) => ({ id: s.id }));
}

export async function generateMetadata({
  params,
}: {
  params: { id: string };
}) {
  const specimen = await getSpecimenById(params.id);
  if (!specimen) return {};
  return {
    title: `${specimen.name} — Field Guide to AI Organizations`,
    description: specimen.title,
  };
}

export default async function SpecimenPage({
  params,
}: {
  params: { id: string };
}) {
  const [specimen, allSpecimens, mechanismData, findingData, claimsData, enrichment] = await Promise.all([
    getSpecimenById(params.id),
    getAllSpecimens(),
    getMechanisms(),
    getFindings(),
    getPurposeClaims().catch((e) => {
      console.error("[specimen page] Failed to load purpose claims:", e);
      return { description: "", lastUpdated: "", taxonomyVersion: "", claims: [], claimTypes: [], claimTypeDefinitions: {} } as unknown as Awaited<ReturnType<typeof getPurposeClaims>>;
    }),
    getSpecimenEnrichment(params.id).catch((e) => {
      console.error("[specimen page] Failed to load enrichment:", e);
      return null;
    }),
  ]);

  const specimenClaims = (claimsData?.claims ?? []).filter((c) => c.specimenId === params.id);

  if (!specimen) notFound();

  const related = findRelated(specimen, allSpecimens);

  return (
    <div className="space-y-8">
      {/* Breadcrumb */}
      <nav className="text-sm text-charcoal-400">
        <Link href="/specimens" className="hover:text-forest">
          Specimens
        </Link>
        <span className="mx-2">/</span>
        <span className="text-charcoal-700">{specimen.name}</span>
      </nav>

      {/* Header */}
      <header className="space-y-4">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="font-serif text-3xl font-semibold text-forest">
              {specimen.name}
            </h1>
            <p className="mt-1 text-lg text-charcoal-500">{specimen.title}</p>
          </div>
          <div className="flex items-center gap-2">
            <span
              className={`rounded px-2 py-1 text-xs font-medium ${
                specimen.meta.completeness === "High"
                  ? "bg-forest-50 text-forest"
                  : specimen.meta.completeness === "Medium"
                    ? "bg-amber-50 text-amber-700"
                    : "bg-charcoal-50 text-charcoal-400"
              }`}
            >
              {specimen.meta.completeness} completeness
            </span>
            <span className="rounded px-2 py-1 text-xs text-charcoal-400">
              {specimen.classification.confidence} confidence
            </span>
          </div>
        </div>

        <ClassificationBadge classification={specimen.classification} />

        {/* Habitat summary */}
        <div className="flex flex-wrap gap-3 text-sm text-charcoal-500">
          <span>{specimen.habitat.industry}</span>
          {specimen.habitat.sector && (
            <>
              <span className="text-charcoal-300">&middot;</span>
              <span>{specimen.habitat.sector}</span>
            </>
          )}
          {specimen.habitat.orgSize && (
            <>
              <span className="text-charcoal-300">&middot;</span>
              <span>{specimen.habitat.orgSize}</span>
            </>
          )}
          {specimen.habitat.employees && (
            <>
              <span className="text-charcoal-300">&middot;</span>
              <span>
                {specimen.habitat.employees.toLocaleString()} employees
              </span>
            </>
          )}
          {specimen.habitat.revenue && (
            <>
              <span className="text-charcoal-300">&middot;</span>
              <span>{specimen.habitat.revenue} revenue</span>
            </>
          )}
          {specimen.habitat.headquarters && (
            <>
              <span className="text-charcoal-300">&middot;</span>
              <span>{specimen.habitat.headquarters}</span>
            </>
          )}
        </div>
      </header>

      {/* Tabbed content */}
      <SpecimenTabs
        specimen={specimen}
        related={related}
        mechanismDefinitions={mechanismData.confirmed}
        purposeClaims={specimenClaims}
        claimTypeDefinitions={claimsData?.claimTypeDefinitions ?? {}}
        enrichment={enrichment ?? undefined}
      />

      {/* Consolidated findings this specimen supports */}
      {(() => {
        const specimenFindings = findingData.findings.filter((f) =>
          f.evidence.some((e) => e.specimenId === specimen.id)
        );
        if (specimenFindings.length === 0) return null;

        const PRIMITIVE_COLORS: Record<string, string> = {
          P1: "bg-forest-50 text-forest",
          P2: "bg-amber-50 text-amber-700",
          P3: "bg-violet-50 text-violet-700",
          P4: "bg-sky-50 text-sky-700",
          P5: "bg-rose-50 text-rose-700",
        };

        return (
          <section className="rounded-lg border border-sage-200 bg-cream-50 p-5">
            <h2 className="mb-3 font-serif text-lg text-forest">
              Findings ({specimenFindings.length})
            </h2>
            <p className="mb-3 text-xs text-charcoal-400">
              Consolidated findings this specimen contributes evidence to.
            </p>
            <div className="space-y-3">
              {specimenFindings.map((finding) => {
                const thisEvidence = finding.evidence.find(
                  (e) => e.specimenId === specimen.id
                );
                return (
                  <Link
                    key={finding.id}
                    href={`/findings#${finding.id}`}
                    className="block rounded border border-sage-100 bg-white p-3 transition-colors hover:border-forest-50"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex items-center gap-2">
                        <span className="rounded bg-forest px-1.5 py-0.5 font-mono text-[9px] font-bold text-cream">
                          F{finding.number}
                        </span>
                        <p className="font-serif text-sm font-medium text-forest">
                          {finding.title}
                        </p>
                      </div>
                      <span
                        className={`shrink-0 rounded px-1.5 py-0.5 text-[9px] font-medium ${
                          finding.maturity === "confirmed"
                            ? "bg-forest-50 text-forest"
                            : finding.maturity === "emerging"
                            ? "bg-amber-50 text-amber-700"
                            : "bg-charcoal-50 text-charcoal-400"
                        }`}
                      >
                        {finding.maturity}
                      </span>
                    </div>
                    <div className="mt-1.5 flex gap-1">
                      {finding.primitivesEngaged.map((pid) => (
                        <span
                          key={pid}
                          className={`rounded px-1 py-0.5 font-mono text-[9px] font-bold ${PRIMITIVE_COLORS[pid] || "bg-sage-50 text-sage-700"}`}
                        >
                          {pid}
                        </span>
                      ))}
                    </div>
                    {thisEvidence && (
                      <p className="mt-1 text-xs text-charcoal-500">
                        {thisEvidence.note}
                      </p>
                    )}
                  </Link>
                );
              })}
            </div>
          </section>
        );
      })()}

      {/* Meta footer */}
      <footer className="border-t border-sage-200 pt-4 text-xs text-charcoal-400">
        <p>
          Created: {specimen.meta.created} &middot; Last updated:{" "}
          {specimen.meta.lastUpdated} &middot; Layers: {specimen.layers.length}{" "}
          &middot; Sources: {specimen.sources.length}
        </p>
      </footer>
    </div>
  );
}

function findRelated(
  specimen: Specimen,
  allSpecimens: Specimen[]
): Specimen[] {
  const others = allSpecimens.filter(
    (s) => s.id !== specimen.id && s.meta.status !== "Archived"
  );

  // Score each by relationship strength
  const scored = others.map((other) => {
    let score = 0;
    // Same primary model
    if (
      other.classification?.structuralModel != null &&
      specimen.classification?.structuralModel != null &&
      other.classification.structuralModel ===
      specimen.classification.structuralModel
    ) {
      score += 3;
    }
    // Same orientation
    if (
      other.classification?.orientation &&
      specimen.classification?.orientation &&
      other.classification.orientation === specimen.classification.orientation
    ) {
      score += 2;
    }
    // Shared mechanisms
    const sharedMechs = (other.mechanisms ?? []).filter((m) =>
      (specimen.mechanisms ?? []).some((sm) => sm.id === m.id)
    ).length;
    score += sharedMechs * 2;
    // Same industry
    if (other.habitat?.industry && other.habitat.industry === specimen.habitat?.industry) {
      score += 1;
    }
    return { specimen: other, score };
  });

  return scored
    .filter((s) => s.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 12)
    .map((s) => s.specimen);
}
