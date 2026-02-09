import type { ClaimType } from "@/lib/types/purpose-claims";

export const CLAIM_TYPE_LABELS: Record<ClaimType, string> = {
  utopian: "Utopian",
  teleological: "Teleological",
  "higher-calling": "Higher Calling",
  identity: "Identity",
  survival: "Survival",
  "commercial-success": "Commercial",
};

export const CLAIM_TYPE_COLORS: Record<ClaimType, { bg: string; text: string; border: string; hex: string }> = {
  utopian: { bg: "bg-violet-50", text: "text-violet-700", border: "border-violet-300", hex: "#8b5cf6" },
  teleological: { bg: "bg-amber-50", text: "text-amber-700", border: "border-amber-300", hex: "#D4A373" },
  "higher-calling": { bg: "bg-rose-50", text: "text-rose-600", border: "border-rose-300", hex: "#e11d48" },
  identity: { bg: "bg-forest-50", text: "text-forest", border: "border-forest-200", hex: "#1B4332" },
  survival: { bg: "bg-charcoal-50", text: "text-charcoal-600", border: "border-charcoal-200", hex: "#535657" },
  "commercial-success": { bg: "bg-sky-50", text: "text-sky-700", border: "border-sky-300", hex: "#0284c7" },
};

export const CLAIM_TYPES_ORDER: ClaimType[] = [
  "utopian",
  "teleological",
  "higher-calling",
  "identity",
  "survival",
  "commercial-success",
];

export interface SpecimenInfo {
  id: string;
  name: string;
  industry: string;
  structuralModel: number | null;
  structuralModelName: string | null;
}
