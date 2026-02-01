"use client";

import { useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import type { Specimen } from "@/lib/types/specimen";
import { rankSpecimens, type MatchInput, type MatchResult } from "@/lib/matching";

const DIMENSIONS = [
  {
    key: "regulatoryIntensity" as const,
    label: "Regulatory Intensity",
    description: "How heavily regulated is your industry?",
    options: [
      { value: "Low", label: "Low", hint: "Tech, retail, media" },
      { value: "Medium", label: "Medium", hint: "Manufacturing, professional services" },
      { value: "High", label: "High", hint: "Pharma, financial services, healthcare" },
    ],
  },
  {
    key: "timeToObsolescence" as const,
    label: "Time to Obsolescence",
    description: "How quickly could AI disrupt your core business?",
    options: [
      { value: "Fast", label: "Fast", hint: "Market moves in months" },
      { value: "Medium", label: "Medium", hint: "1-3 year cycles" },
      { value: "Slow", label: "Slow", hint: "Decades of stability" },
    ],
  },
  {
    key: "ceoTenure" as const,
    label: "CEO Tenure & Mandate",
    description: "How much runway does leadership have for structural change?",
    options: [
      { value: "Short", label: "Short", hint: "New or transitional leader" },
      { value: "Medium", label: "Medium", hint: "2-5 years, building track record" },
      { value: "Long", label: "Long", hint: "Established leader or founder" },
    ],
  },
  {
    key: "talentMarketPosition" as const,
    label: "Talent Market Position",
    description: "How easily can you attract top AI talent?",
    options: [
      { value: "Talent-rich", label: "Talent-rich", hint: "Top-tier brand, competitive comp" },
      { value: "Talent-constrained", label: "Constrained", hint: "Competing for limited pool" },
      { value: "Non-traditional", label: "Non-traditional", hint: "Building from adjacent skills" },
    ],
  },
  {
    key: "technicalDebt" as const,
    label: "Technical Debt",
    description: "How much legacy infrastructure constrains AI adoption?",
    options: [
      { value: "Low", label: "Low", hint: "Modern stack, cloud-native" },
      { value: "Medium", label: "Medium", hint: "Mix of modern and legacy" },
      { value: "High", label: "High", hint: "Significant legacy systems" },
    ],
  },
];

export function MatcherForm({
  specimens,
}: {
  specimens: Specimen[];
}) {
  const [input, setInput] = useState<MatchInput>({
    regulatoryIntensity: null,
    timeToObsolescence: null,
    ceoTenure: null,
    talentMarketPosition: null,
    technicalDebt: null,
  });

  const results = useMemo(() => rankSpecimens(input, specimens), [input, specimens]);
  const hasInput = Object.values(input).some(Boolean);

  const setDimension = (key: keyof MatchInput, value: string) => {
    setInput((prev) => ({
      ...prev,
      [key]: prev[key] === value ? null : value, // Toggle off if same
    }));
  };

  const resetAll = () => {
    setInput({
      regulatoryIntensity: null,
      timeToObsolescence: null,
      ceoTenure: null,
      talentMarketPosition: null,
      technicalDebt: null,
    });
  };

  return (
    <div className="mt-6 grid gap-8 lg:grid-cols-[340px_1fr]">
      {/* Input form */}
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <p className="text-sm text-charcoal-500">
            Tell us about your context. Select as many or as few dimensions as relevant.
          </p>
          {hasInput && (
            <button
              onClick={resetAll}
              className="text-xs text-charcoal-400 underline hover:text-forest"
            >
              Reset
            </button>
          )}
        </div>

        {DIMENSIONS.map((dim) => (
          <div key={dim.key}>
            <label className="mb-1 block text-sm font-medium text-charcoal-700">
              {dim.label}
            </label>
            <p className="mb-2 text-xs text-charcoal-400">{dim.description}</p>
            <div className="flex flex-wrap gap-2">
              {dim.options.map((opt) => (
                <button
                  key={opt.value}
                  onClick={() => setDimension(dim.key, opt.value)}
                  className={`rounded-lg border px-3 py-2 text-left transition-colors ${
                    input[dim.key] === opt.value
                      ? "border-forest bg-forest text-cream"
                      : "border-sage-200 bg-cream-50 text-charcoal-700 hover:border-sage-400"
                  }`}
                >
                  <span className="block text-xs font-medium">{opt.label}</span>
                  <span
                    className={`block text-[10px] ${
                      input[dim.key] === opt.value
                        ? "text-cream/70"
                        : "text-charcoal-400"
                    }`}
                  >
                    {opt.hint}
                  </span>
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Results */}
      <div>
        {!hasInput ? (
          <div className="flex h-48 items-center justify-center rounded-lg border border-dashed border-sage-300 bg-cream-50">
            <p className="text-sm text-charcoal-400">
              Select dimensions to find matching specimens
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            <p className="text-sm text-charcoal-500">
              <span className="font-semibold text-forest">{results.length}</span>{" "}
              matching specimen{results.length !== 1 ? "s" : ""} found
            </p>

            <AnimatePresence mode="popLayout">
              {results.map((result) => (
                <MatchResultCard key={result.specimen.id} result={result} />
              ))}
            </AnimatePresence>

            {results.length === 0 && (
              <p className="mt-4 text-sm text-charcoal-400">
                No specimens match your current selections. Try adjusting your
                inputs or selecting fewer dimensions.
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function MatchResultCard({ result }: { result: MatchResult }) {
  const [expanded, setExpanded] = useState(false);
  const s = result.specimen;

  const scoreColor =
    result.score >= 80
      ? "text-forest bg-forest-50"
      : result.score >= 50
        ? "text-amber-700 bg-amber-50"
        : "text-charcoal-500 bg-charcoal-50";

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -8 }}
      transition={{ duration: 0.2 }}
      className="rounded-lg border border-sage-200 bg-cream-50"
    >
      <div className="flex items-start justify-between p-4">
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <Link
              href={`/specimens/${s.id}`}
              className="font-serif text-base font-semibold text-forest hover:underline"
            >
              {s.name}
            </Link>
            <span className={`rounded-full px-2.5 py-0.5 font-mono text-xs font-medium ${scoreColor}`}>
              {result.score}%
            </span>
          </div>
          <div className="mt-1 flex flex-wrap gap-1.5">
            <span className="rounded bg-forest-50 px-1.5 py-0.5 font-mono text-[10px] text-forest">
              M{s.classification.structuralModel}
            </span>
            <span className="rounded bg-sage-100 px-1.5 py-0.5 font-mono text-[10px] text-sage-700">
              {s.classification.orientation}
            </span>
            <span className="rounded bg-charcoal-50 px-1.5 py-0.5 text-[10px] text-charcoal-500">
              {s.habitat.industry}
            </span>
          </div>
        </div>
        <button
          onClick={() => setExpanded(!expanded)}
          className="ml-3 text-xs text-charcoal-400 hover:text-forest"
        >
          {expanded ? "Hide" : "Why?"}
        </button>
      </div>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="border-t border-sage-100 px-4 pb-4 pt-3">
              <p className="mb-2 text-xs font-medium uppercase tracking-wide text-charcoal-400">
                Match Breakdown ({result.matchedDimensions}/{result.totalDimensions} dimensions)
              </p>
              <div className="space-y-1.5">
                {result.dimensions.map((d) => (
                  <div
                    key={d.label}
                    className="flex items-center justify-between text-xs"
                  >
                    <span className="text-charcoal-600">{d.label}</span>
                    <div className="flex items-center gap-2">
                      <span className="text-charcoal-400">
                        {d.explanation}
                      </span>
                      <span
                        className={`rounded px-1.5 py-0.5 font-mono text-[10px] ${
                          d.score === 1
                            ? "bg-forest-50 text-forest"
                            : d.score === 0.5
                              ? "bg-amber-50 text-amber-700"
                              : "bg-charcoal-50 text-charcoal-400"
                        }`}
                      >
                        {d.score === 1 ? "✓" : d.score === 0.5 ? "~" : "✗"}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
