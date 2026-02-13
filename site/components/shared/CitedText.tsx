import type { Source } from "@/lib/types/specimen";
import { parseCitations } from "@/lib/utils/citations";

/**
 * Renders text with inline [source-id] citations as superscript links.
 *
 * Text without citations renders as plain text. Each [source-id] marker
 * becomes a numbered superscript that links to the source URL and shows
 * source metadata on hover.
 *
 * Backward compatible: existing text without markers renders normally.
 */
export function CitedText({
  text,
  sources,
}: {
  text: string;
  sources: Source[];
}) {
  const segments = parseCitations(text);

  // If only one text segment and no citations, render as plain text
  if (segments.length === 1 && segments[0].type === "text") {
    return <>{text}</>;
  }

  // Build source index for quick lookup
  const sourceIndex = new Map<string, { source: Source; index: number }>();
  const citationOrder: string[] = [];

  // Assign citation numbers in order of first appearance
  for (const seg of segments) {
    if (seg.type === "citation" && !sourceIndex.has(seg.content)) {
      const source = sources.find((s) => s.id === seg.content);
      if (source) {
        citationOrder.push(seg.content);
        sourceIndex.set(seg.content, {
          source,
          index: citationOrder.length,
        });
      }
    }
  }

  return (
    <>
      {segments.map((seg, i) => {
        if (seg.type === "text") {
          return <span key={i}>{seg.content}</span>;
        }

        const ref = sourceIndex.get(seg.content);
        if (!ref) {
          // Unknown source ID — render as bracketed text
          return (
            <span key={i} className="text-charcoal-300" title="Unknown source reference">
              [{seg.content}]
            </span>
          );
        }

        const { source, index } = ref;
        const title = [
          source.name,
          source.type && `(${source.type})`,
          source.sourceDate && `• ${source.sourceDate}`,
        ]
          .filter(Boolean)
          .join(" ");

        return (
          <sup key={i} className="ml-px">
            {source.url ? (
              <a
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-[9px] font-medium text-forest hover:underline"
                title={title}
              >
                {index}
              </a>
            ) : (
              <span
                className="text-[9px] font-medium text-charcoal-400 cursor-help"
                title={title}
              >
                {index}
              </span>
            )}
          </sup>
        );
      })}
    </>
  );
}
