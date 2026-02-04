import {
  getSpecimensByTaxonomy,
  getComputedStats,
  getAllSpecimens,
} from "@/lib/data/specimens";
import { getMechanisms } from "@/lib/data/synthesis";
import { TaxonomyMatrix } from "@/components/taxonomy/TaxonomyMatrix";
import { ModelAccordion } from "@/components/taxonomy/ModelAccordion";
import { OrientationAccordion } from "@/components/taxonomy/OrientationAccordion";
import { MODEL_NUMBERS, ORIENTATIONS } from "@/lib/types/taxonomy";
import type { Orientation } from "@/lib/types/specimen";

export const metadata = {
  title: "Taxonomy — Field Guide to AI Organizations",
  description: "8 structural models x 3 ambidexterity orientations",
};

export default async function TaxonomyPage() {
  const [matrix, stats, specimens, mechanismData] = await Promise.all([
    getSpecimensByTaxonomy(),
    getComputedStats(),
    getAllSpecimens(),
    getMechanisms(),
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
          Classification Matrix
        </h2>
        <p className="mb-4 text-sm text-charcoal-400">
          Click any cell to see the specimens in that category.{" "}
          {stats.totalSpecimens} specimens total.
        </p>
        <TaxonomyMatrix matrix={matrix} />
      </section>

      {/* Key Insights */}
      <section className="grid gap-4 md:grid-cols-2">
        <div className="rounded-lg border-l-4 border-l-amber bg-cream-50 p-5">
          <h3 className="mb-2 font-serif text-sm font-semibold text-charcoal-700">
            The Quiet Majority
          </h3>
          <p className="text-sm leading-relaxed text-charcoal-600">
            Model 6 (Unnamed/Informal) captures AI adoption that happens without
            formal structure. Research focused only on named labs (Models 1&ndash;5)
            systematically underestimates AI&apos;s organizational transformation.
            Many of the most impactful deployments have no lab, no CAIO, and no
            branded initiative.
          </p>
        </div>
        <div className="rounded-lg border-l-4 border-l-forest bg-cream-50 p-5">
          <h3 className="mb-2 font-serif text-sm font-semibold text-charcoal-700">
            Structural Dominance
          </h3>
          <p className="text-sm leading-relaxed text-charcoal-600">
            {stats.byOrientation["Structural"] ?? 0} of {stats.totalSpecimens}{" "}
            specimens ({Math.round(((stats.byOrientation["Structural"] ?? 0) / stats.totalSpecimens) * 100)}%)
            have a Structural orientation &mdash; separate units for exploration and
            execution. This may reflect reporting bias (structural approaches are
            more visible to researchers) rather than actual prevalence.
          </p>
        </div>
        <div className="rounded-lg border-l-4 border-l-sage bg-cream-50 p-5 md:col-span-2">
          <h3 className="mb-2 font-serif text-sm font-semibold text-charcoal-700">
            Hub-and-Spoke Is the Default at Scale
          </h3>
          <p className="text-sm leading-relaxed text-charcoal-600">
            Model 4 (Hub-and-Spoke) is the most populated model with{" "}
            {stats.byModel["4"] ?? 0} specimens. Large, diversified organizations
            consistently arrive at this structure &mdash; a central AI hub for
            platforms and standards, with embedded spokes in business units for
            domain-specific execution. This is convergent evolution: different
            organizations independently discovering the same structural solution.
          </p>
        </div>
      </section>

      {/* Understanding the Models — Accordion */}
      <section>
        <h2 className="mb-4 font-serif text-xl text-forest">
          Understanding the {MODEL_NUMBERS.length} Structural Models
        </h2>
        <div className="space-y-2">
          {MODEL_NUMBERS.map((m) => (
            <ModelAccordion
              key={m}
              modelNum={m}
              specimens={specimens}
              mechanisms={mechanismData.confirmed}
            />
          ))}
        </div>
      </section>

      {/* Three Orientations — Accordion */}
      <section>
        <h2 className="mb-2 font-serif text-xl text-forest">
          Three Ambidexterity Orientations
        </h2>
        <p className="mb-4 text-sm text-charcoal-500">
          Each specimen has one dominant orientation describing how the
          organization balances exploration and execution.
        </p>
        <div className="space-y-2">
          {ORIENTATIONS.map((o) => (
            <OrientationAccordion
              key={o}
              orientation={o as Orientation}
              specimens={specimens}
              mechanisms={mechanismData.confirmed}
            />
          ))}
        </div>
      </section>
    </div>
  );
}
