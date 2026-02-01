import { getComputedStats } from "@/lib/data/specimens";
import { getMechanisms } from "@/lib/data/synthesis";

export const metadata = {
  title: "About — Ambidexterity Field Guide",
  description: "The botanist's approach to documenting organizational ambidexterity",
};

export default async function AboutPage() {
  const [stats, mechanisms] = await Promise.all([
    getComputedStats(),
    getMechanisms(),
  ]);

  return (
    <div className="mx-auto max-w-3xl space-y-10">
      <header>
        <h1 className="font-serif text-3xl font-semibold text-forest">
          About This Field Guide
        </h1>
      </header>

      <section className="space-y-4">
        <h2 className="font-serif text-xl text-forest">
          The Botanist&rsquo;s Lens
        </h2>
        <p className="leading-relaxed text-charcoal-700">
          This is a <strong>field guide</strong>, not a framework. Where
          consulting frameworks tell leaders what they should do, a field guide
          documents what organizations actually do.
        </p>
        <p className="leading-relaxed text-charcoal-700">
          Like a botanical field guide that catalogs plant species with detailed
          descriptions, habitat notes, and identification markers, this resource
          catalogs organizational specimens &mdash; real companies navigating the
          exploration/execution tension in the AI era.
        </p>
      </section>

      <section className="space-y-4">
        <h2 className="font-serif text-xl text-forest">
          The Botanist&rsquo;s Job
        </h2>
        <ul className="ml-4 list-disc space-y-2 text-charcoal-700">
          <li>
            Observe organizational specimens in their natural habitat
          </li>
          <li>
            Document structural forms with rich, sourced detail
          </li>
          <li>Classify specimens by their characteristics</li>
          <li>
            Note the conditions under which each form thrives
          </li>
          <li>Let patterns emerge from careful observation</li>
        </ul>
      </section>

      <section className="space-y-4">
        <h2 className="font-serif text-xl text-forest">
          What This Is Not
        </h2>
        <ul className="ml-4 list-disc space-y-2 text-charcoal-600">
          <li>A maturity model or scoring system</li>
          <li>A prescriptive methodology</li>
          <li>
            A consulting framework with &ldquo;best practices&rdquo;
          </li>
          <li>A tool that tells leaders what to do</li>
        </ul>
      </section>

      <section className="space-y-4">
        <h2 className="font-serif text-xl text-forest">The Core Tension</h2>
        <p className="leading-relaxed text-charcoal-700">
          Every organization faces the same fundamental challenge:{" "}
          <strong>
            how to simultaneously explore new possibilities while executing on
            current commitments.
          </strong>
        </p>
        <p className="leading-relaxed text-charcoal-700">
          This is the ambidexterity challenge, first articulated by
          organizational scholars studying how firms survive technological
          disruption. In the AI era, this tension has become acute.
        </p>
        <div className="grid gap-4 md:grid-cols-2">
          <div className="rounded-lg border border-sage-200 bg-cream-50 p-4">
            <h3 className="font-serif text-base font-medium text-forest">
              Exploration
            </h3>
            <p className="mt-1 text-sm text-charcoal-600">
              Experimenting with AI capabilities, developing new offerings,
              building for an uncertain future.
            </p>
          </div>
          <div className="rounded-lg border border-sage-200 bg-cream-50 p-4">
            <h3 className="font-serif text-base font-medium text-forest">
              Execution
            </h3>
            <p className="mt-1 text-sm text-charcoal-600">
              Running the business, serving existing customers, delivering on
              current commitments with operational excellence.
            </p>
          </div>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="font-serif text-xl text-forest">Methodology</h2>
        <p className="leading-relaxed text-charcoal-700">
          The field guide is built through a three-phase research workflow:
        </p>
        <div className="space-y-3">
          <MethodologyStep
            number={1}
            title="Field Work (Research)"
            description="Scan sources systematically. Gather observations about organizations — wide and deep. Record raw findings with full source provenance."
          />
          <MethodologyStep
            number={2}
            title="Curation (Classification)"
            description="Apply the 7-model taxonomy. Assign ambidexterity orientation. Structure findings into specimen cards. Link to relevant mechanisms."
          />
          <MethodologyStep
            number={3}
            title="Synthesis (Patterns)"
            description="Identify mechanisms that appear across multiple specimens. Surface tensions and trade-offs. Update mechanism descriptions with new examples."
          />
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="font-serif text-xl text-forest">
          Theoretical Foundation
        </h2>
        <p className="leading-relaxed text-charcoal-700">
          This field guide draws on organizational ambidexterity research,
          particularly the work of Charles O&rsquo;Reilly and Michael Tushman,
          while remaining accessible to practitioners.
        </p>
        <p className="text-sm text-charcoal-600">
          <em>
            Note on language: The academic literature uses
            &ldquo;exploitation&rdquo; to describe leveraging existing
            capabilities. We use &ldquo;execution&rdquo; for clarity &mdash; it
            captures the same concept without the negative connotations.
          </em>
        </p>
      </section>

      <section className="rounded-lg border border-sage-200 bg-cream-50 p-6">
        <h2 className="mb-4 font-serif text-xl text-forest">
          Collection Status
        </h2>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          <div className="text-center">
            <p className="font-serif text-2xl font-semibold text-forest">
              {stats.totalSpecimens}
            </p>
            <p className="text-xs text-charcoal-400">Specimens</p>
          </div>
          <div className="text-center">
            <p className="font-serif text-2xl font-semibold text-forest">
              {Object.keys(stats.byModel).length}
            </p>
            <p className="text-xs text-charcoal-400">Structural Models</p>
          </div>
          <div className="text-center">
            <p className="font-serif text-2xl font-semibold text-forest">
              {mechanisms.confirmed.length}
            </p>
            <p className="text-xs text-charcoal-400">Mechanisms</p>
          </div>
          <div className="text-center">
            <p className="font-serif text-2xl font-semibold text-forest">
              {stats.industries.length}
            </p>
            <p className="text-xs text-charcoal-400">Industries</p>
          </div>
        </div>
      </section>
    </div>
  );
}

function MethodologyStep({
  number,
  title,
  description,
}: {
  number: number;
  title: string;
  description: string;
}) {
  return (
    <div className="flex gap-4 rounded-lg border border-sage-200 bg-cream-50 p-4">
      <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-forest font-mono text-sm font-medium text-cream">
        {number}
      </span>
      <div>
        <h3 className="font-serif text-base font-medium text-forest">
          {title}
        </h3>
        <p className="mt-1 text-sm text-charcoal-600">{description}</p>
      </div>
    </div>
  );
}
