import type { Specimen } from "@/lib/types/specimen";
import type { ConfirmedMechanism } from "@/lib/types/synthesis";
import { MechanismChip } from "@/components/mechanisms/MechanismChip";

export function MechanismsTab({
  specimen,
  mechanismDefinitions,
}: {
  specimen: Specimen;
  mechanismDefinitions: ConfirmedMechanism[];
}) {
  if (specimen.mechanisms.length === 0) {
    return (
      <p className="text-sm text-charcoal-400">
        No mechanisms documented for this specimen yet.
      </p>
    );
  }

  return (
    <div className="space-y-4">
      <p className="text-sm text-charcoal-500">
        Cross-cutting patterns observed in {specimen.name}:
      </p>
      <div className="space-y-3">
        {specimen.mechanisms.map((m) => {
          const definition = mechanismDefinitions.find((d) => d.id === m.id);
          return (
            <div key={m.id} className="space-y-2">
              <MechanismChip mechanism={m} showEvidence />
              {definition && (
                <p className="ml-4 text-xs text-charcoal-400">
                  {definition.definition}
                </p>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
