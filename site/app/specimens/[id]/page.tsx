import { notFound } from "next/navigation";
import Link from "next/link";
import { getAllSpecimens, getSpecimenById } from "@/lib/data/specimens";
import { getMechanisms } from "@/lib/data/synthesis";
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
  const [specimen, allSpecimens, mechanismData] = await Promise.all([
    getSpecimenById(params.id),
    getAllSpecimens(),
    getMechanisms(),
  ]);

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
      />

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
      other.classification.structuralModel ===
      specimen.classification.structuralModel
    ) {
      score += 3;
    }
    // Same orientation
    if (
      other.classification.orientation === specimen.classification.orientation
    ) {
      score += 2;
    }
    // Shared mechanisms
    const sharedMechs = other.mechanisms.filter((m) =>
      specimen.mechanisms.some((sm) => sm.id === m.id)
    ).length;
    score += sharedMechs * 2;
    // Same industry
    if (other.habitat.industry === specimen.habitat.industry) {
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
