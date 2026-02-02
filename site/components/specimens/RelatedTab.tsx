import type { Specimen } from "@/lib/types/specimen";
import { SpecimenCard } from "./SpecimenCard";

export function RelatedTab({
  specimen,
  related,
}: {
  specimen: Specimen;
  related: Specimen[];
}) {
  if (related.length === 0) {
    return (
      <p className="text-sm text-charcoal-400">
        No closely related specimens found.
      </p>
    );
  }

  // Group related specimens by relationship type
  const sameModel = related.filter(
    (r) =>
      r.classification.structuralModel ===
      specimen.classification.structuralModel
  );
  const sameOrientation = related.filter(
    (r) =>
      r.classification.orientation === specimen.classification.orientation &&
      r.classification.structuralModel !==
        specimen.classification.structuralModel
  );
  const sharedMechanisms = related.filter(
    (r) =>
      !sameModel.includes(r) &&
      !sameOrientation.includes(r) &&
      r.mechanisms.some((m) =>
        specimen.mechanisms.some((sm) => sm.id === m.id)
      )
  );

  return (
    <div className="space-y-8">
      {sameModel.length > 0 && (
        <RelatedGroup
          title="Same Structural Model"
          description={`Other organizations classified as Model ${specimen.classification.structuralModel}`}
          specimens={sameModel}
        />
      )}
      {sameOrientation.length > 0 && (
        <RelatedGroup
          title="Same Orientation"
          description={`Other ${specimen.classification.orientation} orientation specimens`}
          specimens={sameOrientation}
        />
      )}
      {sharedMechanisms.length > 0 && (
        <RelatedGroup
          title="Shared Principles"
          description="Organizations demonstrating similar principles"
          specimens={sharedMechanisms}
        />
      )}
    </div>
  );
}

function RelatedGroup({
  title,
  description,
  specimens,
}: {
  title: string;
  description: string;
  specimens: Specimen[];
}) {
  return (
    <div>
      <h4 className="font-serif text-base font-medium text-forest">{title}</h4>
      <p className="mt-0.5 text-xs text-charcoal-400">{description}</p>
      <div className="mt-3 grid gap-3 md:grid-cols-2">
        {specimens.slice(0, 6).map((s) => (
          <SpecimenCard key={s.id} specimen={s} compact />
        ))}
      </div>
    </div>
  );
}
