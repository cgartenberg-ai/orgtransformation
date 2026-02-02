import { getAllSpecimens, getComputedStats } from "@/lib/data/specimens";
import { getMechanisms } from "@/lib/data/synthesis";
import { STRUCTURAL_MODELS } from "@/lib/types/taxonomy";
import type { StructuralModel } from "@/lib/types/specimen";
import { FieldObservation } from "@/components/home/FieldObservation";
import Link from "next/link";

export default async function HomePage() {
  const [stats, specimens, mechanismData] = await Promise.all([
    getComputedStats(),
    getAllSpecimens(),
    getMechanisms(),
  ]);

  const typeSpecimens = specimens.filter((s) => s.classification.typeSpecimen);

  // Prepare patterns for FieldObservation — prefer evidence quotes, fall back to problemItSolves
  const eligiblePatterns = mechanismData.confirmed
    .filter((m) => m.specimens.length >= 2)
    .map((m) => {
      const evidenceWithQuote = m.evidence.find((e) => e.quote);
      return {
        id: m.id,
        name: m.name,
        problemItSolves: m.problemItSolves,
        specimensCount: m.specimens.length,
        quote: evidenceWithQuote?.quote ?? null,
        speaker: evidenceWithQuote?.speaker ?? null,
      };
    });

  return (
    <div className="-mx-4 -mt-8 sm:-mx-6 lg:-mx-8">
      {/* ═══════════════════════════════════════════════════════════
          Section 1: Hero — Full-bleed forest background
          ═══════════════════════════════════════════════════════════ */}
      <section className="relative overflow-hidden bg-forest px-4 py-24 text-center sm:px-6 lg:px-8">
        {/* Subtle botanical texture overlay */}
        <div className="absolute inset-0 opacity-[0.07]" style={{
          backgroundImage: `radial-gradient(circle at 20% 50%, #84A98C 1px, transparent 1px),
                            radial-gradient(circle at 80% 20%, #84A98C 1px, transparent 1px),
                            radial-gradient(circle at 50% 80%, #84A98C 1px, transparent 1px)`,
          backgroundSize: '60px 60px, 80px 80px, 70px 70px',
        }} />
        <div className="relative mx-auto max-w-3xl">
          <p className="font-mono text-xs uppercase tracking-[0.3em] text-sage-300">
            A Research-Backed Collection
          </p>
          <h1 className="mt-4 font-serif text-4xl font-semibold leading-tight text-cream lg:text-5xl xl:text-6xl">
            A Field Guide to{" "}
            <span className="text-amber-300">AI Organization</span>
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg leading-relaxed text-sage-200">
            Like a botanist cataloging species in the wild, we&rsquo;ve
            documented{" "}
            <span className="font-semibold text-cream">
              {stats.totalSpecimens} organizations
            </span>{" "}
            and the structural forms they&rsquo;ve evolved to navigate the AI
            era. Browse the collection. Find your species. See what thrives.
          </p>
          <div className="mt-10 flex flex-col justify-center gap-4 sm:flex-row">
            <Link
              href="/specimens"
              className="rounded-lg bg-amber px-8 py-3.5 font-serif text-sm font-semibold text-forest-900 shadow-lg transition-all hover:bg-amber-300 hover:shadow-xl"
            >
              Enter the Herbarium
            </Link>
            <Link
              href="/matcher"
              className="rounded-lg border-2 border-sage-400 px-8 py-3.5 font-serif text-sm font-semibold text-cream transition-all hover:border-cream hover:bg-cream/10"
            >
              Find Your Match
            </Link>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════
          Section 2: Seven Structural Species
          ═══════════════════════════════════════════════════════════ */}
      <section className="bg-cream-50 px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <div className="text-center">
            <p className="font-mono text-xs uppercase tracking-[0.2em] text-sage-500">
              The Taxonomy
            </p>
            <h2 className="mt-2 font-serif text-3xl font-semibold text-forest">
              Seven Structural Species
            </h2>
            <p className="mx-auto mt-3 max-w-lg text-charcoal-500">
              Every organization in the collection fits one of these forms.
              Select a species to see its specimens.
            </p>
          </div>
          <div className="mt-10 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
            {([1, 2, 3, 4, 5, 6, 7] as StructuralModel[]).map((model) => {
              const info = STRUCTURAL_MODELS[model];
              const count = stats.byModel[String(model)] ?? 0;
              return (
                <Link
                  key={model}
                  href={`/specimens?model=${model}`}
                  className="group relative rounded-xl border border-sage-200 bg-white p-5 shadow-sm transition-all hover:-translate-y-1 hover:shadow-md"
                >
                  {/* Color accent bar */}
                  <div className="absolute left-0 top-0 h-1 w-full rounded-t-xl bg-gradient-to-r from-forest to-sage-400" />
                  <p className="mt-1 font-mono text-xs text-sage-500">
                    {info.shortName}
                  </p>
                  <p className="mt-1 font-serif text-lg font-semibold text-forest group-hover:text-forest-600">
                    {info.name}
                  </p>
                  <p className="mt-1 text-sm leading-snug text-charcoal-500">
                    {info.description}
                  </p>
                  <div className="mt-3 flex items-center gap-1.5">
                    <span className="inline-flex h-5 w-5 items-center justify-center rounded-full bg-forest-50 font-mono text-[10px] font-semibold text-forest">
                      {count}
                    </span>
                    <span className="text-xs text-charcoal-400">collected</span>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════
          Section 3: Type Specimens — The Centerpiece
          ═══════════════════════════════════════════════════════════ */}
      <section className="bg-cream-100 px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <div className="text-center">
            <p className="font-mono text-xs uppercase tracking-[0.2em] text-amber-600">
              The Reference Collection
            </p>
            <h2 className="mt-2 font-serif text-3xl font-semibold text-forest">
              Type Specimens
            </h2>
            <p className="mx-auto mt-3 max-w-lg text-charcoal-500">
              The reference example of each species &mdash; the clearest,
              best-documented case in the collection.
            </p>
          </div>
          <div className="mt-10 grid gap-6 lg:grid-cols-2">
            {typeSpecimens.map((s) => {
              const modelInfo = s.classification.structuralModel
                ? STRUCTURAL_MODELS[s.classification.structuralModel]
                : null;
              const keyQuote =
                s.quotes?.[0]?.text ?? s.description.slice(0, 200) + "...";
              const quoteSpeaker = s.quotes?.[0]?.speaker ?? null;

              const classificationParts = [
                modelInfo ? modelInfo.name : null,
                s.classification.orientation,
                s.habitat.industry,
              ].filter(Boolean);

              const habitatParts = [
                s.habitat.employees
                  ? `${s.habitat.employees.toLocaleString()} employees`
                  : null,
                s.habitat.revenue ? `${s.habitat.revenue} revenue` : null,
                s.habitat.headquarters,
              ].filter(Boolean);

              return (
                <Link
                  key={s.id}
                  href={`/specimens/${s.id}`}
                  className="group relative block overflow-hidden rounded-xl bg-white shadow-sm transition-all hover:-translate-y-1 hover:shadow-lg"
                >
                  {/* Amber top border — like a specimen label strip */}
                  <div className="h-2 bg-gradient-to-r from-amber-300 via-amber to-amber-300" />
                  <div className="p-7">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <span className="inline-block rounded-full bg-amber-100 px-3 py-1 font-mono text-[10px] font-bold uppercase tracking-widest text-amber-800">
                          Type Specimen
                        </span>
                        <h3 className="mt-3 font-serif text-2xl font-semibold text-forest group-hover:text-forest-600">
                          {s.name}
                        </h3>
                        <p className="mt-0.5 text-base text-charcoal-500">
                          {s.title}
                        </p>
                      </div>
                    </div>

                    <div className="mt-4 flex flex-wrap gap-2">
                      {classificationParts.map((part, i) => (
                        <span
                          key={i}
                          className="rounded-full bg-sage-50 px-2.5 py-0.5 text-xs text-sage-700"
                        >
                          {part}
                        </span>
                      ))}
                    </div>
                    {habitatParts.length > 0 && (
                      <p className="mt-2 font-mono text-xs text-charcoal-400">
                        {habitatParts.join("  ·  ")}
                      </p>
                    )}

                    <blockquote className="mt-5 rounded-lg bg-amber-50/60 p-4">
                      <p className="font-serif text-sm italic leading-relaxed text-charcoal-700">
                        &ldquo;{keyQuote}&rdquo;
                      </p>
                      {quoteSpeaker && (
                        <p className="mt-2 text-right text-xs font-medium text-amber-700">
                          &mdash; {quoteSpeaker}
                        </p>
                      )}
                    </blockquote>

                    <p className="mt-5 text-sm font-semibold text-forest group-hover:underline">
                      View full specimen &rarr;
                    </p>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════════
          Section 4: Collection Summary
          ═══════════════════════════════════════════════════════════ */}
      <section className="bg-forest px-4 py-10 text-center sm:px-6 lg:px-8">
        <p className="text-sm leading-relaxed text-sage-200">
          The collection spans{" "}
          <span className="font-semibold text-amber-300">
            {stats.industries.length} industries
          </span>{" "}
          &mdash; from pharma giants and banks to AI startups and government
          agencies.{" "}
          <span className="font-semibold text-amber-300">
            {mechanismData.confirmed.length} structural principles
          </span>{" "}
          documented. Last field update:{" "}
          <span className="text-cream">
            {new Date(stats.lastUpdated).toLocaleDateString("en-US", {
              month: "short",
              day: "numeric",
            })}
          </span>
          .
        </p>
      </section>

      {/* ═══════════════════════════════════════════════════════════
          Section 5: Rotating Field Observation
          ═══════════════════════════════════════════════════════════ */}
      <div className="bg-cream-50 px-4 py-16 sm:px-6 lg:px-8">
        <FieldObservation patterns={eligiblePatterns} />
      </div>
    </div>
  );
}
