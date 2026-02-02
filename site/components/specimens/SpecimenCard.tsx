"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import type { Specimen } from "@/lib/types/specimen";

export function SpecimenCard({
  specimen,
  compact = false,
}: {
  specimen: Specimen;
  compact?: boolean;
}) {
  const s = specimen;

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -8 }}
      whileHover={{
        y: -3,
        boxShadow: "0 8px 24px rgba(27,67,50,0.10)",
        transition: { duration: 0.2, ease: "easeOut" },
      }}
      whileTap={{ scale: 0.99 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className={`rounded-lg border bg-cream-50 ${
        s.classification.typeSpecimen
          ? "border-amber-200"
          : "border-sage-200"
      }`}
    >
      <div className={compact ? "p-3" : "p-5"}>
        {/* Name, title, description — link to specimen detail */}
        <Link href={`/specimens/${s.id}`} className="group block">
          <div className="flex items-start justify-between gap-2">
            <h3
              className={`font-serif font-semibold text-forest group-hover:text-forest-600 ${
                compact ? "text-sm" : "text-lg"
              }`}
            >
              {s.name}
            </h3>
            {s.classification.typeSpecimen && (
              <span className="shrink-0 rounded-full bg-amber-100 px-2 py-0.5 font-mono text-[10px] text-amber-700">
                Type
              </span>
            )}
          </div>

          {!compact && (
            <p className="mt-0.5 text-sm text-charcoal-500">{s.title}</p>
          )}
        </Link>

        {/* Tags — each links to its taxonomy detail page */}
        <div className="mt-2 flex flex-wrap gap-1.5">
          {s.classification.structuralModel && (
            <Link
              href={`/taxonomy/models/${s.classification.structuralModel}`}
              className="rounded bg-forest-50 px-1.5 py-0.5 font-mono text-[10px] text-forest transition-colors hover:bg-forest-100 hover:text-forest-700"
            >
              M{s.classification.structuralModel}
            </Link>
          )}
          {s.classification.secondaryModel && (
            <Link
              href={`/taxonomy/models/${s.classification.secondaryModel}`}
              className="rounded bg-forest-50 px-1.5 py-0.5 font-mono text-[10px] text-forest transition-colors hover:bg-forest-100 hover:text-forest-700"
            >
              +M{s.classification.secondaryModel}
            </Link>
          )}
          {s.classification.orientation && (
            <Link
              href={`/taxonomy/orientations/${s.classification.orientation}`}
              className="rounded bg-sage-100 px-1.5 py-0.5 font-mono text-[10px] text-sage-700 transition-colors hover:bg-sage-200 hover:text-sage-800"
            >
              {s.classification.orientation}
            </Link>
          )}
          {s.habitat.orgType === "AI-native" && (
            <span className="rounded bg-violet-100 px-1.5 py-0.5 font-mono text-[10px] text-violet-700">
              AI-native
            </span>
          )}
          <span className="rounded bg-charcoal-50 px-1.5 py-0.5 text-[10px] text-charcoal-500">
            {s.habitat.industry}
          </span>
          {!compact && (
            <span
              className={`rounded px-1.5 py-0.5 text-[10px] ${
                s.meta.completeness === "High"
                  ? "bg-forest-50 text-forest"
                  : s.meta.completeness === "Medium"
                    ? "bg-amber-50 text-amber-700"
                    : "bg-charcoal-50 text-charcoal-400"
              }`}
            >
              {s.meta.completeness}
            </span>
          )}
        </div>

        {/* Description — link to specimen detail */}
        {!compact && (
          <Link href={`/specimens/${s.id}`} className="group block">
            <p className="mt-2 line-clamp-2 text-sm text-charcoal-600">
              {s.description.slice(0, 150)}...
            </p>
          </Link>
        )}
      </div>
    </motion.div>
  );
}
