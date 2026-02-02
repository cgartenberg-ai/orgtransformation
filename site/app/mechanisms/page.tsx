import { getMechanisms } from "@/lib/data/synthesis";
import { getAllSpecimens } from "@/lib/data/specimens";
import Link from "next/link";

export const metadata = {
  title: "Principles — Ambidexterity Field Guide",
  description: "Structural principles observed across organizational specimens",
};

export default async function MechanismsPage() {
  const [mechanismData, allSpecimens] = await Promise.all([
    getMechanisms(),
    getAllSpecimens(),
  ]);

  return (
    <div className="space-y-12">
      <header>
        <h1 className="font-serif text-3xl font-semibold text-forest">
          Principles
        </h1>
        <p className="mt-2 text-charcoal-500">
          Structural principles observed across multiple specimens. These
          principles emerged from systematic observation of how organizations
          structurally enable both exploration and execution.
        </p>
      </header>

      {/* Confirmed Mechanisms */}
      <section>
        <h2 className="mb-4 font-serif text-xl text-forest">
          Confirmed Principles ({mechanismData.confirmed.length})
        </h2>
        <div className="space-y-4">
          {mechanismData.confirmed.map((m) => {
            const linkedSpecimens = allSpecimens.filter((s) =>
              m.specimens.includes(s.id)
            );
            return (
              <Link
                key={m.id}
                href={`/mechanisms/${m.id}`}
                className="group block rounded-lg border border-sage-200 bg-cream-50 p-5 transition-shadow hover:shadow-md"
              >
                <div className="flex items-start justify-between">
                  <h3 className="font-serif text-lg font-medium text-forest group-hover:text-forest-600">
                    <span className="mr-2 font-mono text-sm text-charcoal-400">
                      #{m.id}
                    </span>
                    {m.name}
                  </h3>
                  <span className="shrink-0 rounded bg-forest-50 px-2 py-0.5 font-mono text-xs text-forest">
                    {linkedSpecimens.length} specimen
                    {linkedSpecimens.length !== 1 ? "s" : ""}
                  </span>
                </div>
                <p className="mt-2 text-sm text-charcoal-600">
                  {m.definition}
                </p>
                <p className="mt-1 text-xs text-charcoal-400">
                  {m.problemItSolves}
                </p>
                {linkedSpecimens.length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {linkedSpecimens.slice(0, 6).map((s) => (
                      <span
                        key={s.id}
                        className="rounded bg-sage-50 px-2 py-0.5 text-[10px] text-sage-700"
                      >
                        {s.name}
                      </span>
                    ))}
                    {linkedSpecimens.length > 6 && (
                      <span className="text-[10px] text-charcoal-400">
                        +{linkedSpecimens.length - 6} more
                      </span>
                    )}
                  </div>
                )}
              </Link>
            );
          })}
        </div>
      </section>

      {/* Candidate Mechanisms */}
      {mechanismData.candidates.length > 0 && (
        <section>
          <h2 className="mb-4 font-serif text-xl text-charcoal-600">
            Emerging Principles ({mechanismData.candidates.length})
          </h2>
          <p className="mb-4 text-sm text-charcoal-400">
            Principles emerging from some specimens but not yet confirmed across
            enough cases.
          </p>
          <div className="space-y-3">
            {mechanismData.candidates.map((c, i) => (
              <div
                key={i}
                className="rounded-lg border border-dashed border-sage-300 bg-cream-50 p-4"
              >
                <h3 className="font-serif text-base font-medium text-charcoal-600">
                  {c.name}
                </h3>
                <p className="mt-1 text-sm text-charcoal-500">{c.hypothesis}</p>
                <p className="mt-1 text-xs text-charcoal-400">
                  Evidence needed: {c.evidenceNeeded}
                </p>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
