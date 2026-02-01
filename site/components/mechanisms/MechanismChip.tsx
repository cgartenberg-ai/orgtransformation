import Link from "next/link";
import type { SpecimenMechanism } from "@/lib/types/specimen";

export function MechanismChip({
  mechanism,
  showEvidence = false,
}: {
  mechanism: SpecimenMechanism;
  showEvidence?: boolean;
}) {
  const strengthColors: Record<string, string> = {
    Strong: "bg-forest-50 text-forest border-forest-200",
    Moderate: "bg-sage-50 text-sage-700 border-sage-200",
    Emerging: "bg-amber-50 text-amber-700 border-amber-200",
  };

  const colorClass = strengthColors[mechanism.strength] ?? strengthColors.Moderate;

  return (
    <div className={`rounded-lg border p-3 ${colorClass}`}>
      <div className="flex items-center justify-between">
        <Link
          href={`/mechanisms/${mechanism.id}`}
          className="text-sm font-medium hover:underline"
        >
          #{mechanism.id} {mechanism.name}
        </Link>
        <span className="ml-2 rounded-full px-2 py-0.5 text-[10px] font-medium uppercase">
          {mechanism.strength}
        </span>
      </div>
      {showEvidence && mechanism.evidence && (
        <p className="mt-2 text-xs leading-relaxed opacity-80">
          {mechanism.evidence}
        </p>
      )}
    </div>
  );
}
