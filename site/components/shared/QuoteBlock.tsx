import type { Quote } from "@/lib/types/specimen";

export function QuoteBlock({ quote }: { quote: Quote }) {
  return (
    <blockquote className="rounded-lg border-l-4 border-amber bg-cream-50 p-4">
      <p className="font-serif text-base italic text-charcoal-700">
        &ldquo;{quote.text}&rdquo;
      </p>
      <footer className="mt-2 text-sm text-charcoal-500">
        <span className="font-medium text-charcoal-700">{quote.speaker}</span>
        {quote.speakerTitle && <span>, {quote.speakerTitle}</span>}
        {quote.source && (
          <>
            {" "}
            &mdash;{" "}
            {quote.sourceUrl ? (
              <a
                href={quote.sourceUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="underline hover:text-forest"
              >
                {quote.source}
              </a>
            ) : (
              <span>{quote.source}</span>
            )}
          </>
        )}
        {quote.date && <span className="ml-1 text-charcoal-400">({quote.date})</span>}
      </footer>
    </blockquote>
  );
}
