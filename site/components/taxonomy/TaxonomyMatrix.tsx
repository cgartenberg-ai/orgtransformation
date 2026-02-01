"use client";

import Link from "next/link";
import type { Specimen, StructuralModel, Orientation } from "@/lib/types/specimen";
import {
  STRUCTURAL_MODELS,
  ORIENTATIONS,
  MODEL_NUMBERS,
} from "@/lib/types/taxonomy";

type Matrix = Record<number, Record<string, Specimen[]>>;

export function TaxonomyMatrix({ matrix }: { matrix: Matrix }) {
  return (
    <div className="mt-6 overflow-x-auto">
      <table className="w-full border-collapse">
        <thead>
          <tr>
            <th className="p-3 text-left text-xs font-medium uppercase tracking-wide text-charcoal-400" />
            {ORIENTATIONS.map((o) => (
              <th
                key={o}
                className="p-3 text-center text-xs font-medium uppercase tracking-wide text-charcoal-400"
              >
                {o}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {MODEL_NUMBERS.map((model) => (
            <tr key={model} className="border-t border-sage-200">
              <td className="p-3">
                <div className="font-mono text-xs font-medium text-forest">
                  {STRUCTURAL_MODELS[model].shortName}
                </div>
                <div className="text-sm font-medium text-charcoal-700">
                  {STRUCTURAL_MODELS[model].name}
                </div>
              </td>
              {ORIENTATIONS.map((orientation) => {
                const specimens = matrix[model]?.[orientation] ?? [];
                return (
                  <TaxonomyCell
                    key={`${model}-${orientation}`}
                    model={model}
                    orientation={orientation}
                    specimens={specimens}
                  />
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function TaxonomyCell({
  model,
  orientation,
  specimens,
}: {
  model: StructuralModel;
  orientation: Orientation;
  specimens: Specimen[];
}) {
  const count = specimens.length;

  if (count === 0) {
    return (
      <td className="p-3 text-center">
        <span className="text-xs text-charcoal-300">&mdash;</span>
      </td>
    );
  }

  // Dot density: 1-5 dots based on count
  const dots = Math.min(count, 5);
  const filled = Array.from({ length: dots }, () => true);
  const empty = Array.from({ length: 5 - dots }, () => false);

  return (
    <td className="p-3 text-center">
      <Link
        href={`/specimens?model=${model}&orientation=${orientation}`}
        className="group inline-block rounded-lg p-2 transition-colors hover:bg-sage-50"
        title={specimens.map((s) => s.name).join(", ")}
      >
        <div className="flex items-center justify-center gap-0.5">
          {filled.map((_, i) => (
            <span
              key={`f-${i}`}
              className="inline-block h-2 w-2 rounded-full bg-forest"
            />
          ))}
          {empty.map((_, i) => (
            <span
              key={`e-${i}`}
              className="inline-block h-2 w-2 rounded-full bg-sage-200"
            />
          ))}
        </div>
        <span className="mt-1 block font-mono text-xs text-charcoal-500 group-hover:text-forest">
          {count}
        </span>
      </Link>
    </td>
  );
}
