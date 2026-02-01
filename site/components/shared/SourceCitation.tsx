import type { Source } from "@/lib/types/specimen";

export function SourceCitation({ source }: { source: Source }) {
  return (
    <div className="flex items-start gap-3 rounded border border-sage-200 bg-cream-50 px-4 py-3">
      <span className="mt-0.5 rounded bg-sage-100 px-1.5 py-0.5 font-mono text-[10px] uppercase text-sage-700">
        {source.type}
      </span>
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium text-charcoal-700">
          {source.url ? (
            <a
              href={source.url}
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-forest"
            >
              {source.name}
            </a>
          ) : (
            source.name
          )}
        </p>
        <div className="mt-0.5 flex gap-3 text-xs text-charcoal-400">
          {source.sourceDate && <span>Source: {source.sourceDate}</span>}
          {source.collectedDate && (
            <span>Collected: {source.collectedDate}</span>
          )}
        </div>
        {source.notes && (
          <p className="mt-1 text-xs text-charcoal-400">{source.notes}</p>
        )}
      </div>
    </div>
  );
}
