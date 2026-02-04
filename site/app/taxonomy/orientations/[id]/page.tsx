import { notFound } from "next/navigation";
import Link from "next/link";
import { getAllSpecimens } from "@/lib/data/specimens";
import { getMechanisms } from "@/lib/data/synthesis";
import { ORIENTATION_DESCRIPTIONS } from "@/lib/types/taxonomy";
import { SpecimenCard } from "@/components/specimens/SpecimenCard";
import type { Orientation } from "@/lib/types/specimen";

const VALID_ORIENTATIONS = ["Structural", "Contextual", "Temporal"] as const;

export function generateStaticParams() {
  return VALID_ORIENTATIONS.map((id) => ({ id }));
}

export async function generateMetadata({ params }: { params: { id: string } }) {
  const orientation = params.id as Orientation;
  if (!VALID_ORIENTATIONS.includes(orientation as (typeof VALID_ORIENTATIONS)[number])) {
    return {};
  }
  return {
    title: `${orientation} Orientation — Field Guide to AI Organizations`,
  };
}

export default async function OrientationDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const orientation = params.id as Orientation;
  if (!VALID_ORIENTATIONS.includes(orientation as (typeof VALID_ORIENTATIONS)[number])) {
    notFound();
  }

  const description = ORIENTATION_DESCRIPTIONS[orientation];

  const [specimens, mechanismData] = await Promise.all([
    getAllSpecimens(),
    getMechanisms(),
  ]);
  const matching = specimens.filter(
    (s) =>
      s.meta.status !== "Archived" &&
      s.classification.orientation === orientation
  );

  return (
    <div className="space-y-10">
      {/* Breadcrumb */}
      <nav className="text-sm text-charcoal-400">
        <Link href="/taxonomy" className="hover:text-forest">
          Taxonomy
        </Link>
        <span className="mx-1.5">/</span>
        <span className="text-charcoal-600">{orientation}</span>
      </nav>

      {/* Header */}
      <header>
        <div className="flex items-center gap-3">
          <span className="rounded bg-sage-100 px-2.5 py-1 font-mono text-sm font-medium text-sage-700">
            {orientation}
          </span>
          <h1 className="font-serif text-3xl font-semibold text-forest">
            {orientation} Orientation
          </h1>
        </div>
      </header>

      {/* Description */}
      <section className="rounded-lg border border-sage-200 bg-cream-50 p-6">
        <h2 className="mb-3 font-serif text-lg text-forest">
          What It Means
        </h2>
        <p className="leading-relaxed text-charcoal-600">{description}</p>
      </section>

      {/* Common Principles */}
      {(() => {
        const relatedMechanisms = mechanismData.confirmed
          .filter((m) => m.affinityProfile?.orientationDistribution[orientation])
          .sort(
            (a, b) =>
              (b.affinityProfile?.orientationDistribution[orientation]?.count ?? 0) -
              (a.affinityProfile?.orientationDistribution[orientation]?.count ?? 0)
          );
        if (relatedMechanisms.length === 0) return null;
        return (
          <section>
            <h2 className="mb-4 font-serif text-lg text-forest">
              Common Principles
            </h2>
            <div className="space-y-2">
              {relatedMechanisms.map((m) => {
                const dist = m.affinityProfile!.orientationDistribution[orientation];
                return (
                  <Link
                    key={m.id}
                    href={`/mechanisms/${m.id}`}
                    className="flex items-center justify-between rounded-lg border border-sage-200 bg-cream-50 p-4 transition-shadow hover:shadow-sm"
                  >
                    <div>
                      <span className="font-mono text-xs text-charcoal-400">
                        #{m.id}
                      </span>{" "}
                      <span className="text-sm font-medium text-forest">
                        {m.name}
                      </span>
                    </div>
                    <span className="font-mono text-xs text-charcoal-400">
                      {dist.count} specimen{dist.count !== 1 ? "s" : ""} ({dist.percentage}%)
                    </span>
                  </Link>
                );
              })}
            </div>
          </section>
        );
      })()}

      {/* Specimens */}
      <section>
        <h2 className="mb-4 font-serif text-lg text-forest">
          Specimens ({matching.length})
        </h2>
        {matching.length > 0 ? (
          <div className="grid gap-4 sm:grid-cols-2">
            {matching.map((s) => (
              <SpecimenCard key={s.id} specimen={s} />
            ))}
          </div>
        ) : (
          <p className="text-sm text-charcoal-400">
            No specimens with this orientation yet.
          </p>
        )}
      </section>
    </div>
  );
}
