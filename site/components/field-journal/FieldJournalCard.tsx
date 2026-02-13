import Link from "next/link";
import type { FieldJournalEntry, FieldJournalTrack } from "@/lib/data/field-journal";

const trackConfig: Record<
  FieldJournalTrack,
  { label: string; bg: string; text: string }
> = {
  research: {
    label: "Research",
    bg: "bg-forest-50",
    text: "text-forest",
  },
  curation: {
    label: "Curation",
    bg: "bg-blue-50",
    text: "text-blue-700",
  },
  "purpose-claims": {
    label: "Purpose Claims",
    bg: "bg-amber-50",
    text: "text-amber-700",
  },
  synthesis: {
    label: "Synthesis",
    bg: "bg-purple-50",
    text: "text-purple-700",
  },
};

function formatDate(dateStr: string): string {
  if (!dateStr) return "";
  const [year, month, day] = dateStr.split("-");
  const months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
  ];
  return `${months[parseInt(month, 10) - 1]} ${parseInt(day, 10)}, ${year}`;
}

export function TrackBadge({ track }: { track: FieldJournalTrack }) {
  const config = trackConfig[track];
  return (
    <span
      className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-medium ${config.bg} ${config.text}`}
    >
      {config.label}
    </span>
  );
}

export function FieldJournalCard({ entry }: { entry: FieldJournalEntry }) {
  return (
    <Link
      href={`/field-journal/${encodeURIComponent(entry.id)}`}
      className="block rounded-lg border border-sage-200 bg-cream-50 p-5 transition-colors hover:border-forest/30 hover:bg-cream-100"
    >
      <div className="mb-2 flex items-center gap-3">
        <time className="text-xs text-charcoal-400">{formatDate(entry.date)}</time>
        <TrackBadge track={entry.track} />
        {entry.hasInsights && (
          <span className="rounded-full bg-forest-50 px-2 py-0.5 text-xs text-forest">
            insights
          </span>
        )}
      </div>
      <h3 className="mb-2 font-serif text-base font-medium text-charcoal-800">
        {entry.title}
      </h3>
      {entry.preview && (
        <p className="text-sm leading-relaxed text-charcoal-500">{entry.preview}</p>
      )}
    </Link>
  );
}
