/**
 * Citation parser for inline [source-id] markers in specimen text.
 *
 * Text containing `[source-id]` markers gets split into segments:
 * - type "text": regular prose
 * - type "citation": a source ID reference
 *
 * Source IDs must match entries in the specimen's `sources` array.
 * Text without any citations parses to a single text segment.
 */

export interface ParsedSegment {
  type: "text" | "citation";
  content: string; // text content or source ID
}

// Matches [source-id-like-this] — lowercase letters, digits, hyphens
const CITATION_REGEX = /\[([a-z0-9][a-z0-9-]*[a-z0-9])\]/g;

/**
 * Parse text with [source-id] markers into alternating text/citation segments.
 */
export function parseCitations(text: string): ParsedSegment[] {
  const segments: ParsedSegment[] = [];
  let lastIndex = 0;

  // Reset regex state
  CITATION_REGEX.lastIndex = 0;

  let match: RegExpExecArray | null;
  while ((match = CITATION_REGEX.exec(text)) !== null) {
    // Add text before this match
    if (match.index > lastIndex) {
      segments.push({
        type: "text",
        content: text.slice(lastIndex, match.index),
      });
    }

    // Add citation
    segments.push({
      type: "citation",
      content: match[1], // captured source ID
    });

    lastIndex = match.index + match[0].length;
  }

  // Add remaining text
  if (lastIndex < text.length) {
    segments.push({
      type: "text",
      content: text.slice(lastIndex),
    });
  }

  // If no citations found, return single text segment
  if (segments.length === 0) {
    segments.push({ type: "text", content: text });
  }

  return segments;
}

/**
 * Check if text contains any citation markers.
 */
export function hasCitations(text: string): boolean {
  CITATION_REGEX.lastIndex = 0;
  return CITATION_REGEX.test(text);
}
