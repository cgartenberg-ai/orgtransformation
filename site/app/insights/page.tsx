import Link from "next/link";
import { getInsights } from "@/lib/data/synthesis";
import { getAllSpecimens } from "@/lib/data/specimens";

const THEME_LABELS: Record<string, { label: string; color: string }> = {
  convergence: { label: "Convergence Pattern", color: "bg-forest-50 text-forest" },
  "organizational-form": { label: "Organizational Form", color: "bg-amber-50 text-amber-700" },
  mechanism: { label: "Mechanism Insight", color: "bg-sage-50 text-sage-700" },
  workforce: { label: "Workforce", color: "bg-violet-50 text-violet-700" },
  methodology: { label: "Methodology", color: "bg-charcoal-100 text-charcoal-600" },
};

export const metadata = {
  title: "Field Insights — Field Guide to AI Organizations",
  description: "Cross-cutting findings from systematic observation of how organizations structure for AI",
};

export default async function InsightsPage() {
  const [insightData, specimens] = await Promise.all([
    getInsights(),
    getAllSpecimens(),
  ]);

  const themes = ["convergence", "organizational-form", "mechanism", "workforce", "methodology"];

  return (
    <div className="space-y-10">
      <header>
        <h1 className="font-serif text-3xl font-semibold text-forest">
          Field Insights
        </h1>
        <p className="mt-2 max-w-3xl text-charcoal-500">
          Cross-cutting findings discovered during synthesis &mdash; patterns that
          span multiple specimens, industries, or mechanisms. These are the
          field guide&apos;s key empirical contributions.
        </p>
      </header>

      {themes.map((theme) => {
        const themeInsights = insightData.insights.filter((i) => i.theme === theme);
        if (themeInsights.length === 0) return null;
        const themeInfo = THEME_LABELS[theme];
        return (
          <section key={theme}>
            <h2 className="mb-4 font-serif text-xl text-forest">
              {themeInfo.label}s ({themeInsights.length})
            </h2>
            <div className="space-y-4">
              {themeInsights.map((insight) => (
                <div
                  key={insight.id}
                  className="rounded-lg border border-sage-200 bg-cream-50 p-5"
                >
                  <div className="flex items-start justify-between gap-3">
                    <h3 className="font-serif text-lg font-medium text-forest">
                      {insight.title}
                    </h3>
                    <div className="flex shrink-0 items-center gap-1.5">
                      <span
                        className={`rounded px-2 py-0.5 text-[10px] font-medium ${
                          insight.maturity === "confirmed"
                            ? "bg-forest-50 text-forest"
                            : insight.maturity === "emerging"
                            ? "bg-amber-50 text-amber-700"
                            : "bg-rose-50 text-rose-600"
                        }`}
                      >
                        {insight.maturity}
                      </span>
                      <span className={`rounded px-2 py-0.5 text-[10px] font-medium ${themeInfo.color}`}>
                        {themeInfo.label}
                      </span>
                    </div>
                  </div>

                  {/* Research target flag for thin evidence */}
                  {insight.maturity === "hypothesis" && (
                    <div className="mt-2 rounded border border-rose-200 bg-rose-50 px-3 py-1.5">
                      <p className="text-[11px] font-medium text-rose-700">
                        Research target — only {insight.evidence.length} specimen{insight.evidence.length !== 1 ? "s" : ""}. Needs more evidence to confirm.
                      </p>
                    </div>
                  )}
                  {insight.maturity === "emerging" && (
                    <div className="mt-2 rounded border border-amber-200 bg-amber-50 px-3 py-1.5">
                      <p className="text-[11px] font-medium text-amber-700">
                        Emerging — {insight.evidence.length} specimens. Look for additional evidence in new research.
                      </p>
                    </div>
                  )}

                  <p className="mt-2 text-sm leading-relaxed text-charcoal-600">
                    {insight.finding}
                  </p>

                  {/* Evidence */}
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {insight.evidence.map((e) => {
                      const specimen = specimens.find((s) => s.id === e.specimenId);
                      return (
                        <Link
                          key={e.specimenId}
                          href={`/specimens/${e.specimenId}`}
                          className="rounded bg-sage-50 px-2 py-0.5 text-[10px] text-sage-700 hover:bg-sage-100"
                          title={e.note}
                        >
                          {specimen?.name ?? e.specimenId}
                        </Link>
                      );
                    })}
                  </div>

                  {/* Theoretical connection */}
                  {insight.theoreticalConnection && (
                    <div className="mt-3 rounded border-l-4 border-l-amber bg-white p-3">
                      <p className="text-xs leading-relaxed text-charcoal-500">
                        {insight.theoreticalConnection}
                      </p>
                    </div>
                  )}

                  {/* Related mechanisms/tensions */}
                  {((insight.relatedMechanisms && insight.relatedMechanisms.length > 0) ||
                    (insight.relatedTensions && insight.relatedTensions.length > 0)) && (
                    <div className="mt-2 flex flex-wrap gap-2">
                      {insight.relatedMechanisms?.map((id) => (
                        <Link
                          key={`m-${id}`}
                          href={`/mechanisms/${id}`}
                          className="text-[10px] text-forest hover:underline"
                        >
                          Principle #{id}
                        </Link>
                      ))}
                      {insight.relatedTensions?.map((id) => (
                        <Link
                          key={`t-${id}`}
                          href="/tensions"
                          className="text-[10px] text-amber-700 hover:underline"
                        >
                          Tension #{id}
                        </Link>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>
        );
      })}
    </div>
  );
}
