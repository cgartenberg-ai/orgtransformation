import fs from "fs/promises";
import path from "path";
import type { Specimen, StructuralModel, Orientation } from "@/lib/types/specimen";

const DATA_ROOT = path.resolve(process.cwd(), "..");
const SPECIMENS_DIR = path.join(DATA_ROOT, "specimens");

const EXCLUDED_FILES = new Set([
  "_template.json",
  "specimen-schema.json",
  "registry.json",
  "source-registry.json",
]);

/**
 * Load all specimen JSON files from ../specimens/.
 * Globs dynamically — no hardcoded list.
 */
export async function getAllSpecimens(): Promise<Specimen[]> {
  const files = await fs.readdir(SPECIMENS_DIR);
  const jsonFiles = files.filter(
    (f) => f.endsWith(".json") && !EXCLUDED_FILES.has(f)
  );

  const results = await Promise.all(
    jsonFiles.map(async (file) => {
      try {
        const raw = await fs.readFile(path.join(SPECIMENS_DIR, file), "utf-8");
        return JSON.parse(raw) as Specimen;
      } catch (e) {
        console.error(`[specimens] Failed to parse ${file}:`, e);
        return null;
      }
    })
  );

  const specimens = results.filter((s): s is Specimen => s !== null);
  return specimens.sort((a, b) =>
    (a.name || "").localeCompare(b.name || "")
  );
}

/**
 * Load a single specimen by its ID (filename without .json).
 */
export async function getSpecimenById(id: string): Promise<Specimen | null> {
  const filePath = path.join(SPECIMENS_DIR, `${id}.json`);
  try {
    const raw = await fs.readFile(filePath, "utf-8");
    return JSON.parse(raw) as Specimen;
  } catch {
    return null;
  }
}

/**
 * Get all specimen IDs for generateStaticParams.
 */
export async function getSpecimenIds(): Promise<string[]> {
  const specimens = await getAllSpecimens();
  return specimens.map((s) => s.id);
}

/**
 * Compute aggregate stats from actual specimen files.
 * No hardcoded counts — everything derived from the data.
 */
export async function getComputedStats() {
  const specimens = await getAllSpecimens();
  const active = specimens.filter((s) => s.meta?.status !== "Archived");

  return {
    totalSpecimens: active.length,
    byModel: countBy(active, (s) =>
      s.classification?.structuralModel != null
        ? String(s.classification.structuralModel)
        : "Unknown"
    ),
    byOrientation: countBy(
      active,
      (s) => s.classification?.orientation ?? "Unknown"
    ),
    typeSpecimens: active.filter((s) => s.classification?.typeSpecimen),
    byCompleteness: countBy(active, (s) => s.meta?.completeness ?? "Unknown"),
    byIndustry: countBy(active, (s) => s.habitat?.industry || "Unknown"),
    industries: Array.from(
      new Set(active.map((s) => s.habitat?.industry).filter(Boolean))
    ).sort(),
    lastUpdated: active.reduce(
      (latest, s) =>
        (s.meta?.lastUpdated || "") > latest ? s.meta.lastUpdated : latest,
      ""
    ),
  };
}

/**
 * Get specimens grouped by structural model and orientation.
 * Used by the taxonomy browser.
 */
export async function getSpecimensByTaxonomy(): Promise<
  Record<number, Record<string, Specimen[]>>
> {
  const specimens = await getAllSpecimens();
  const active = specimens.filter((s) => s.meta.status !== "Archived");

  const matrix: Record<number, Record<string, Specimen[]>> = {};
  for (const model of [1, 2, 3, 4, 5, 6, 7, 8, 9] as StructuralModel[]) {
    matrix[model] = {};
    for (const orientation of [
      "Structural",
      "Contextual",
      "Temporal",
    ] as Orientation[]) {
      matrix[model][orientation] = active.filter(
        (s) =>
          s.classification.structuralModel === model &&
          s.classification.orientation === orientation
      );
    }
  }

  return matrix;
}

function countBy<T>(
  items: T[],
  keyFn: (item: T) => string
): Record<string, number> {
  return items.reduce(
    (acc, item) => {
      const key = keyFn(item);
      acc[key] = (acc[key] || 0) + 1;
      return acc;
    },
    {} as Record<string, number>
  );
}
