import { notFound } from "next/navigation";
import Link from "next/link";
import { getAllSpecimens } from "@/lib/data/specimens";
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

  const specimens = await getAllSpecimens();
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
