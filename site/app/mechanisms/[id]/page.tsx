import { notFound } from "next/navigation";
import Link from "next/link";
import { getMechanisms } from "@/lib/data/synthesis";
import { getAllSpecimens } from "@/lib/data/specimens";
import { STRUCTURAL_MODELS } from "@/lib/types/taxonomy";
import type { StructuralModel } from "@/lib/types/specimen";
import { SpecimenCard } from "@/components/specimens/SpecimenCard";

export async function generateStaticParams() {
  const data = await getMechanisms();
  return data.confirmed.map((m) => ({ id: String(m.id) }));
}

export async function generateMetadata({
  params,
}: {
  params: { id: string };
}) {
  const data = await getMechanisms();
  const mechanism = data.confirmed.find((m) => m.id === Number(params.id));
  if (!mechanism) return {};
  return {
    title: `${mechanism.name} — Principles — Field Guide to AI Organizations`,
    description: mechanism.definition,
  };
}

export default async function MechanismDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const [mechanismData, allSpecimens] = await Promise.all([
    getMechanisms(),
    getAllSpecimens(),
  ]);

  const mechanism = mechanismData.confirmed.find(
    (m) => m.id === Number(params.id)
  );
  if (!mechanism) notFound();

  const linkedSpecimens = allSpecimens.filter((s) =>
    mechanism.specimens.includes(s.id)
  );

  return (
    <div className="space-y-8">
      {/* Breadcrumb */}
      <nav className="text-sm text-charcoal-400">
        <Link href="/mechanisms" className="hover:text-forest">
          Principles
        </Link>
        <span className="mx-2">/</span>
        <span className="text-charcoal-700">Principle #{mechanism.id}</span>
      </nav>

      {/* Header */}
      <header>
        <div className="flex items-center gap-3">
          <span className="font-mono text-sm text-charcoal-400">
            Principle #{mechanism.id}
          </span>
          {mechanism.maturity && (
            <span className={`rounded px-2 py-0.5 font-mono text-xs ${
              mechanism.maturity === "widespread" ? "bg-amber-50 text-amber-700" :
              mechanism.maturity === "emerging" ? "bg-sage-50 text-sage-600" :
              "bg-forest-50 text-forest"
            }`}>
              {mechanism.maturity}
            </span>
          )}
        </div>
        <h1 className="mt-1 font-serif text-3xl font-semibold text-forest">
          {mechanism.name}
        </h1>
      </header>

      {/* Definition */}
      <section>
        <h2 className="mb-2 font-serif text-lg text-forest">Definition</h2>
        <p className="text-base leading-relaxed text-charcoal-700">
          {mechanism.definition}
        </p>
      </section>

      {/* Problem It Solves */}
      <section>
        <h2 className="mb-2 font-serif text-lg text-forest">
          Problem It Solves
        </h2>
        <p className="text-sm leading-relaxed text-charcoal-600">
          {mechanism.problemItSolves}
        </p>
      </section>

      {/* Theoretical Connection */}
      <section>
        <h2 className="mb-2 font-serif text-lg text-forest">
          Theoretical Connection
        </h2>
        <p className="text-sm leading-relaxed text-charcoal-600">
          {mechanism.theoreticalConnection}
        </p>
      </section>

      {/* Scholarly Anchor */}
      {mechanism.scholarlyAnchor && (
        <section>
          <h2 className="mb-2 font-serif text-lg text-forest">
            Scholarly Anchor
          </h2>
          <p className="text-sm leading-relaxed text-charcoal-600">
            {mechanism.scholarlyAnchor}
          </p>
        </section>
      )}

      {/* Taxonomy Affinity */}
      {mechanism.affinityProfile && (
        <section className="rounded-lg border border-sage-200 bg-cream-50 p-6">
          <h2 className="mb-4 font-serif text-lg text-forest">
            Taxonomy Affinity
          </h2>
          <p className="mb-4 text-sm text-charcoal-600">
            {mechanism.affinityProfile.affinitySummary}
          </p>

          <div className="grid gap-6 sm:grid-cols-2">
            {/* Model distribution */}
            <div>
              <h3 className="mb-3 text-xs font-medium uppercase tracking-wide text-charcoal-400">
                By Structural Model
              </h3>
              <div className="space-y-2">
                {Object.entries(mechanism.affinityProfile.modelDistribution)
                  .sort(([, a], [, b]) => b.count - a.count)
                  .map(([model, data]) => {
                    const maxCount = Math.max(
                      ...Object.values(mechanism.affinityProfile!.modelDistribution).map((d) => d.count)
                    );
                    return (
                      <div key={model} className="space-y-1">
                        <div className="flex items-center justify-between text-sm">
                          <Link
                            href={`/taxonomy/models/${model}`}
                            className="text-charcoal-600 hover:text-forest"
                          >
                            <span className="font-mono text-xs text-forest">M{model}</span>{" "}
                            {STRUCTURAL_MODELS[Number(model) as StructuralModel]?.name}
                          </Link>
                          <span className="font-mono text-xs text-charcoal-400">
                            {data.count} ({data.percentage}%)
                          </span>
                        </div>
                        <div className="h-1.5 rounded-full bg-sage-100">
                          <div
                            className="h-1.5 rounded-full bg-forest"
                            style={{ width: `${(data.count / maxCount) * 100}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
              </div>
            </div>

            {/* Orientation distribution */}
            <div>
              <h3 className="mb-3 text-xs font-medium uppercase tracking-wide text-charcoal-400">
                By Orientation
              </h3>
              <div className="space-y-2">
                {Object.entries(mechanism.affinityProfile.orientationDistribution)
                  .sort(([, a], [, b]) => b.count - a.count)
                  .map(([orient, data]) => (
                    <div key={orient} className="space-y-1">
                      <div className="flex items-center justify-between text-sm">
                        <Link
                          href={`/taxonomy/orientations/${orient}`}
                          className="text-charcoal-600 hover:text-forest"
                        >
                          {orient}
                        </Link>
                        <span className="font-mono text-xs text-charcoal-400">
                          {data.count} ({data.percentage}%)
                        </span>
                      </div>
                      <div className="h-1.5 rounded-full bg-sage-100">
                        <div
                          className={`h-1.5 rounded-full ${
                            orient === "Structural"
                              ? "bg-forest"
                              : orient === "Contextual"
                              ? "bg-amber"
                              : "bg-sage"
                          }`}
                          style={{ width: `${data.percentage}%` }}
                        />
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Evidence */}
      {mechanism.evidence.length > 0 && (
        <section>
          <h2 className="mb-3 font-serif text-lg text-forest">
            Evidence ({mechanism.evidence.length})
          </h2>
          <div className="space-y-3">
            {mechanism.evidence.map((e, i) => (
              <div
                key={i}
                className="rounded-lg border border-sage-200 bg-cream-50 p-4"
              >
                <div className="flex items-start justify-between">
                  <Link
                    href={`/specimens/${e.specimenId}`}
                    className="font-medium text-forest hover:underline"
                  >
                    {allSpecimens.find((s) => s.id === e.specimenId)?.name ??
                      e.specimenId}
                  </Link>
                  <span className="text-xs text-charcoal-400">{e.source}</span>
                </div>
                {e.quote && (
                  <blockquote className="mt-2 border-l-2 border-amber pl-3 text-sm italic text-charcoal-600">
                    &ldquo;{e.quote}&rdquo;
                    {e.speaker && (
                      <span className="not-italic text-charcoal-400">
                        {" "}
                        &mdash; {e.speaker}
                      </span>
                    )}
                  </blockquote>
                )}
                {e.notes && (
                  <p className="mt-1 text-xs text-charcoal-400">{e.notes}</p>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Linked Specimens */}
      {linkedSpecimens.length > 0 && (
        <section>
          <h2 className="mb-3 font-serif text-lg text-forest">
            Organizations Showing This Principle ({linkedSpecimens.length})
          </h2>
          <div className="grid gap-3 md:grid-cols-2">
            {linkedSpecimens.map((s) => (
              <SpecimenCard key={s.id} specimen={s} compact />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
