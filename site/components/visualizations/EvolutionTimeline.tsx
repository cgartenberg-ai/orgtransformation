"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { Layer } from "@/lib/types/specimen";

export function EvolutionTimeline({ layers }: { layers: Layer[] }) {
  const [selectedIndex, setSelectedIndex] = useState(0);

  if (layers.length === 0) return null;

  // Parse dates for positioning
  const parsed = layers.map((layer, i) => {
    const [year, month] = layer.date.split("-").map(Number);
    return { ...layer, year, month: month || 1, index: i };
  });

  // SVG dimensions
  const padding = 40;
  const width = Math.max(400, parsed.length * 140 + padding * 2);
  const height = 100;
  const lineY = 50;

  // Distribute nodes evenly
  const nodeSpacing = (width - padding * 2) / Math.max(parsed.length - 1, 1);

  return (
    <div className="space-y-4">
      {/* Timeline SVG */}
      <div className="overflow-x-auto rounded-lg border border-sage-200 bg-cream-50 p-4">
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="w-full"
          style={{ minWidth: `${width}px`, maxHeight: "100px" }}
        >
          {/* Main line */}
          <line
            x1={padding}
            y1={lineY}
            x2={width - padding}
            y2={lineY}
            stroke="#84A98C"
            strokeWidth={2}
          />

          {/* Nodes */}
          {parsed.map((layer, i) => {
            const x = parsed.length === 1
              ? width / 2
              : padding + i * nodeSpacing;
            const isSelected = i === selectedIndex;
            const isCurrent = i === 0;

            return (
              <g
                key={i}
                onClick={() => setSelectedIndex(i)}
                className="cursor-pointer"
              >
                {/* Click target (larger invisible circle) */}
                <circle cx={x} cy={lineY} r={16} fill="transparent" />

                {/* Visible node */}
                <motion.circle
                  cx={x}
                  cy={lineY}
                  r={isSelected ? 10 : 7}
                  fill={isCurrent ? "#1B4332" : isSelected ? "#3F7D5A" : "#84A98C"}
                  stroke={isSelected ? "#1B4332" : "transparent"}
                  strokeWidth={2}
                  animate={{
                    r: isSelected ? 10 : 7,
                    fill: isCurrent
                      ? "#1B4332"
                      : isSelected
                        ? "#3F7D5A"
                        : "#84A98C",
                  }}
                  transition={{ duration: 0.2 }}
                />

                {/* Date label */}
                <text
                  x={x}
                  y={lineY - 18}
                  textAnchor="middle"
                  className="fill-charcoal-600 font-mono text-[11px]"
                >
                  {layer.date}
                </text>

                {/* Layer label (if short enough) */}
                {layer.label && (
                  <text
                    x={x}
                    y={lineY + 24}
                    textAnchor="middle"
                    className="fill-charcoal-400 text-[10px]"
                  >
                    {layer.label.length > 20
                      ? layer.label.slice(0, 18) + "..."
                      : layer.label}
                  </text>
                )}
              </g>
            );
          })}
        </svg>
      </div>

      {/* Selected layer detail */}
      <AnimatePresence mode="wait">
        <motion.div
          key={selectedIndex}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -8 }}
          transition={{ duration: 0.2 }}
          className="rounded-lg border border-sage-200 bg-cream-50 p-5"
        >
          <div className="flex items-start justify-between">
            <div>
              <span className="font-mono text-sm font-medium text-forest">
                {parsed[selectedIndex].date}
              </span>
              {selectedIndex === 0 && (
                <span className="ml-2 rounded bg-forest-50 px-1.5 py-0.5 text-[10px] font-medium text-forest">
                  Latest
                </span>
              )}
              {parsed[selectedIndex].label && (
                <span className="ml-2 text-sm font-medium text-charcoal-700">
                  {parsed[selectedIndex].label}
                </span>
              )}
            </div>
            <span className="text-xs text-charcoal-400">
              Observation {parsed.length - selectedIndex} of {parsed.length}
            </span>
          </div>
          <p className="mt-3 text-sm leading-relaxed text-charcoal-600">
            {parsed[selectedIndex].summary}
          </p>
          {parsed[selectedIndex].classification && (
            <p className="mt-2 font-mono text-xs text-charcoal-400">
              Classification:{" "}
              {typeof parsed[selectedIndex].classification === "object"
                ? formatClassification(parsed[selectedIndex].classification as Record<string, unknown>)
                : String(parsed[selectedIndex].classification)}
            </p>
          )}
          {parsed[selectedIndex].sourceRefs.length > 0 && (
            <p className="mt-1 text-xs text-charcoal-400">
              Sources: {parsed[selectedIndex].sourceRefs.join(", ")}
            </p>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}

function formatClassification(c: Record<string, unknown>): string {
  const parts: string[] = [];
  if (c.structuralModel) parts.push(`M${c.structuralModel}`);
  if (c.orientation) parts.push(String(c.orientation));
  if (c.action) parts.push(String(c.action));
  if (c.confidence) parts.push(`${c.confidence} confidence`);
  return parts.join(" · ");
}
