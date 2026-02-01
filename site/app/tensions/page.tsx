import { getAllSpecimens } from "@/lib/data/specimens";
import { getTensions } from "@/lib/data/synthesis";
import { TensionMap } from "@/components/visualizations/TensionMap";

export const metadata = {
  title: "Tension Map — Ambidexterity Field Guide",
  description:
    "Explore where organizations sit on key structural tensions",
};

export default async function TensionsPage() {
  const [specimens, tensionData] = await Promise.all([
    getAllSpecimens(),
    getTensions(),
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
        <div className="space-y-3">
          {tensionData.tensions.map((t) => (
            <div
              key={t.id}
              className="rounded-lg border border-sage-200 bg-cream-50 p-4"
            >
              <h3 className="font-serif text-base font-medium text-forest">
                {t.name}
              </h3>
              <p className="mt-1 text-sm text-charcoal-600">{t.tradeoff}</p>
              <div className="mt-2 grid gap-2 md:grid-cols-2">
                <div className="rounded bg-forest-50 p-2">
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
                </div>
                <div className="rounded bg-amber-50 p-2">
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
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
