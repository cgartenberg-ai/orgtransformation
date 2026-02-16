import Link from "next/link";
import { getFindings, getPrimitives } from "@/lib/data/synthesis";
import { getAllSpecimens } from "@/lib/data/specimens";

export const metadata = {
  title: "Consolidated Findings — Field Guide to AI Organizations",
  description: "10 core findings from systematic observation of how organizations structure for AI",
};

const PRIMITIVE_COLORS: Record<string, string> = {
  P1: "bg-forest-50 text-forest",
  P2: "bg-amber-50 text-amber-700",
  P3: "bg-violet-50 text-violet-700",
  P4: "bg-sky-50 text-sky-700",
  P5: "bg-rose-50 text-rose-700",
};

const MATURITY_COLORS: Record<string, string> = {
  confirmed: "bg-forest-50 text-forest",
  emerging: "bg-amber-50 text-amber-700",
  hypothesis: "bg-rose-50 text-rose-600",
};

export default async function FindingsPage() {
  const [findingData, primitiveData, specimens] = await Promise.all([
    getFindings(),
    getPrimitives(),
    getAllSpecimens(),
  ]);

  const primitiveLookup = Object.fromEntries(
    primitiveData.primitives.map((p) => [p.shortId, p])
  );

  return (
    <div className="space-y-10">
      <header>
        <p className="font-mono text-xs uppercase tracking-[0.2em] text-sage-500">
          Converged Analysis
        </p>
        <h1 className="mt-2 font-serif text-3xl font-semibold text-forest">
          Consolidated Findings
        </h1>
        <p className="mt-2 max-w-3xl text-charcoal-500">
          78 field insights converged into 10 core findings that do genuine theoretical work.
          Each finding is grounded in the{" "}
          <Link href="/framework" className="text-forest underline">
            5 primitives
          </Link>
          , generates testable predictions, and is supported by multiple specimens.
        </p>
      </header>

      {/* Findings */}
      {findingData.findings.map((f) => {
        const evidenceSpecimens = f.evidence.map((e) => {
          const spec = specimens.find((s) => s.id === e.specimenId);
          return { ...e, name: spec?.name ?? e.specimenId };
        });

        return (
          <section
            key={f.id}
            id={f.id}
            className="rounded-lg border border-sage-200 bg-cream-50 p-6"
          >
            {/* Title row */}
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className="rounded bg-forest px-2 py-0.5 font-mono text-xs font-bold text-cream">
                    F{f.number}
                  </span>
                  <h2 className="font-serif text-xl font-medium text-forest">
                    {f.title}
                  </h2>
                </div>
              </div>
              <span className={`shrink-0 rounded px-2 py-0.5 text-[10px] font-medium ${MATURITY_COLORS[f.maturity]}`}>
                {f.maturity}
              </span>
            </div>

            {/* Primitives engaged */}
            <div className="mt-3 flex flex-wrap items-center gap-2">
              <span className="text-[10px] font-medium uppercase tracking-wide text-charcoal-400">
                Primitives:
              </span>
              {f.primitivesEngaged.map((pid) => {
                const prim = primitiveLookup[pid];
                return (
                  <Link
                    key={pid}
                    href="/framework"
                    className={`rounded px-2 py-0.5 font-mono text-[10px] font-bold transition-opacity hover:opacity-80 ${PRIMITIVE_COLORS[pid] || "bg-sage-50 text-sage-700"}`}
                    title={prim?.name ?? pid}
                  >
                    {pid} {prim?.name ?? ""}
                  </Link>
                );
              })}
              {f.paperLink && (
                <>
                  <span className="text-charcoal-300">&middot;</span>
                  <span className="text-[10px] text-charcoal-400">
                    {f.paperLink.replace("paper-", "Paper ").replace(/-/g, " ")}
                  </span>
                </>
              )}
            </div>

            {/* Claim */}
            <div className="mt-4">
              <p className="text-sm leading-relaxed text-charcoal-700">
                {f.claim}
              </p>
            </div>

            {/* Mechanism */}
            <div className="mt-4 rounded border-l-4 border-l-amber bg-white p-3">
              <p className="text-[10px] font-medium uppercase tracking-wide text-charcoal-400">
                Mechanism
              </p>
              <p className="mt-1 text-xs leading-relaxed text-charcoal-600">
                {f.mechanism}
              </p>
            </div>

            {/* Evidence */}
            <div className="mt-4">
              <p className="text-[10px] font-medium uppercase tracking-wide text-charcoal-400">
                Key Evidence ({evidenceSpecimens.length} specimens)
              </p>
              <div className="mt-2 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
                {evidenceSpecimens.slice(0, 9).map((e) => (
                  <Link
                    key={e.specimenId}
                    href={`/specimens/${e.specimenId}`}
                    className="block rounded border border-sage-100 bg-white p-2.5 transition-colors hover:border-forest-50"
                  >
                    <p className="text-xs font-medium text-forest">{e.name}</p>
                    {e.note && (
                      <p className="mt-0.5 line-clamp-2 text-[10px] text-charcoal-500">
                        {e.note}
                      </p>
                    )}
                  </Link>
                ))}
              </div>
              {evidenceSpecimens.length > 9 && (
                <p className="mt-2 text-[10px] text-charcoal-400">
                  +{evidenceSpecimens.length - 9} more specimens
                </p>
              )}
            </div>

            {/* Testable implications */}
            {f.testableImplications.length > 0 && (
              <div className="mt-4">
                <p className="text-[10px] font-medium uppercase tracking-wide text-charcoal-400">
                  Testable Implications
                </p>
                <ul className="mt-1 space-y-0.5">
                  {f.testableImplications.map((impl, i) => (
                    <li key={i} className="text-xs text-charcoal-500">
                      &bull; {impl}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Former insights */}
            <div className="mt-4 border-t border-sage-100 pt-3">
              <p className="text-[10px] text-charcoal-400">
                Subsumes {f.formerInsights.length} former insight{f.formerInsights.length !== 1 ? "s" : ""}:{" "}
                <span className="font-mono">
                  {f.formerInsights.join(", ")}
                </span>
              </p>
            </div>
          </section>
        );
      })}

      {/* Field Observations */}
      {findingData.fieldObservations.length > 0 && (
        <section>
          <h2 className="mb-4 font-serif text-xl text-forest">
            Field Observations ({findingData.fieldObservations.length})
          </h2>
          <p className="mb-4 text-sm text-charcoal-500">
            Valid empirical patterns that don&apos;t rise to findings yet but may become analytically
            important as the collection grows. The botanist&apos;s field notes.
          </p>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-sage-200">
                  <th className="pb-2 pr-4 font-medium text-charcoal-400">Observation</th>
                  <th className="pb-2 pr-4 font-medium text-charcoal-400">Why Preserved</th>
                  <th className="pb-2 font-medium text-charcoal-400">Potential Relevance</th>
                </tr>
              </thead>
              <tbody>
                {findingData.fieldObservations.map((obs) => (
                  <tr key={obs.id} className="border-b border-sage-100">
                    <td className="py-2 pr-4 text-charcoal-700">{obs.observation}</td>
                    <td className="py-2 pr-4 text-charcoal-500">{obs.whyPreserved}</td>
                    <td className="py-2 text-charcoal-500">{obs.potentialRelevance}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}
    </div>
  );
}
