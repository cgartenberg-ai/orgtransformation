"use client";

import { useState, useMemo } from "react";
import type { ClaimType } from "@/lib/types/purpose-claims";
import {
  CLAIM_TYPE_LABELS,
  CLAIM_TYPE_COLORS,
  CLAIM_TYPES_ORDER,
} from "@/components/purpose-claims/claim-constants";

interface SpiderChartProps {
  /** Display-ready 0-1 values (rescaled) for each claim type axis. */
  values: Partial<Record<ClaimType, number>>;
  /** Raw proportions (0-1, not rescaled) for accurate tooltip percentages.
   *  If omitted, tooltips use display values directly. */
  rawProportions?: Partial<Record<ClaimType, number>>;
  /** Optional comparison overlay (e.g., model average). */
  comparison?: {
    label: string;
    values: Partial<Record<ClaimType, number>>;
    color?: string;
  } | null;
  /** Diameter in pixels. Default 200. */
  size?: number;
  /** Show axis labels. Default true. */
  showLabels?: boolean;
  /** Show concentric grid rings. Default true. */
  showGrid?: boolean;
  /** Enable hover tooltips. Default false. */
  interactive?: boolean;
  /** Accent fill color. Default forest. */
  fillColor?: string;
  /** Accent stroke color. Default forest. */
  strokeColor?: string;
}

const ABBREVIATED_LABELS: Record<ClaimType, string> = {
  utopian: "Uto",
  teleological: "Tel",
  "higher-calling": "HC",
  identity: "Id",
  survival: "Sur",
  "commercial-success": "Com",
};

const GRID_LEVELS = [0.33, 0.66, 1.0];
const AXIS_COUNT = 6;
const ANGLE_STEP = (2 * Math.PI) / AXIS_COUNT;
// Start from the top (12 o'clock position), going clockwise
const START_ANGLE = -Math.PI / 2;

function polarToCartesian(
  angle: number,
  radius: number,
  cx: number,
  cy: number
): [number, number] {
  return [cx + radius * Math.cos(angle), cy + radius * Math.sin(angle)];
}

function buildPolygonPath(
  values: Partial<Record<ClaimType, number>>,
  maxRadius: number,
  cx: number,
  cy: number
): string {
  const points = CLAIM_TYPES_ORDER.map((type, i) => {
    const angle = START_ANGLE + i * ANGLE_STEP;
    const val = values[type] || 0;
    const r = val * maxRadius;
    return polarToCartesian(angle, r, cx, cy);
  });
  return points.map(([x, y], i) => `${i === 0 ? "M" : "L"}${x},${y}`).join(" ") + "Z";
}

function buildGridPath(level: number, maxRadius: number, cx: number, cy: number): string {
  const r = level * maxRadius;
  const points = Array.from({ length: AXIS_COUNT }, (_, i) => {
    const angle = START_ANGLE + i * ANGLE_STEP;
    return polarToCartesian(angle, r, cx, cy);
  });
  return points.map(([x, y], i) => `${i === 0 ? "M" : "L"}${x},${y}`).join(" ") + "Z";
}

