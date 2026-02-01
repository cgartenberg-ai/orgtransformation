import { getAllSpecimens, getComputedStats } from "@/lib/data/specimens";
import { SpecimenBrowser } from "@/components/specimens/SpecimenBrowser";

export const metadata = {
  title: "Specimens — Ambidexterity Field Guide",
  description: "Browse all organizational specimens in the field guide",
};

export default async function SpecimensPage() {
  const [specimens, stats] = await Promise.all([
    getAllSpecimens(),
    getComputedStats(),
  ]);

  return (
    <div>
      <h1 className="font-serif text-3xl font-semibold text-forest">
        Specimens
      </h1>
      <p className="mt-1 text-sm text-charcoal-500">
        {stats.totalSpecimens} organizations documented across{" "}
        {Object.keys(stats.byModel).length} structural models
      </p>
      <SpecimenBrowser specimens={specimens} industries={stats.industries} />
    </div>
  );
}
