import Link from "next/link";
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
        <Link
          href={`/taxonomy/models/${model}`}
          className="rounded bg-forest-50 px-2.5 py-1 font-mono text-xs font-medium text-forest transition-colors hover:bg-forest-100 hover:text-forest-700"
        >
          {modelInfo.shortName}: {modelInfo.name}
        </Link>
      )}
      {subTypeName && (
        <Link
          href={`/taxonomy/models/${model}`}
          className="rounded bg-forest-50 px-2.5 py-1 font-mono text-xs text-forest-600 transition-colors hover:bg-forest-100 hover:text-forest-700"
        >
          {subTypeName}
        </Link>
      )}
      {classification.secondaryModel && (
        <Link
          href={`/taxonomy/models/${classification.secondaryModel}`}
          className="rounded bg-forest-50 px-2.5 py-1 font-mono text-xs text-forest-600 transition-colors hover:bg-forest-100 hover:text-forest-700"
        >
          +M{classification.secondaryModel}
          {classification.secondaryModelName
            ? `: ${classification.secondaryModelName}`
            : ""}
        </Link>
      )}
      {classification.orientation && (
        <Link
          href={`/taxonomy/orientations/${classification.orientation}`}
          className="rounded bg-sage-100 px-2.5 py-1 font-mono text-xs text-sage-700 transition-colors hover:bg-sage-200 hover:text-sage-800"
        >
          {classification.orientation}
        </Link>
      )}
      {classification.typeSpecimen && (
        <span className="rounded-full bg-amber-100 px-2.5 py-1 font-mono text-xs font-medium text-amber-700">
          Type Specimen
        </span>
      )}
    </div>
  );
}
