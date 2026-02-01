"use client";

import { useEffect, useRef, useState } from "react";
import * as d3 from "d3";
import Link from "next/link";
import type { Specimen, TensionPositions } from "@/lib/types/specimen";
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
    const height = 400;
    const padding = 60;

    svg.selectAll("*").remove();
    svg.attr("viewBox", `0 0 ${width} ${height}`);

    // Scale: -1 to +1 maps to padding to width-padding
    const xScale = d3
      .scaleLinear()
      .domain([-1, 1])
      .range([padding, width - padding]);

    // Axis line
    svg
      .append("line")
      .attr("x1", padding)
      .attr("y1", height / 2)
      .attr("x2", width - padding)
      .attr("y2", height / 2)
      .attr("stroke", "#D8E5DB")
      .attr("stroke-width", 1);

    // Pole labels
    svg
      .append("text")
      .attr("x", padding)
      .attr("y", height / 2 + 40)
      .attr("text-anchor", "start")
      .attr("class", "fill-charcoal-400")
      .style("font-size", "11px")
      .text(tension.whenNegative.label);

    svg
      .append("text")
      .attr("x", width - padding)
      .attr("y", height / 2 + 40)
      .attr("text-anchor", "end")
      .attr("class", "fill-charcoal-400")
      .style("font-size", "11px")
      .text(tension.whenPositive.label);

    // Center line
    svg
      .append("line")
      .attr("x1", width / 2)
      .attr("y1", padding)
      .attr("x2", width / 2)
      .attr("y2", height - padding)
      .attr("stroke", "#D8E5DB")
      .attr("stroke-width", 1)
      .attr("stroke-dasharray", "4,4");

    // D3 force simulation
    const simulation = d3
      .forceSimulation<SpecimenNode>(nodes)
      .force(
        "x",
        d3.forceX<SpecimenNode>((d) => xScale(d.value)).strength(0.8)
      )
      .force("y", d3.forceY(height / 2).strength(0.15))
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
      .attr("r", 12)
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
      .attr("dy", 24)
      .attr("class", "fill-charcoal-600")
      .style("font-size", "9px")
      .text((d) => {
        const name = d.specimen.name;
        return name.length > 14 ? name.slice(0, 12) + "..." : name;
      });

    // Hover interactions via DOM events
    nodeGroups
      .on("mouseenter", (_event, d) => {
        setHoveredSpecimen(d.specimen);
      })
      .on("mouseleave", () => {
        setHoveredSpecimen(null);
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
        <svg ref={svgRef} className="w-full" style={{ minHeight: "400px" }} />
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
              M{model}: {STRUCTURAL_MODELS[Number(model) as 1 | 2 | 3 | 4 | 5 | 6 | 7]?.name}
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
            <div className="flex gap-2">
              <span className="rounded bg-forest-50 px-2 py-0.5 font-mono text-[10px] text-forest">
                M{hoveredSpecimen.classification.structuralModel}
              </span>
              <span className="rounded bg-sage-100 px-2 py-0.5 font-mono text-[10px] text-sage-700">
                {hoveredSpecimen.classification.orientation}
              </span>
            </div>
          </div>
          <p className="mt-2 line-clamp-2 text-sm text-charcoal-600">
            {hoveredSpecimen.description.slice(0, 200)}...
          </p>
        </div>
      )}
    </div>
  );
}
