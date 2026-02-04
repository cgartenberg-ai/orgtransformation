"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import type { StructuralModel, Specimen } from "@/lib/types/specimen";
import { STRUCTURAL_MODELS, SUB_TYPES } from "@/lib/types/taxonomy";
import type { ConfirmedMechanism } from "@/lib/types/synthesis";

interface ModelAccordionProps {
  modelNum: StructuralModel;
  specimens: Specimen[];
  mechanisms: ConfirmedMechanism[];
}

const MODEL_SUBTYPES: Record<number, string[]> = {
  5: ["5a", "5b", "5c"],
  6: ["6a", "6b", "6c"],
};

export function ModelAccordion({ modelNum, specimens, mechanisms }: ModelAccordionProps) {
  const [open, setOpen] = useState(false);
  const model = STRUCTURAL_MODELS[modelNum];

  const matching = specimens.filter(
    (s) => s.meta.status !== "Archived" && s.classification.structuralModel === modelNum
  );

  const typeSpecimen = matching.find((s) => s.classification.typeSpecimen);

  const orientDist: Record<string, number> = {};
  for (const s of matching) {
    const o = s.classification.orientation;
    if (o) orientDist[o] = (orientDist[o] || 0) + 1;
  }

  // Find mechanisms with affinity to this model
  const relatedMechanisms = mechanisms
    .filter((m) => m.affinityProfile?.modelDistribution[modelNum])
    .sort(
      (a, b) =>
        (b.affinityProfile?.modelDistribution[modelNum]?.count ?? 0) -
        (a.affinityProfile?.modelDistribution[modelNum]?.count ?? 0)
    )
    .slice(0, 4);

  const subtypeKeys = MODEL_SUBTYPES[modelNum] || [];
  const isEmpty = matching.length === 0;

  return (
    <div className="rounded-lg border border-sage-200 bg-white">
      <button
        onClick={() => setOpen(!open)}
        className="flex w-full items-center justify-between px-5 py-4 text-left transition-colors hover:bg-cream-50"
      >
        <div className="flex items-center gap-3">
          <span className="rounded bg-forest-50 px-2 py-0.5 font-mono text-xs font-medium text-forest">
            {model.shortName}
          </span>
          <span className="font-serif text-base font-medium text-forest">
            {model.name}
          </span>
          {isEmpty && (
            <span className="rounded bg-charcoal-50 px-1.5 py-0.5 text-[10px] italic text-charcoal-400">
              {modelNum === 8 ? "Predicted" : "No specimens"}
            </span>
          )}
        </div>
        <div className="flex items-center gap-3">
          <span className="font-mono text-xs text-charcoal-400">
            {matching.length} specimen{matching.length !== 1 ? "s" : ""}
          </span>
          <span className="text-charcoal-400">{open ? "−" : "+"}</span>
        </div>
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="border-t border-sage-100 px-5 pb-5 pt-4 space-y-4">
              {/* Description */}
              <p className="text-sm text-charcoal-500">{model.description}</p>

              {/* Characteristics */}
              <p className="text-sm leading-relaxed text-charcoal-600">
                {model.characteristics}
              </p>

              {/* Stats row */}
              <div className="flex flex-wrap gap-4 text-xs text-charcoal-500">
                {typeSpecimen && (
                  <span>
                    Type specimen:{" "}
                    <Link
                      href={`/specimens/${typeSpecimen.id}`}
                      className="font-medium text-forest hover:underline"
                    >
                      {typeSpecimen.name}
                    </Link>
                  </span>
                )}
                {Object.entries(orientDist).map(([orient, count]) => (
                  <span key={orient}>
                    {count} {orient}
                  </span>
                ))}
              </div>

              {/* Sub-types */}
              {subtypeKeys.length > 0 && (
                <div>
                  <h4 className="mb-2 text-xs font-medium uppercase tracking-wide text-charcoal-400">
                    Sub-types
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {subtypeKeys.map((key) => {
                      const count = matching.filter(
                        (s) => s.classification.subType === key
                      ).length;
                      return (
                        <span
                          key={key}
                          className="rounded border border-sage-200 bg-cream-50 px-2 py-1 text-xs text-charcoal-600"
                        >
                          <span className="font-mono text-forest">{key.toUpperCase()}</span>{" "}
                          {SUB_TYPES[key]} ({count})
                        </span>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Related mechanisms */}
              {relatedMechanisms.length > 0 && (
                <div>
                  <h4 className="mb-2 text-xs font-medium uppercase tracking-wide text-charcoal-400">
                    Common Principles
                  </h4>
                  <div className="flex flex-wrap gap-1.5">
                    {relatedMechanisms.map((m) => (
                      <Link
                        key={m.id}
                        href={`/mechanisms/${m.id}`}
                        className="rounded bg-forest-50 px-2 py-1 text-xs text-forest hover:bg-forest-100"
                      >
                        #{m.id} {m.name} ({m.affinityProfile?.modelDistribution[modelNum]?.count})
                      </Link>
                    ))}
                  </div>
                </div>
              )}

              {/* Link to detail */}
              <Link
                href={`/taxonomy/models/${modelNum}`}
                className="inline-block text-xs font-medium text-forest hover:underline"
              >
                View all M{modelNum} specimens &rarr;
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
