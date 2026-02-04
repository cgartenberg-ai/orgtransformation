import Link from "next/link";
import { getAllSpecimens } from "@/lib/data/specimens";
import { SpecimenCard } from "@/components/specimens/SpecimenCard";

export const metadata = {
  title: "AI-Native Organizations — Field Guide to AI Organizations",
};

export default async function AINativePage() {
  const specimens = await getAllSpecimens();

  const active = specimens.filter((s) => s.meta.status !== "Archived");

  // M9 AI-Native is now a structural model — filter by model OR orgType tag for backward compat
  const aiNative = active.filter(
    (s) => s.classification.structuralModel === 9 || s.habitat.orgType === "AI-native"
  );

  const aiAdopter = active.filter(
    (s) => s.classification.structuralModel !== 9 && s.habitat.orgType !== "AI-native"
  );

  // Orientation distribution for AI-native
  const orientDist: Record<string, number> = {};
  for (const s of aiNative) {
    const o = s.classification.orientation;
    if (o) orientDist[o] = (orientDist[o] || 0) + 1;
  }

  return (
    <div className="space-y-10">
      {/* Header */}
      <header>
        <div className="flex items-center gap-3">
          <span className="rounded bg-violet-100 px-2.5 py-1 font-mono text-sm font-medium text-violet-700">
            AI-native
          </span>
          <h1 className="font-serif text-3xl font-semibold text-forest">
            AI-Native Organizations
          </h1>
        </div>
        <p className="mt-3 max-w-3xl leading-relaxed text-charcoal-600">
          AI-native organizations were born as AI companies &mdash; artificial
          intelligence is not something they adopted, it is their foundational
          technology and business model. Their ambidexterity challenges differ
          fundamentally from AI-adopters: rather than balancing AI exploration
          against legacy operations, they balance frontier research against
          product-market execution.
        </p>
      </header>

      {/* Key differences */}
      <section className="rounded-lg border border-sage-200 bg-cream-50 p-6">
        <h2 className="mb-4 font-serif text-lg text-forest">
          How AI-Native Differs from AI-Adopter
        </h2>
        <div className="grid gap-6 sm:grid-cols-2">
          <div>
            <h3 className="mb-2 font-mono text-xs font-medium uppercase tracking-wide text-violet-600">
              AI-Native ({aiNative.length} specimens)
            </h3>
            <ul className="space-y-1.5 text-sm text-charcoal-600">
              <li>AI is the core product, not a support function</li>
              <li>
                Exploration/execution tension is research vs. product shipping
              </li>
              <li>Talent is the primary constraint, not adoption</li>
              <li>Classified as M9 (AI-Native) — a distinct structural species</li>
            </ul>
          </div>
          <div>
            <h3 className="mb-2 font-mono text-xs font-medium uppercase tracking-wide text-charcoal-400">
              AI-Adopter ({aiAdopter.length} specimens)
            </h3>
            <ul className="space-y-1.5 text-sm text-charcoal-600">
              <li>AI augments existing business operations</li>
              <li>
                Exploration/execution tension is transformation vs. core business
              </li>
              <li>Cultural adoption is the primary constraint</li>
              <li>Structural models span M1–M8</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Distribution */}
      <section>
        <h2 className="mb-4 font-serif text-lg text-forest">
          Taxonomy Distribution
        </h2>
        <div className="grid gap-4 sm:grid-cols-2">
          {/* Model classification */}
          <div className="rounded-lg border border-sage-200 bg-white p-4">
            <h3 className="mb-3 text-xs font-medium uppercase tracking-wide text-charcoal-400">
              Structural Model
            </h3>
            <Link
              href="/taxonomy/models/9"
              className="flex items-center gap-2 text-sm text-charcoal-600 hover:text-forest"
            >
              <span className="rounded bg-violet-100 px-2 py-0.5 font-mono text-xs font-medium text-violet-700">
                M9
              </span>
              AI-Native &mdash; {aiNative.length} specimens
            </Link>
            <p className="mt-2 text-xs text-charcoal-400">
              All AI-native organizations are classified under Model 9, a distinct structural species where AI is the foundational operating model rather than a transformation initiative.
            </p>
          </div>

          {/* Orientation distribution */}
          <div className="rounded-lg border border-sage-200 bg-white p-4">
            <h3 className="mb-3 text-xs font-medium uppercase tracking-wide text-charcoal-400">
              By Orientation
            </h3>
            <div className="space-y-2">
              {Object.entries(orientDist)
                .sort(([, a], [, b]) => b - a)
                .map(([orient, count]) => (
                  <div key={orient} className="flex items-center justify-between">
                    <Link
                      href={`/taxonomy/orientations/${orient}`}
                      className="text-sm text-charcoal-600 hover:text-forest"
                    >
                      {orient}
                    </Link>
                    <span className="font-mono text-xs text-charcoal-400">
                      {count}
                    </span>
                  </div>
                ))}
            </div>
          </div>
        </div>
      </section>

      {/* Specimens */}
      <section>
        <h2 className="mb-4 font-serif text-lg text-forest">
          All AI-Native Specimens ({aiNative.length})
        </h2>
        <div className="grid gap-4 sm:grid-cols-2">
          {aiNative.map((s) => (
            <SpecimenCard key={s.id} specimen={s} />
          ))}
        </div>
      </section>
    </div>
  );
}
