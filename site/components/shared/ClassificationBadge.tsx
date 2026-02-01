import { STRUCTURAL_MODELS, SUB_TYPES } from "@/lib/types/taxonomy";
import type { Classification } from "@/lib/types/specimen";

export function ClassificationBadge({
  classification,
}: {
  classification: Classification;
}) {
  const model = classification.structuralModel;
  const modelInfo = model ? STRUCTURAL_MODELS[model] : null;
  const subTypeName = classification.subType
    ? SUB_TYPES[classification.subType] ?? classification.subTypeName
    : null;

  return (
    <div className="flex flex-wrap gap-2">
      {modelInfo && (
        <span className="rounded bg-forest-50 px-2.5 py-1 font-mono text-xs font-medium text-forest">
          {modelInfo.shortName}: {modelInfo.name}
        </span>
      )}
      {subTypeName && (
        <span className="rounded bg-forest-50 px-2.5 py-1 font-mono text-xs text-forest-600">
          {subTypeName}
        </span>
      )}
      {classification.secondaryModel && (
        <span className="rounded bg-forest-50 px-2.5 py-1 font-mono text-xs text-forest-600">
          +M{classification.secondaryModel}
          {classification.secondaryModelName
            ? `: ${classification.secondaryModelName}`
            : ""}
        </span>
      )}
      {classification.orientation && (
        <span className="rounded bg-sage-100 px-2.5 py-1 font-mono text-xs text-sage-700">
          {classification.orientation}
        </span>
      )}
      {classification.typeSpecimen && (
        <span className="rounded-full bg-amber-100 px-2.5 py-1 font-mono text-xs font-medium text-amber-700">
          Type Specimen
        </span>
      )}
    </div>
  );
}
