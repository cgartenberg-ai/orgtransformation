import type { Specimen } from "@/lib/types/specimen";
import { SourceCitation } from "@/components/shared/SourceCitation";

export function SourcesTab({ specimen }: { specimen: Specimen }) {
  if (specimen.sources.length === 0) {
    return (
      <p className="text-sm text-charcoal-400">
        No sources documented yet.
      </p>
    );
  }

  // Group sources by type
  const grouped = specimen.sources.reduce(
    (acc, source) => {
      const type = source.type;
      if (!acc[type]) acc[type] = [];
      acc[type].push(source);
      return acc;
    },
    {} as Record<string, typeof specimen.sources>
  );

  return (
    <div className="space-y-6">
      <p className="text-sm text-charcoal-500">
        All facts in this specimen are traceable to primary sources.
      </p>
      {Object.entries(grouped)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([type, sources]) => (
          <div key={type}>
            <h4 className="mb-2 text-xs font-medium uppercase tracking-wide text-charcoal-400">
              {type} ({sources.length})
            </h4>
            <div className="space-y-2">
              {sources.map((source) => (
                <SourceCitation key={source.id} source={source} />
              ))}
            </div>
          </div>
        ))}
    </div>
  );
}
