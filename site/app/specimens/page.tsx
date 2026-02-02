import { getAllSpecimens, getComputedStats } from "@/lib/data/specimens";
import { SpecimenBrowser } from "@/components/specimens/SpecimenBrowser";

export const metadata = {
  title: "Specimens — Field Guide to AI Organizations",
  description: "Browse all organizational specimens in the field guide",
};

export default async function SpecimensPage({
  searchParams,
}: {
  searchParams: { model?: string };
}) {
  const [specimens, stats] = await Promise.all([
    getAllSpecimens(),
    getComputedStats(),
  ]);

  const initialModel = searchParams.model
    ? (Number(searchParams.model) as 1 | 2 | 3 | 4 | 5 | 6 | 7)
    : null;

  return (
    <div>
      <h1 className="font-serif text-3xl font-semibold text-forest">
        Specimens
      </h1>
      <p className="mt-1 text-sm text-charcoal-500">
        {stats.totalSpecimens} organizations documented across{" "}
        {Object.keys(stats.byModel).length} structural models
      </p>
      <SpecimenBrowser
        specimens={specimens}
        industries={stats.industries}
        initialModel={initialModel}
      />
    </div>
  );
}
