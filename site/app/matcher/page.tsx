import { getAllSpecimens } from "@/lib/data/specimens";
import { MatcherForm } from "@/components/matcher/MatcherForm";

export const metadata = {
  title: "Situation Matcher — Ambidexterity Field Guide",
  description:
    "Find organizations facing constraints like yours",
};

export default async function MatcherPage() {
  const specimens = await getAllSpecimens();
  const active = specimens.filter((s) => s.meta.status !== "Archived");

  return (
    <div className="space-y-6">
      <header>
        <h1 className="font-serif text-3xl font-semibold text-forest">
          Situation Matcher
        </h1>
        <p className="mt-2 text-charcoal-500">
          Describe your organizational context and we&rsquo;ll find specimens
          facing similar constraints. Matching is transparent &mdash; click
          &ldquo;Why?&rdquo; on any result to see exactly how it scored.
        </p>
      </header>

      <MatcherForm specimens={active} />
    </div>
  );
}
