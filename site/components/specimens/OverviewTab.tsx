import type { Specimen } from "@/lib/types/specimen";
import { QuoteBlock } from "@/components/shared/QuoteBlock";

export function OverviewTab({ specimen }: { specimen: Specimen }) {
  const markers = specimen.observableMarkers;
  const contingencies = specimen.contingencies;

  return (
    <div className="space-y-8">
      {/* Description */}
      <section>
        <p className="whitespace-pre-line text-base leading-relaxed text-charcoal-700">
          {specimen.description}
        </p>
      </section>

      {/* Key Quote */}
      {specimen.quotes.length > 0 && (
        <section>
          <h3 className="mb-3 font-serif text-lg text-forest">Key Quote</h3>
          <QuoteBlock quote={specimen.quotes[0]} />
          {specimen.quotes.length > 1 && (
            <div className="mt-4 space-y-3">
              {specimen.quotes.slice(1).map((q, i) => (
                <QuoteBlock key={i} quote={q} />
              ))}
            </div>
          )}
        </section>
      )}

      {/* Observable Markers */}
      {Object.values(markers).some(Boolean) && (
        <section>
          <h3 className="mb-3 font-serif text-lg text-forest">
            Observable Markers
          </h3>
          <dl className="grid gap-3 md:grid-cols-2">
            {markers.reportingStructure && (
              <MarkerItem label="Reporting Structure" value={markers.reportingStructure} />
            )}
            {markers.resourceAllocation && (
              <MarkerItem label="Resource Allocation" value={markers.resourceAllocation} />
            )}
            {markers.timeHorizons && (
              <MarkerItem label="Time Horizons" value={markers.timeHorizons} />
            )}
            {markers.decisionRights && (
              <MarkerItem label="Decision Rights" value={markers.decisionRights} />
            )}
            {markers.metrics && (
              <MarkerItem label="Metrics" value={markers.metrics} />
            )}
          </dl>
        </section>
      )}

      {/* Contingencies */}
      {Object.values(contingencies).some(Boolean) && (
        <section>
          <h3 className="mb-3 font-serif text-lg text-forest">
            Contingency Profile
          </h3>
          <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
            {contingencies.regulatoryIntensity && (
              <ContingencyItem
                label="Regulatory Intensity"
                value={contingencies.regulatoryIntensity}
              />
            )}
            {contingencies.timeToObsolescence && (
              <ContingencyItem
                label="Time to Obsolescence"
                value={contingencies.timeToObsolescence}
              />
            )}
            {contingencies.ceoTenure && (
              <ContingencyItem label="CEO Tenure" value={contingencies.ceoTenure} />
            )}
            {contingencies.talentMarketPosition && (
              <ContingencyItem
                label="Talent Position"
                value={contingencies.talentMarketPosition}
              />
            )}
            {contingencies.technicalDebt && (
              <ContingencyItem
                label="Technical Debt"
                value={contingencies.technicalDebt}
              />
            )}
          </div>
        </section>
      )}

      {/* Classification Rationale */}
      {specimen.classification.classificationRationale && (
        <section>
          <h3 className="mb-2 font-serif text-lg text-forest">
            Classification Rationale
          </h3>
          <p className="text-sm leading-relaxed text-charcoal-600">
            {specimen.classification.classificationRationale}
          </p>
        </section>
      )}

      {/* Open Questions */}
      {specimen.openQuestions && specimen.openQuestions.length > 0 && (
        <section>
          <h3 className="mb-2 font-serif text-lg text-forest">
            Open Questions
          </h3>
          <ul className="list-inside list-disc space-y-1 text-sm text-charcoal-600">
            {specimen.openQuestions.map((q, i) => (
              <li key={i}>{q}</li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}

function MarkerItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded border border-sage-200 bg-cream-50 p-3">
      <dt className="text-xs font-medium uppercase tracking-wide text-charcoal-400">
        {label}
      </dt>
      <dd className="mt-1 text-sm text-charcoal-700">{value}</dd>
    </div>
  );
}

function ContingencyItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between rounded border border-sage-200 bg-cream-50 px-3 py-2">
      <span className="text-xs text-charcoal-500">{label}</span>
      <span className="rounded bg-forest-50 px-2 py-0.5 font-mono text-xs font-medium text-forest">
        {value}
      </span>
    </div>
  );
}
