// app/src/utils/abbreviateInsight.ts

/**
 * Extracts a 3-5 word key phrase from a longer insight.
 * Strategy: Find the most meaningful short phrase, prioritizing:
 * 1. Quoted text (often the key message)
 * 2. Text after colons (often the punchline)
 * 3. First significant clause
 */
export function abbreviateInsight(fullInsight: string, maxWords: number = 5): string {
  if (!fullInsight) return '';

  // Strategy 1: Look for quoted text (CEO quotes, key phrases)
  const quotedMatch = fullInsight.match(/'([^']+)'/);
  if (quotedMatch && quotedMatch[1]) {
    const quoted = quotedMatch[1];
    const words = quoted.split(/\s+/);
    if (words.length <= maxWords + 2) {
      // Return the quoted portion, possibly truncated
      return words.slice(0, maxWords).join(' ') + (words.length > maxWords ? '...' : '');
    }
  }

  // Strategy 2: Look for text after a colon (often the key insight)
  const colonIndex = fullInsight.indexOf(':');
  if (colonIndex !== -1 && colonIndex < fullInsight.length - 10) {
    const afterColon = fullInsight.slice(colonIndex + 1).trim();
    // Take first phrase/clause
    const firstClause = afterColon.split(/[.;,]/)[0].trim();
    const words = firstClause.split(/\s+/);
    if (words.length >= 3) {
      return words.slice(0, maxWords).join(' ') + (words.length > maxWords ? '...' : '');
    }
  }

  // Strategy 3: Extract key verb phrase or first meaningful chunk
  // Remove common filler starts
  const processed = fullInsight
    .replace(/^(The insight is that|The core insight is|CEO [^:]+:|[A-Z][a-z]+ [A-Z][a-z]+:)\s*/i, '')
    .trim();

  // Take first clause
  const firstClause = processed.split(/[.;]/)[0].trim();
  const words = firstClause.split(/\s+/);

  // If very short, use as-is
  if (words.length <= maxWords) {
    return firstClause;
  }

  // Otherwise truncate and add ellipsis
  return words.slice(0, maxWords).join(' ') + '...';
}
