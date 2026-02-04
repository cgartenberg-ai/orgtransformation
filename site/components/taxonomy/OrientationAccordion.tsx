"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import type { Orientation, Specimen, StructuralModel } from "@/lib/types/specimen";
import { ORIENTATION_DESCRIPTIONS, STRUCTURAL_MODELS } from "@/lib/types/taxonomy";
import type { ConfirmedMechanism } from "@/lib/types/synthesis";

interface OrientationAccordionProps {
  orientation: Orientation;
  specimens: Specimen[];
  mechanisms: ConfirmedMechanism[];
}

export function OrientationAccordion({
  orientation,
  specimens,
  mechanisms,
}: OrientationAccordionProps) {
  const [open, setOpen] = useState(false);

  const matching = specimens.filter(
    (s) =>
      s.meta.status !== "Archived" && s.classification.orientation === orientation
  );

  const modelDist: Record<number, number> = {};
  for (const s of matching) {
    const m = s.classification.structuralModel;
    if (m) modelDist[m] = (modelDist[m] || 0) + 1;
  }

  // Find mechanisms whose primary orientation matches
  const relatedMechanisms = mechanisms
    .filter((m) => m.affinityProfile?.primaryOrientation === orientation)
    .slice(0, 5);

  return (
    <div className="rounded-lg border border-sage-200 bg-white">
      <button
        onClick={() => setOpen(!open)}
        className="flex w-full items-center justify-between px-5 py-4 text-left transition-colors hover:bg-cream-50"
      >
        <span className="font-serif text-base font-medium text-forest">
          {orientation}
        </span>
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
              <p className="text-sm leading-relaxed text-charcoal-600">
                {ORIENTATION_DESCRIPTIONS[orientation]}
              </p>

              {/* Model distribution */}
              <div>
                <h4 className="mb-2 text-xs font-medium uppercase tracking-wide text-charcoal-400">
                  Most Common Models
                </h4>
                <div className="flex flex-wrap gap-2">
                  {Object.entries(modelDist)
                    .sort(([, a], [, b]) => b - a)
                    .slice(0, 5)
                    .map(([model, count]) => (
                      <Link
                        key={model}
                        href={`/taxonomy/models/${model}`}
                        className="rounded border border-sage-200 bg-cream-50 px-2 py-1 text-xs text-charcoal-600 hover:bg-sage-50"
                      >
                        <span className="font-mono text-forest">M{model}</span>{" "}
                        {STRUCTURAL_MODELS[Number(model) as StructuralModel]?.name} ({count})
                      </Link>
                    ))}
                </div>
              </div>

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
                        #{m.id} {m.name}
                      </Link>
                    ))}
                  </div>
                </div>
              )}

              <Link
                href={`/taxonomy/orientations/${orientation}`}
                className="inline-block text-xs font-medium text-forest hover:underline"
              >
                View all {orientation} specimens &rarr;
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