export function SpiderChart({
  values,
  rawProportions,
  comparison = null,
  size = 200,
  showLabels = true,
  showGrid = true,
  interactive = false,
  fillColor = "#1B4332",
  strokeColor = "#1B4332",
}: SpiderChartProps) {
  const [hoveredAxis, setHoveredAxis] = useState<ClaimType | null>(null);

  // Layout dimensions
  const labelMargin = showLabels ? (size < 160 ? 24 : 36) : 8;
  const totalSize = size + labelMargin * 2;
  const cx = totalSize / 2;
  const cy = totalSize / 2;
  const maxRadius = size / 2;

  const useAbbreviated = size < 160;
  const labelMap = useAbbreviated ? ABBREVIATED_LABELS : CLAIM_TYPE_LABELS;

  // Pre-compute axis endpoints and label positions
  const axes = useMemo(
    () =>
      CLAIM_TYPES_ORDER.map((type, i) => {
        const angle = START_ANGLE + i * ANGLE_STEP;
        const [endX, endY] = polarToCartesian(angle, maxRadius, cx, cy);
        const labelRadius = maxRadius + (useAbbreviated ? 14 : 20);
        const [labelX, labelY] = polarToCartesian(angle, labelRadius, cx, cy);
        return { type, angle, endX, endY, labelX, labelY };
      }),
    [maxRadius, cx, cy, useAbbreviated]
  );

  // Primary polygon path
  const primaryPath = buildPolygonPath(values, maxRadius, cx, cy);

  // Comparison polygon path
  const comparisonPath = comparison
    ? buildPolygonPath(comparison.values, maxRadius, cx, cy)
    : null;
  const comparisonColor = comparison?.color || "#8BA69B"; // sage

  return (
    <svg
      width={totalSize}
      height={totalSize}
      viewBox={`0 0 ${totalSize} ${totalSize}`}
      className="block"
    >
      {/* Grid rings */}
      {showGrid &&
        GRID_LEVELS.map((level) => (
          <path
            key={level}
            d={buildGridPath(level, maxRadius, cx, cy)}
            fill="none"
            stroke="#BFD4C4"
            strokeWidth={0.5}
            opacity={0.6}
          />
        ))}

      {/* Axis lines — subtle guides, not visual focus */}
      {axes.map(({ type, endX, endY }) => (
        <line
          key={type}
          x1={cx}
          y1={cy}
          x2={endX}
          y2={endY}
          stroke={CLAIM_TYPE_COLORS[type].hex}
          strokeWidth={0.75}
          opacity={0.25}
        />
      ))}

      {/* Comparison polygon (behind primary) */}
      {comparisonPath && (
        <path
          d={comparisonPath}
          fill={comparisonColor}
          fillOpacity={0.1}
          stroke={comparisonColor}
          strokeWidth={1.5}
          strokeDasharray="4 3"
          opacity={0.7}
        />
      )}

      {/* Primary polygon */}
      <path
        d={primaryPath}
        fill={fillColor}
        fillOpacity={0.2}
        stroke={strokeColor}
        strokeWidth={1.5}
        strokeLinejoin="round"
      />

      {/* Axis endpoint dots */}
      {axes.map(({ type, angle }) => {
        const val = values[type] || 0;
        const r = val * maxRadius;
        const [dx, dy] = polarToCartesian(angle, r, cx, cy);
        return (
          <circle
            key={`dot-${type}`}
            cx={dx}
            cy={dy}
            r={interactive && hoveredAxis === type ? 4 : 2.5}
            fill={CLAIM_TYPE_COLORS[type].hex}
            stroke="white"
            strokeWidth={1}
            className={interactive ? "cursor-pointer transition-all duration-150" : ""}
            onMouseEnter={interactive ? () => setHoveredAxis(type) : undefined}
            onMouseLeave={interactive ? () => setHoveredAxis(null) : undefined}
          />
        );
      })}

      {/* Axis labels */}
      {showLabels &&
        axes.map(({ type, labelX, labelY, angle }) => {
          // Determine text-anchor based on position
          const angleDeg = ((angle * 180) / Math.PI + 360) % 360;
          let textAnchor: "start" | "middle" | "end" = "middle";
          if (angleDeg > 10 && angleDeg < 170) textAnchor = "start";
          if (angleDeg > 190 && angleDeg < 350) textAnchor = "end";

          const isHovered = interactive && hoveredAxis === type;

          return (
            <text
              key={`label-${type}`}
              x={labelX}
              y={labelY}
              textAnchor={textAnchor}
              dominantBaseline="central"
              fontSize={useAbbreviated ? 9 : 10}
              fontWeight={isHovered ? 600 : 400}
              fill={isHovered ? CLAIM_TYPE_COLORS[type].hex : "#535657"}
              className={interactive ? "transition-all duration-150" : ""}
              onMouseEnter={interactive ? () => setHoveredAxis(type) : undefined}
              onMouseLeave={interactive ? () => setHoveredAxis(null) : undefined}
            >
              {labelMap[type]}
            </text>
          );
        })}

      {/* Hover tooltip */}
      {interactive && hoveredAxis && (() => {
        const idx = CLAIM_TYPES_ORDER.indexOf(hoveredAxis);
        const angle = START_ANGLE + idx * ANGLE_STEP;
        const displayVal = values[hoveredAxis] || 0;
        const r = displayVal * maxRadius;
        const [tipX, tipY] = polarToCartesian(angle, r, cx, cy);
        // Show real proportion in tooltip, not the rescaled display value
        const rawVal = rawProportions ? (rawProportions[hoveredAxis] || 0) : displayVal;
        const pct = Math.round(rawVal * 100);

        return (
          <g>
            <rect
              x={tipX - 20}
              y={tipY - 20}
              width={40}
              height={16}
              rx={3}
              fill="#3A3D3E"
              opacity={0.9}
            />
            <text
              x={tipX}
              y={tipY - 10}
              textAnchor="middle"
              fontSize={9}
              fill="white"
              fontWeight={500}
            >
              {pct}%
            </text>
          </g>
        );
      })()}

      {/* Comparison label */}
      {comparison && showLabels && (
        <text
          x={totalSize - 4}
          y={totalSize - 4}
          textAnchor="end"
          fontSize={8}
          fill={comparisonColor}
          opacity={0.7}
        >
          ---- {comparison.label}
        </text>
      )}
    </svg>
  );
}
