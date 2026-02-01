import { notFound } from "next/navigation";
import Link from "next/link";
import { getMechanisms } from "@/lib/data/synthesis";
import { getAllSpecimens } from "@/lib/data/specimens";
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
    title: `${mechanism.name} — Mechanisms — Ambidexterity Field Guide`,
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
          Mechanisms
        </Link>
        <span className="mx-2">/</span>
        <span className="text-charcoal-700">#{mechanism.id}</span>
      </nav>

      {/* Header */}
      <header>
        <span className="font-mono text-sm text-charcoal-400">
          Mechanism #{mechanism.id}
        </span>
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
            Specimens Demonstrating This Mechanism ({linkedSpecimens.length})
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
