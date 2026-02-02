"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

interface PatternForDisplay {
  id: number;
  name: string;
  problemItSolves: string;
  specimensCount: number;
  quote?: string | null;
  speaker?: string | null;
}

export function FieldObservation({
  patterns,
}: {
  patterns: PatternForDisplay[];
}) {
  const [featured, setFeatured] = useState<PatternForDisplay | null>(null);

  useEffect(() => {
    if (patterns.length === 0) return;
    setFeatured(patterns[Math.floor(Math.random() * patterns.length)]);
  }, [patterns]);

  if (!featured) return null;

  const displayQuote = featured.quote ?? featured.problemItSolves;
  const attribution =
    featured.quote && featured.speaker ? featured.speaker : null;

  return (
    <div className="mx-auto max-w-3xl">
      <div className="relative overflow-hidden rounded-2xl border border-sage-200 bg-white p-10 shadow-sm">
        {/* Decorative corner accent */}
        <div className="absolute right-0 top-0 h-24 w-24 opacity-[0.06]">
          <div className="h-full w-full rounded-bl-full bg-forest" />
        </div>
        <div className="absolute bottom-0 left-0 h-16 w-16 opacity-[0.04]">
          <div className="h-full w-full rounded-tr-full bg-sage" />
        </div>

        <div className="relative text-center">
          <p className="font-mono text-[10px] uppercase tracking-[0.3em] text-sage-500">
            From the Field
          </p>
          <blockquote className="mx-auto mt-5 max-w-2xl">
            <p className="font-serif text-xl italic leading-relaxed text-charcoal-700">
              &ldquo;{displayQuote}&rdquo;
            </p>
          </blockquote>
          {attribution && (
            <p className="mt-3 text-sm text-charcoal-400">
              &mdash; {attribution}
            </p>
          )}
          <div className="mx-auto mt-6 h-px w-12 bg-amber" />
          <p className="mt-4 font-serif text-base font-semibold text-forest">
            {featured.name}
          </p>
          <p className="mt-1 text-sm text-charcoal-500">
            Observed across {featured.specimensCount} organizations
          </p>
          <Link
            href={`/mechanisms/${featured.id}`}
            className="mt-4 inline-block rounded-full border border-forest bg-forest-50/50 px-5 py-2 text-xs font-semibold text-forest transition-colors hover:bg-forest hover:text-cream"
          >
            Explore this principle &rarr;
          </Link>
        </div>
      </div>
    </div>
  );
}
