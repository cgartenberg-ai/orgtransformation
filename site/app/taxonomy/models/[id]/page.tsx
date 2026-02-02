import { notFound } from "next/navigation";
import Link from "next/link";
import { getAllSpecimens } from "@/lib/data/specimens";
import { STRUCTURAL_MODELS, SUB_TYPES } from "@/lib/types/taxonomy";
import { SpecimenCard } from "@/components/specimens/SpecimenCard";
import type { StructuralModel } from "@/lib/types/specimen";

const VALID_MODELS = [1, 2, 3, 4, 5, 6, 7] as const;

export function generateStaticParams() {
  return VALID_MODELS.map((id) => ({ id: String(id) }));
}

export async function generateMetadata({ params }: { params: { id: string } }) {
  const modelNum = Number(params.id) as StructuralModel;
  const model = STRUCTURAL_MODELS[modelNum];
  if (!model) return {};
  return {
    title: `${model.shortName}: ${model.name} — Field Guide to AI Organizations`,
  };
}

// Sub-types that belong to each model
const MODEL_SUBTYPES: Record<number, string[]> = {
  5: ["5a", "5b", "5c"],
  6: ["6a", "6b", "6c"],
};

export default async function ModelDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const modelNum = Number(params.id) as StructuralModel;
  const model = STRUCTURAL_MODELS[modelNum];
  if (!model || !VALID_MODELS.includes(modelNum as (typeof VALID_MODELS)[number])) {
    notFound();
  }

  const specimens = await getAllSpecimens();

  const matching = specimens.filter(
    (s) =>
      s.meta.status !== "Archived" &&
      s.classification.structuralModel === modelNum
  );

  const subtypeKeys = MODEL_SUBTYPES[modelNum] || [];

  return (
    <div className="space-y-10">
      {/* Breadcrumb */}
      <nav className="text-sm text-charcoal-400">
        <Link href="/taxonomy" className="hover:text-forest">
          Taxonomy
        </Link>
        <span className="mx-1.5">/</span>
        <span className="text-charcoal-600">
          {model.shortName}: {model.name}
        </span>
      </nav>

      {/* Header */}
      <header>
        <div className="flex items-center gap-3">
          <span className="rounded bg-forest-50 px-2.5 py-1 font-mono text-sm font-medium text-forest">
            {model.shortName}
          </span>
          <h1 className="font-serif text-3xl font-semibold text-forest">
            {model.name}
          </h1>
        </div>
        <p className="mt-2 text-charcoal-500">{model.description}</p>
      </header>

      {/* Characteristics */}
      <section className="rounded-lg border border-sage-200 bg-cream-50 p-6">
        <h2 className="mb-3 font-serif text-lg text-forest">Characteristics</h2>
        <p className="leading-relaxed text-charcoal-600">
          {model.characteristics}
        </p>
      </section>

      {/* Sub-types (M5 and M6 only) */}
      {subtypeKeys.length > 0 && (
        <section>
          <h2 className="mb-4 font-serif text-lg text-forest">Sub-types</h2>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {subtypeKeys.map((key) => {
              const subTypeName = SUB_TYPES[key];
              const count = matching.filter(
                (s) => s.classification.subType === key
              ).length;
              return (
                <div
                  key={key}
                  className="rounded-lg border border-sage-200 bg-white p-4"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-sm font-medium text-forest">
                      {key.toUpperCase()}
                    </span>
                    <span className="font-mono text-xs text-charcoal-400">
                      {count} specimen{count !== 1 ? "s" : ""}
                    </span>
                  </div>
                  <p className="mt-1 text-sm font-medium text-charcoal-700">
                    {subTypeName}
                  </p>
                </div>
              );
            })}
          </div>
        </section>
      )}

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
            No specimens classified under this model yet.
          </p>
        )}
      </section>
    </div>
  );
}
