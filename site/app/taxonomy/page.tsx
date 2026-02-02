import Link from "next/link";
import { getSpecimensByTaxonomy, getComputedStats } from "@/lib/data/specimens";
import { TaxonomyMatrix } from "@/components/taxonomy/TaxonomyMatrix";
import { STRUCTURAL_MODELS, ORIENTATION_DESCRIPTIONS } from "@/lib/types/taxonomy";
import type { StructuralModel } from "@/lib/types/specimen";

export const metadata = {
  title: "Taxonomy — Field Guide to AI Organizations",
  description: "7 structural models x 3 ambidexterity orientations",
};

export default async function TaxonomyPage() {
  const [matrix, stats] = await Promise.all([
    getSpecimensByTaxonomy(),
    getComputedStats(),
  ]);

  return (
    <div className="space-y-12">
      <header>
        <h1 className="font-serif text-3xl font-semibold text-forest">
          Taxonomy Browser
        </h1>
        <p className="mt-2 text-charcoal-500">
          Specimens are classified along two dimensions: structural model (how AI
          work is organized) and ambidexterity orientation (how the org balances
          exploration and execution).
        </p>
      </header>

      {/* Matrix */}
      <section>
        <h2 className="mb-2 font-serif text-xl text-forest">
          7 &times; 3 Classification Matrix
        </h2>
        <p className="mb-4 text-sm text-charcoal-400">
          Click any cell to see the specimens in that category.{" "}
          {stats.totalSpecimens} specimens total.
        </p>
        <TaxonomyMatrix matrix={matrix} />
      </section>

      {/* Structural Models reference */}
      <section>
        <h2 className="mb-4 font-serif text-xl text-forest">
          Structural Models
        </h2>
        <div className="grid gap-3 md:grid-cols-2">
          {([1, 2, 3, 4, 5, 6, 7] as StructuralModel[]).map((m) => {
            const info = STRUCTURAL_MODELS[m];
            const count = stats.byModel[String(m)] ?? 0;
            return (
              <Link
                key={m}
                href={`/taxonomy/models/${m}`}
                className="group rounded-lg border border-sage-200 bg-cream-50 p-4 transition-shadow hover:shadow-md"
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-sm font-medium text-forest group-hover:text-forest-600">
                    {info.shortName}: {info.name}
                  </span>
                  <span className="font-mono text-xs text-charcoal-400">
                    {count} specimen{count !== 1 ? "s" : ""} &rarr;
                  </span>
                </div>
                <p className="mt-1 text-sm text-charcoal-500">
                  {info.description}
                </p>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Orientations reference */}
      <section>
        <h2 className="mb-4 font-serif text-xl text-forest">
          Ambidexterity Orientations
        </h2>
        <div className="grid gap-3 md:grid-cols-3">
          {(Object.entries(ORIENTATION_DESCRIPTIONS) as [string, string][]).map(
            ([orientation, description]) => {
              const count = stats.byOrientation[orientation] ?? 0;
              return (
                <Link
                  key={orientation}
                  href={`/taxonomy/orientations/${orientation}`}
                  className="group rounded-lg border border-sage-200 bg-cream-50 p-4 transition-shadow hover:shadow-md"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-sm font-medium text-sage-700 group-hover:text-sage-800">
                      {orientation}
                    </span>
                    <span className="font-mono text-xs text-charcoal-400">
                      {count} &rarr;
                    </span>
                  </div>
                  <p className="mt-1 text-sm text-charcoal-500">
                    {description}
                  </p>
                </Link>
              );
            }
          )}
        </div>
      </section>
    </div>
  );
}
