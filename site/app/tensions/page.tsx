import { getAllSpecimens } from "@/lib/data/specimens";
import { getTensions, getContingencies } from "@/lib/data/synthesis";
import type { TensionPositions } from "@/lib/types/specimen";
import { TensionMap } from "@/components/visualizations/TensionMap";
import Link from "next/link";

export const metadata = {
  title: "Tension Map — Field Guide to AI Organizations",
  description:
    "Explore where organizations sit on key structural tensions",
};

export default async function TensionsPage() {
  const [specimens, tensionData, contingencyData] = await Promise.all([
    getAllSpecimens(),
    getTensions(),
    getContingencies(),
  ]);

  const active = specimens.filter((s) => s.meta.status !== "Archived");

  return (
    <div className="space-y-8">
      <header>
        <h1 className="font-serif text-3xl font-semibold text-forest">
          Tension Map
        </h1>
        <p className="mt-2 text-charcoal-500">
          Organizations navigate 5 core structural tensions differently. Select
          a tension to see where specimens fall on the spectrum. Hover over a
          node to preview, click to view the full specimen.
        </p>
      </header>

      <TensionMap specimens={active} tensions={tensionData.tensions} />

      {/* Tension reference */}
      <section>
        <h2 className="mb-4 font-serif text-xl text-forest">
          The 5 Core Tensions
        </h2>
        <div className="space-y-6">
          {tensionData.tensions.map((t) => {
            // Compute model clustering for this tension
            const fieldName = t.fieldName as keyof TensionPositions;
            const positioned = active.filter((s) => {
              const val = s.tensionPositions[fieldName];
              return val !== null && val !== undefined;
            });
            const negativeSpecimens = positioned.filter(
              (s) => (s.tensionPositions[fieldName] as number) < -0.2
            );
            const positiveSpecimens = positioned.filter(
              (s) => (s.tensionPositions[fieldName] as number) > 0.2
            );

            // Model distribution on each pole
            const negModels: Record<number, number> = {};
            for (const s of negativeSpecimens) {
              const m = s.classification.structuralModel;
              if (m) negModels[m] = (negModels[m] || 0) + 1;
            }
            const posModels: Record<number, number> = {};
            for (const s of positiveSpecimens) {
              const m = s.classification.structuralModel;
              if (m) posModels[m] = (posModels[m] || 0) + 1;
            }

            // Find connected contingencies
            const connectedContingencies = (t.connectedContingencies ?? [])
              .map((cc) => {
                const contingency = contingencyData.contingencies.find(
                  (c) => c.id === cc.contingencyId
                );
                return contingency
                  ? { contingencyId: cc.contingencyId, relationship: cc.relationship, contingency }
                  : null;
              })
              .filter(
                (cc): cc is { contingencyId: string; relationship: string; contingency: typeof contingencyData.contingencies[number] } =>
                  cc !== null
              );

            return (
              <div
                key={t.id}
                className="rounded-lg border border-sage-200 bg-cream-50 p-5"
              >
                <h3 className="font-serif text-lg font-medium text-forest">
                  {t.name}
                </h3>
                <p className="mt-1 text-sm text-charcoal-600">{t.tradeoff}</p>

                {/* Poles */}
                <div className="mt-3 grid gap-2 md:grid-cols-2">
                  <div className="rounded bg-forest-50 p-3">
                    <span className="text-xs font-medium text-forest">
                      {t.whenNegative.label}
                    </span>
                    <ul className="mt-1 space-y-0.5">
                      {t.whenNegative.conditions.map((c, i) => (
                        <li key={i} className="text-xs text-charcoal-500">
                          {c}
                        </li>
                      ))}
                    </ul>
                    {/* Model clustering on negative pole */}
                    {Object.keys(negModels).length > 0 && (
                      <div className="mt-2 flex flex-wrap gap-1">
                        {Object.entries(negModels)
                          .sort(([, a], [, b]) => b - a)
                          .map(([model, count]) => (
                            <span
                              key={model}
                              className="rounded bg-forest-100 px-1.5 py-0.5 font-mono text-[10px] text-forest-700"
                            >
                              M{model} ({count})
                            </span>
                          ))}
                      </div>
                    )}
                  </div>
                  <div className="rounded bg-amber-50 p-3">
                    <span className="text-xs font-medium text-amber-700">
                      {t.whenPositive.label}
                    </span>
                    <ul className="mt-1 space-y-0.5">
                      {t.whenPositive.conditions.map((c, i) => (
                        <li key={i} className="text-xs text-charcoal-500">
                          {c}
                        </li>
                      ))}
                    </ul>
                    {/* Model clustering on positive pole */}
                    {Object.keys(posModels).length > 0 && (
                      <div className="mt-2 flex flex-wrap gap-1">
                        {Object.entries(posModels)
                          .sort(([, a], [, b]) => b - a)
                          .map(([model, count]) => (
                            <span
                              key={model}
                              className="rounded bg-amber-100 px-1.5 py-0.5 font-mono text-[10px] text-amber-700"
                            >
                              M{model} ({count})
                            </span>
                          ))}
                      </div>
                    )}
                  </div>
                </div>

                {/* Drivers */}
                {t.drivers && (
                  <div className="mt-4">
                    <h4 className="text-xs font-medium uppercase tracking-wide text-charcoal-400">
                      What Drives This Choice
                    </h4>
                    <p className="mt-1 text-sm leading-relaxed text-charcoal-600">
                      {t.drivers}
                    </p>
                  </div>
                )}

                {/* Connected Contingencies */}
                {connectedContingencies.length > 0 && (
                  <div className="mt-4">
                    <h4 className="text-xs font-medium uppercase tracking-wide text-charcoal-400">
                      Connected Contingencies
                    </h4>
                    <div className="mt-2 space-y-2">
                      {connectedContingencies.map((cc) => (
                        <Link
                          key={cc.contingencyId}
                          href="/contingencies"
                          className="block rounded border border-sage-200 bg-white p-3 transition-shadow hover:shadow-sm"
                        >
                          <span className="text-sm font-medium text-forest">
                            {cc.contingency.name}
                          </span>
                          <p className="mt-0.5 text-xs text-charcoal-500">
                            {cc.relationship}
                          </p>
                        </Link>
                      ))}
                    </div>
                  </div>
                )}

                {/* Interpretive Note */}
                {t.interpretiveNote && (
                  <div className="mt-4 rounded border-l-4 border-l-amber bg-white p-3">
                    <h4 className="text-xs font-medium uppercase tracking-wide text-charcoal-400">
                      Interpretive Note
                    </h4>
                    <p className="mt-1 text-sm italic leading-relaxed text-charcoal-600">
                      {t.interpretiveNote}
                    </p>
                  </div>
                )}

                {/* Positioned specimens count */}
                <p className="mt-3 text-[10px] uppercase tracking-wide text-charcoal-400">
                  {positioned.length} specimens positioned &middot;{" "}
                  {negativeSpecimens.length} lean negative &middot;{" "}
                  {positiveSpecimens.length} lean positive
                </p>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}
