"use client";

import { useEffect, useRef, useState } from "react";
import * as d3 from "d3";
import Link from "next/link";
import type { Specimen, StructuralModel, TensionPositions } from "@/lib/types/specimen";
import type { Tension } from "@/lib/types/synthesis";
import { STRUCTURAL_MODELS } from "@/lib/types/taxonomy";

const MODEL_COLORS: Record<number, string> = {
  1: "#1B4332", // forest
  2: "#3F7D5A", // forest-500
  3: "#84A98C", // sage
  4: "#5C9173", // forest-400
  5: "#D4A373", // amber
  6: "#C48B55", // amber-500
  7: "#A87241", // amber-600
  8: "#8B6914", // dark gold — Skunkworks
  9: "#6A0DAD", // purple — AI-Native
};

interface SpecimenNode extends d3.SimulationNodeDatum {
  specimen: Specimen;
  value: number;
}

export function TensionMap({
  specimens,
  tensions,
}: {
  specimens: Specimen[];
  tensions: Tension[];
}) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [selectedTension, setSelectedTension] = useState(0);
  const [hoveredSpecimen, setHoveredSpecimen] = useState<Specimen | null>(null);
  const [hoveredValue, setHoveredValue] = useState<number | null>(null);

  const tension = tensions[selectedTension];
  const fieldName = tension?.fieldName as keyof TensionPositions | undefined;

  // Filter specimens that have a position for this tension
  const nodes: SpecimenNode[] = specimens
    .filter((s) => {
      if (!fieldName) return false;
      const val = s.tensionPositions[fieldName];
      return val !== null && val !== undefined;
    })
    .map((s) => ({
      specimen: s,
      value: s.tensionPositions[fieldName!] as number,
    }));

  useEffect(() => {
    if (!svgRef.current || !tension || nodes.length === 0) return;

    const svg = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth || 700;
    const height = 420;
    const paddingLeft = 120;
    const paddingRight = 120;
    const paddingTop = 40;
    const paddingBottom = 60;

    svg.selectAll("*").remove();
    svg.attr("viewBox", `0 0 ${width} ${height}`);

    const centerY = paddingTop + (height - paddingTop - paddingBottom) / 2;

    // Scale: -1 to +1 maps to paddingLeft to width-paddingRight
    const xScale = d3
      .scaleLinear()
      .domain([-1, 1])
      .range([paddingLeft, width - paddingRight]);

    // Background gradient zones
    svg
      .append("rect")
      .attr("x", paddingLeft)
      .attr("y", paddingTop)
      .attr("width", (width - paddingLeft - paddingRight) / 2)
      .attr("height", height - paddingTop - paddingBottom)
      .attr("fill", "#F8F0E8")
      .attr("opacity", 0.4)
      .attr("rx", 8);

    svg
      .append("rect")
      .attr("x", width / 2)
      .attr("y", paddingTop)
      .attr("width", (width - paddingLeft - paddingRight) / 2)
      .attr("height", height - paddingTop - paddingBottom)
      .attr("fill", "#E8F0E8")
      .attr("opacity", 0.4)
      .attr("rx", 8);

    // Axis line
    svg
      .append("line")
      .attr("x1", paddingLeft)
      .attr("y1", centerY)
      .attr("x2", width - paddingRight)
      .attr("y2", centerY)
      .attr("stroke", "#D8E5DB")
      .attr("stroke-width", 1);

    // Center line
    svg
      .append("line")
      .attr("x1", width / 2)
      .attr("y1", paddingTop)
      .attr("x2", width / 2)
      .attr("y2", height - paddingBottom)
      .attr("stroke", "#D8E5DB")
      .attr("stroke-width", 1)
      .attr("stroke-dasharray", "4,4");

    // Pole labels — positioned on the LEFT and RIGHT sides, vertically centered, multi-line
    const negLabel = tension.whenNegative.label;
    const posLabel = tension.whenPositive.label;

    // Left pole label (rotated vertically or just placed left)
    svg
      .append("text")
      .attr("x", paddingLeft - 12)
      .attr("y", centerY)
      .attr("text-anchor", "end")
      .attr("dominant-baseline", "middle")
      .attr("class", "fill-charcoal-500")
      .style("font-size", "12px")
      .style("font-weight", "600")
      .text(`← ${negLabel}`);

    // Right pole label
    svg
      .append("text")
      .attr("x", width - paddingRight + 12)
      .attr("y", centerY)
      .attr("text-anchor", "start")
      .attr("dominant-baseline", "middle")
      .attr("class", "fill-charcoal-500")
      .style("font-size", "12px")
      .style("font-weight", "600")
      .text(`${posLabel} →`);

    // Scale markers
    [-1, -0.5, 0, 0.5, 1].forEach((v) => {
      svg
        .append("text")
        .attr("x", xScale(v))
        .attr("y", height - paddingBottom + 20)
        .attr("text-anchor", "middle")
        .attr("class", "fill-charcoal-300")
        .style("font-size", "9px")
        .style("font-family", "monospace")
        .text(v > 0 ? `+${v}` : `${v}`);
    });

    // D3 force simulation
    const simulation = d3
      .forceSimulation<SpecimenNode>(nodes)
      .force(
        "x",
        d3.forceX<SpecimenNode>((d) => xScale(d.value)).strength(0.8)
      )
      .force("y", d3.forceY(centerY).strength(0.15))
      .force("collide", d3.forceCollide(18))
      .alphaDecay(0.03)
      .stop();

    // Run simulation synchronously
    for (let i = 0; i < 200; i++) simulation.tick();

    // Draw nodes
    const nodeGroups = svg
      .selectAll<SVGGElement, SpecimenNode>("g.node")
      .data(nodes)
      .join("g")
      .attr("class", "node cursor-pointer")
      .attr("transform", (d) => `translate(${d.x},${d.y})`);

    nodeGroups
      .append("circle")
      .attr("r", 13)
      .attr("fill", (d) =>
        MODEL_COLORS[d.specimen.classification.structuralModel ?? 4] ?? "#84A98C"
      )
      .attr("opacity", 0.85)
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5);

    // Model number label inside circle
    nodeGroups
      .append("text")
      .attr("text-anchor", "middle")
      .attr("dy", "0.35em")
      .attr("fill", "#fff")
      .style("font-size", "9px")
      .style("font-family", "monospace")
      .style("font-weight", "600")
      .text((d) => `M${d.specimen.classification.structuralModel ?? "?"}`);

    // Name label below
    nodeGroups
      .append("text")
      .attr("text-anchor", "middle")
      .attr("dy", 26)
      .attr("class", "fill-charcoal-600")
      .style("font-size", "9px")
      .text((d) => {
        const name = d.specimen.name;
        return name.length > 16 ? name.slice(0, 14) + "..." : name;
      });

    // Hover interactions via DOM events
    nodeGroups
      .on("mouseenter", (_event, d) => {
        setHoveredSpecimen(d.specimen);
        setHoveredValue(d.value);
      })
      .on("mouseleave", () => {
        setHoveredSpecimen(null);
        setHoveredValue(null);
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedTension, nodes.length]);

  if (tensions.length === 0) {
    return <p className="text-sm text-charcoal-400">No tension data available.</p>;
  }

  return (
    <div className="space-y-4">
      {/* Tension selector */}
      <div className="flex items-center gap-3">
        <label className="text-xs font-medium uppercase tracking-wide text-charcoal-400">
          Tension
        </label>
        <select
          value={selectedTension}
          onChange={(e) => setSelectedTension(Number(e.target.value))}
          className="rounded border border-sage-200 bg-cream-50 px-3 py-1.5 text-sm text-charcoal-700 focus:border-forest focus:outline-none"
        >
          {tensions.map((t, i) => (
            <option key={t.id} value={i}>
              {t.name}
            </option>
          ))}
        </select>
        <span className="text-xs text-charcoal-400">
          {nodes.length} specimens positioned
        </span>
      </div>

      {/* Description */}
      {tension && (
        <p className="text-sm text-charcoal-500">{tension.tradeoff}</p>
      )}

      {/* SVG Map */}
      <div className="overflow-x-auto rounded-lg border border-sage-200 bg-cream-50 p-4">
        <svg ref={svgRef} className="w-full" style={{ minHeight: "420px" }} />
      </div>

      {/* Legend */}
      <div className="flex flex-wrap gap-3">
        {Object.entries(MODEL_COLORS).map(([model, color]) => (
          <div key={model} className="flex items-center gap-1.5">
            <span
              className="inline-block h-3 w-3 rounded-full"
              style={{ backgroundColor: color }}
            />
            <span className="text-[10px] text-charcoal-500">
              M{model}: {STRUCTURAL_MODELS[Number(model) as StructuralModel]?.name}
            </span>
          </div>
        ))}
      </div>

      {/* Hover preview */}
      {hoveredSpecimen && (
        <div className="rounded-lg border border-sage-200 bg-cream-50 p-4">
          <div className="flex items-start justify-between">
            <div>
              <Link
                href={`/specimens/${hoveredSpecimen.id}`}
                className="font-serif text-base font-medium text-forest hover:underline"
              >
                {hoveredSpecimen.name}
              </Link>
              <p className="text-sm text-charcoal-500">
                {hoveredSpecimen.title}
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="rounded bg-forest-50 px-2 py-0.5 font-mono text-[10px] text-forest">
                M{hoveredSpecimen.classification.structuralModel}
                {" "}
                {STRUCTURAL_MODELS[hoveredSpecimen.classification.structuralModel as StructuralModel]?.name}
              </span>
              <span className="rounded bg-sage-100 px-2 py-0.5 font-mono text-[10px] text-sage-700">
                {hoveredSpecimen.classification.orientation}
              </span>
            </div>
          </div>
          {/* Position on this tension */}
          {typeof hoveredValue === "number" && tension && (
            <div className="mt-2 flex items-center gap-3">
              <span className="text-xs font-medium text-charcoal-400">
                Position:
              </span>
              <span className="font-mono text-sm font-medium text-forest">
                {hoveredValue > 0 ? "+" : ""}{hoveredValue.toFixed(1)}
              </span>
              <span className="text-xs text-charcoal-400">
                {hoveredValue < -0.2
                  ? `→ ${tension.whenNegative.label}`
                  : hoveredValue > 0.2
                  ? `→ ${tension.whenPositive.label}`
                  : "→ Balanced"}
              </span>
            </div>
          )}
          <p className="mt-2 line-clamp-2 text-sm text-charcoal-600">
            {hoveredSpecimen.description.slice(0, 200)}...
          </p>
        </div>
      )}
    </div>
  );
}
