import fs from "fs/promises";
import path from "path";

const DATA_ROOT = path.resolve(process.cwd(), "..");

/**
 * Directories containing session logs, mapped to their track name.
 */
const SESSION_DIRS: { dir: string; track: FieldJournalTrack }[] = [
  { dir: path.join(DATA_ROOT, "research", "sessions"), track: "research" },
  { dir: path.join(DATA_ROOT, "curation", "sessions"), track: "curation" },
  {
    dir: path.join(DATA_ROOT, "research", "purpose-claims", "sessions"),
    track: "purpose-claims",
  },
  { dir: path.join(DATA_ROOT, "synthesis", "sessions"), track: "synthesis" },
];

export type FieldJournalTrack = "research" | "curation" | "purpose-claims" | "synthesis";

export interface FieldJournalEntry {
  /** Unique ID: track prefix + filename stem, e.g. "research--2026-02-08-overnight-research" */
  id: string;
  /** Date extracted from filename (YYYY-MM-DD) */
  date: string;
  /** Human-readable title derived from first # heading or filename */
  title: string;
  /** Which pipeline track produced this log */
  track: FieldJournalTrack;
  /** Raw markdown content */
  content: string;
  /** Original filename */
  filename: string;
  /** Whether this entry contains analytical insights (vs. pure process log) */
  hasInsights: boolean;
  /** Short preview text for list view (stripped of markdown) */
  preview: string;
}

/**
 * Detect whether a session log contains substantive analytical content.
 * Looks for section headings and content patterns that indicate insight.
 */
function detectInsights(content: string): boolean {
  // Headings that signal analytical content
  const insightHeadings = [
    /^##?\s+.*Botanist/mi,
    /^##?\s+.*Taxonomy Feedback/mi,
    /^##?\s+.*Notable Claims/mi,
    /^##?\s+.*Cross-Cutting/mi,
    /^##?\s+.*Rhetorical/mi,
    /^##?\s+.*Per-Specimen Analysis/mi,
    /^##?\s+.*Field Notes/mi,
    /^##?\s+.*Convergent Evolution/mi,
    /^##?\s+.*New Insights Discovered/mi,
  ];

  // Content patterns that signal analytical prose (not just table data)
  const insightPatterns = [
    /Observation/i,
    /structurally interesting/i,
    /challenges? the taxonomy/i,
    /edge case/i,
    /pattern/i,
    /Open Questions/i,
  ];

  const headingHits = insightHeadings.filter((r) => r.test(content)).length;
  const patternHits = insightPatterns.filter((r) => r.test(content)).length;

  // At least one insight heading, or 3+ content patterns
  return headingHits >= 1 || patternHits >= 3;
}

/**
 * Parse a session-log filename into date and description.
 * Expected pattern: YYYY-MM-DD-description.md
 */
function parseFilename(filename: string): { date: string; description: string } {
  const stem = filename.replace(/\.md$/, "");
  const match = stem.match(/^(\d{4}-\d{2}-\d{2})-(.+)$/);
  if (match) {
    return { date: match[1], description: match[2] };
  }
  return { date: "", description: stem };
}

/**
 * Extract the first # heading from markdown content as the title.
 * Falls back to the filename description if no heading found.
 */
function extractTitle(content: string, fallback: string): string {
  const match = content.match(/^#\s+(.+)$/m);
  if (match) {
    return match[1].trim();
  }
  // Humanize the filename description
  return fallback
    .replace(/-/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

/**
 * Strip markdown formatting for preview text.
 */
function stripMarkdown(text: string): string {
  return text
    .replace(/^#+\s+.+$/gm, "") // headings
    .replace(/\*\*(.+?)\*\*/g, "$1") // bold
    .replace(/\*(.+?)\*/g, "$1") // italic
    .replace(/\[(.+?)\]\(.+?\)/g, "$1") // links
    .replace(/^\|.+\|$/gm, "") // table rows
    .replace(/^[-|:\s]+$/gm, "") // table separators
    .replace(/^[-*]\s+/gm, "") // list items
    .replace(/\n{2,}/g, "\n")
    .trim();
}

/**
 * Get a short preview (first ~200 chars) of the entry content,
 * skipping the title heading and metadata lines.
 */
export function getPreview(content: string, maxLength = 200): string {
  const stripped = stripMarkdown(content);
  if (stripped.length <= maxLength) return stripped;
  return stripped.slice(0, maxLength).replace(/\s+\S*$/, "") + "...";
}

/**
 * Load all field journal entries from all three session directories.
 * Returns entries sorted by date descending (most recent first).
 */
export async function getFieldJournalEntries(): Promise<FieldJournalEntry[]> {
  const entries: FieldJournalEntry[] = [];

  for (const { dir, track } of SESSION_DIRS) {
    let files: string[];
    try {
      files = await fs.readdir(dir);
    } catch {
      // Directory may not exist yet
      continue;
    }

    const mdFiles = files.filter((f) => f.endsWith(".md"));

    for (const filename of mdFiles) {
      const { date, description } = parseFilename(filename);
      const content = await fs.readFile(path.join(dir, filename), "utf-8");
      const title = extractTitle(content, description);
      const id = `${track}--${filename.replace(/\.md$/, "")}`;

      const hasInsights = detectInsights(content);
      const preview = getPreview(content);
      entries.push({ id, date, title, track, content, filename, hasInsights, preview });
    }
  }

  // Sort by date descending, then by track for same-day entries
  entries.sort((a, b) => {
    if (b.date !== a.date) return b.date.localeCompare(a.date);
    return a.track.localeCompare(b.track);
  });

  return entries;
}

/**
 * Load a single field journal entry by its compound ID.
 * ID format: "{track}--{filename-without-extension}"
 */
export async function getFieldJournalEntry(
  id: string
): Promise<FieldJournalEntry | null> {
  const sepIdx = id.indexOf("--");
  if (sepIdx === -1) return null;

  const track = id.slice(0, sepIdx) as FieldJournalTrack;
  const stem = id.slice(sepIdx + 2);
  const filename = `${stem}.md`;

  const dirEntry = SESSION_DIRS.find((d) => d.track === track);
  if (!dirEntry) return null;

  const filePath = path.join(dirEntry.dir, filename);
  try {
    const content = await fs.readFile(filePath, "utf-8");
    const { date, description } = parseFilename(filename);
    const title = extractTitle(content, description);
    const hasInsights = detectInsights(content);
    const preview = getPreview(content);
    return { id, date, title, track, content, filename, hasInsights, preview };
  } catch {
    return null;
  }
}

/**
 * Get all entry IDs for generateStaticParams.
 */
export async function getFieldJournalIds(): Promise<string[]> {
  const entries = await getFieldJournalEntries();
  return entries.map((e) => e.id);
}
