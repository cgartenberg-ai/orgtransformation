import { notFound } from "next/navigation";
import Link from "next/link";
import {
  getFieldJournalEntry,
  getFieldJournalIds,
} from "@/lib/data/field-journal";
import { TrackBadge } from "@/components/field-journal/FieldJournalCard";
import { MarkdownRenderer } from "@/components/field-journal/MarkdownRenderer";

export async function generateStaticParams() {
  const ids = await getFieldJournalIds();
  return ids.map((id) => ({ id }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const entry = await getFieldJournalEntry(decodeURIComponent(id));
  if (!entry) return { title: "Not Found" };
  return {
    title: `${entry.title} | Field Journal`,
  };
}

function formatDate(dateStr: string): string {
  if (!dateStr) return "";
  const [year, month, day] = dateStr.split("-");
  const months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
  ];
  return `${months[parseInt(month, 10) - 1]} ${parseInt(day, 10)}, ${year}`;
}

export default async function FieldJournalEntryPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const entry = await getFieldJournalEntry(decodeURIComponent(id));
  if (!entry) notFound();

  return (
    <main className="mx-auto max-w-4xl px-4 py-10 sm:px-6 lg:px-8">
      <Link
        href="/field-journal"
        className="mb-6 inline-flex items-center gap-1 text-sm text-charcoal-400 transition-colors hover:text-forest"
      >
        &larr; Field Journal
      </Link>

      <div className="mb-6 flex items-center gap-3">
        <time className="text-sm text-charcoal-400">
          {formatDate(entry.date)}
        </time>
        <TrackBadge track={entry.track} />
      </div>

      <article className="prose prose-sm max-w-none prose-headings:font-serif prose-headings:text-forest prose-h1:text-2xl prose-h2:text-xl prose-h3:text-lg prose-p:text-charcoal-700 prose-li:text-charcoal-700 prose-strong:text-charcoal-800 prose-td:text-sm prose-th:text-sm prose-table:text-charcoal-700 prose-th:text-charcoal-500 prose-th:font-medium">
        <MarkdownRenderer content={entry.content} />
      </article>
    </main>
  );
}
