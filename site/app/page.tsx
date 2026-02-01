import { getAllSpecimens, getComputedStats } from "@/lib/data/specimens";
import { getMechanisms } from "@/lib/data/synthesis";
import Link from "next/link";

export default async function HomePage() {
  const [stats, specimens, mechanisms] = await Promise.all([
    getComputedStats(),
    getAllSpecimens(),
    getMechanisms(),
  ]);

  const typeSpecimens = specimens.filter((s) => s.classification.typeSpecimen);

  return (
    <div className="space-y-16">
      {/* Hero */}
      <section className="py-12 text-center">
        <h1 className="mx-auto max-w-3xl font-serif text-3xl font-semibold leading-tight text-forest sm:text-4xl lg:text-5xl">
          How do organizations structurally enable both exploration and execution
          in the AI era?
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-lg text-charcoal-500">
          A field guide documenting{" "}
          <span className="font-semibold text-forest">
            {stats.totalSpecimens}
          </span>{" "}
          organizational specimens across{" "}
          <span className="font-semibold text-forest">7</span> structural models
        </p>
        <div className="mt-8 flex justify-center gap-4">
          <Link
            href="/matcher"
            className="rounded-md bg-forest px-6 py-3 text-sm font-medium text-cream transition-colors hover:bg-forest-700"
          >
            Find Organizations Like Mine
          </Link>
          <Link
            href="/specimens"
            className="rounded-md border border-forest px-6 py-3 text-sm font-medium text-forest transition-colors hover:bg-forest-50"
          >
            Browse Specimens
          </Link>
        </div>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard label="Specimens" value={stats.totalSpecimens} />
        <StatCard label="Structural Models" value={Object.keys(stats.byModel).length} />
        <StatCard label="Mechanisms" value={mechanisms.confirmed.length} />
        <StatCard
          label="Last Updated"
          value={stats.lastUpdated}
          isDate
        />
      </section>

      {/* Distribution by model */}
      <section>
        <h2 className="font-serif text-2xl text-forest">
          Specimen Distribution
        </h2>
        <div className="mt-4 grid grid-cols-2 gap-3 md:grid-cols-4 lg:grid-cols-7">
          {Object.entries(stats.byModel)
            .sort(([a], [b]) => Number(a) - Number(b))
            .map(([model, count]) => (
              <div
                key={model}
                className="rounded-lg border border-sage-200 bg-cream-50 p-4 text-center"
              >
                <p className="font-mono text-xs text-charcoal-400">
                  Model {model}
                </p>
                <p className="mt-1 font-serif text-2xl font-semibold text-forest">
                  {count}
                </p>
              </div>
            ))}
        </div>
      </section>

      {/* Type Specimens */}
      <section>
        <h2 className="font-serif text-2xl text-forest">Type Specimens</h2>
        <p className="mt-1 text-sm text-charcoal-500">
          The clearest reference example of each structural model
        </p>
        <div className="mt-6 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {typeSpecimens.map((s) => (
            <Link
              key={s.id}
              href={`/specimens/${s.id}`}
              className="group rounded-lg border border-amber-200 bg-cream-50 p-5 transition-shadow hover:shadow-md"
            >
              <div className="flex items-start justify-between">
                <h3 className="font-serif text-lg font-semibold text-forest group-hover:text-forest-600">
                  {s.name}
                </h3>
                <span className="rounded-full bg-amber-100 px-2 py-0.5 font-mono text-xs text-amber-700">
                  Type
                </span>
              </div>
              <p className="mt-1 text-sm text-charcoal-500">{s.title}</p>
              <div className="mt-3 flex flex-wrap gap-2">
                <span className="rounded bg-forest-50 px-2 py-0.5 font-mono text-xs text-forest">
                  M{s.classification.structuralModel}
                </span>
                {s.classification.orientation && (
                  <span className="rounded bg-sage-100 px-2 py-0.5 font-mono text-xs text-sage-700">
                    {s.classification.orientation}
                  </span>
                )}
                <span className="rounded bg-charcoal-50 px-2 py-0.5 text-xs text-charcoal-500">
                  {s.habitat.industry}
                </span>
              </div>
              <p className="mt-3 line-clamp-2 text-sm text-charcoal-600">
                {s.description.slice(0, 150)}...
              </p>
            </Link>
          ))}
        </div>
      </section>

      {/* Orientation breakdown */}
      <section>
        <h2 className="font-serif text-2xl text-forest">By Orientation</h2>
        <div className="mt-4 grid grid-cols-3 gap-4">
          {Object.entries(stats.byOrientation)
            .filter(([key]) => key !== "Unknown")
            .map(([orientation, count]) => (
              <div
                key={orientation}
                className="rounded-lg border border-sage-200 bg-cream-50 p-4 text-center"
              >
                <p className="text-sm font-medium text-charcoal-600">
                  {orientation}
                </p>
                <p className="mt-1 font-serif text-2xl font-semibold text-forest">
                  {count}
                </p>
              </div>
            ))}
        </div>
      </section>
    </div>
  );
}

function StatCard({
  label,
  value,
  isDate = false,
}: {
  label: string;
  value: number | string;
  isDate?: boolean;
}) {
  const display = isDate && typeof value === "string"
    ? new Date(value).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      })
    : value;

  return (
    <div className="rounded-lg border border-sage-200 bg-cream-50 p-4 text-center">
      <p className="text-xs font-medium uppercase tracking-wide text-charcoal-400">
        {label}
      </p>
      <p className="mt-1 font-serif text-2xl font-semibold text-forest">
        {display}
      </p>
    </div>
  );
}
