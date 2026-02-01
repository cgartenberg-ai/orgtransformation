import { getAllSpecimens } from "@/lib/data/specimens";
import { ComparisonView } from "@/components/compare/ComparisonView";

export const metadata = {
  title: "Compare Specimens — Ambidexterity Field Guide",
  description: "Side-by-side comparison of up to 4 organizational specimens",
};

export default async function ComparePage() {
  const specimens = await getAllSpecimens();
  const active = specimens.filter((s) => s.meta.status !== "Archived");

  return (
    <div className="space-y-6">
      <header>
        <h1 className="font-serif text-3xl font-semibold text-forest">
          Compare Specimens
        </h1>
        <p className="mt-2 text-charcoal-500">
          Select up to 4 specimens to compare side-by-side across
          classification, contingencies, tension positions, and mechanisms.
        </p>
      </header>

      <ComparisonView allSpecimens={active} />
    </div>
  );
}
