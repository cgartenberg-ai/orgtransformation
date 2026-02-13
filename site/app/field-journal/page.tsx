import { getFieldJournalEntries } from "@/lib/data/field-journal";
import { FieldJournalList } from "@/components/field-journal/FieldJournalList";

export const metadata = {
  title: "Field Journal | Field Guide to AI Organizations",
  description:
    "Research session logs — the running record of every field observation, curation session, and purpose-claims scan.",
};

export default async function FieldJournalPage() {
  const entries = await getFieldJournalEntries();

  // Pass entries without full content to the client (preview is computed here)
  const listEntries = entries.map((e) => ({
    ...e,
    content: "", // don't send full markdown to client for list view
  }));

  return (
    <main className="mx-auto max-w-4xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="font-serif text-3xl font-semibold text-forest">
          Field Journal
        </h1>
        <p className="mt-2 text-base text-charcoal-500">
          The running log of every research session, curation run, and
          purpose-claims scan. {entries.length} entries across three tracks.
        </p>
      </div>

      <FieldJournalList entries={listEntries} />
    </main>
  );
}
