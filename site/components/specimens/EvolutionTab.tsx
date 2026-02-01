import type { Specimen } from "@/lib/types/specimen";
import { EvolutionTimeline } from "@/components/visualizations/EvolutionTimeline";

export function EvolutionTab({ specimen }: { specimen: Specimen }) {
  if (specimen.layers.length === 0) {
    return (
      <p className="text-sm text-charcoal-400">
        No historical layers documented yet.
      </p>
    );
  }

  return (
    <div className="space-y-1">
      <p className="mb-4 text-sm text-charcoal-500">
        Stratigraphic layers &mdash; click a node to see details. Layers are
        never overwritten, only added.
      </p>
      <EvolutionTimeline layers={specimen.layers} />
    </div>
  );
}
