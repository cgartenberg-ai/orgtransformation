import type { Specimen } from "@/lib/types/specimen";
import { EvolutionTimeline } from "@/components/visualizations/EvolutionTimeline";

export function EvolutionTab({ specimen }: { specimen: Specimen }) {
  if (specimen.layers.length === 0) {
    return (
      <p className="text-sm text-charcoal-400">
        No organizational evolution documented yet.
      </p>
    );
  }

  return (
    <div className="space-y-1">
      <p className="mb-4 text-sm text-charcoal-500">
        How this organization&rsquo;s structural form has evolved. Each node
        marks an observed shift in AI organization or strategic direction.
      </p>
      <EvolutionTimeline layers={specimen.layers} />
    </div>
  );
}
