import fs from "fs/promises";
import path from "path";
import type {
  MechanismData,
  TensionData,
  ContingencyData,
  InsightData,
  FindingData,
  PrimitiveData,
} from "@/lib/types/synthesis";

const SYNTHESIS_DIR = path.resolve(process.cwd(), "..", "synthesis");

const EMPTY_MECHANISMS: MechanismData = {
  description: "",
  lastUpdated: "",
  confirmed: [],
  candidates: [],
};

const EMPTY_TENSIONS: TensionData = {
  description: "",
  lastUpdated: "",
  tensions: [],
};

const EMPTY_CONTINGENCIES: ContingencyData = {
  description: "",
  lastUpdated: "",
  contingencies: [],
};

const EMPTY_INSIGHTS: InsightData = {
  description: "",
  lastUpdated: "",
  insights: [],
};

const EMPTY_FINDINGS: FindingData = {
  description: "",
  lastUpdated: "",
  findings: [],
  fieldObservations: [],
};

const EMPTY_PRIMITIVES: PrimitiveData = {
  description: "",
  lastUpdated: "",
  primitives: [],
};

export async function getMechanisms(): Promise<MechanismData> {
  try {
    const raw = await fs.readFile(
      path.join(SYNTHESIS_DIR, "mechanisms.json"),
      "utf-8"
    );
    return JSON.parse(raw);
  } catch (e) {
    console.error(`[synthesis] Failed to load mechanisms.json: ${e}`);
    return EMPTY_MECHANISMS;
  }
}

export async function getTensions(): Promise<TensionData> {
  try {
    const raw = await fs.readFile(
      path.join(SYNTHESIS_DIR, "tensions.json"),
      "utf-8"
    );
    return JSON.parse(raw);
  } catch (e) {
    console.error(`[synthesis] Failed to load tensions.json: ${e}`);
    return EMPTY_TENSIONS;
  }
}

export async function getContingencies(): Promise<ContingencyData> {
  try {
    const raw = await fs.readFile(
      path.join(SYNTHESIS_DIR, "contingencies.json"),
      "utf-8"
    );
    return JSON.parse(raw);
  } catch (e) {
    console.error(`[synthesis] Failed to load contingencies.json: ${e}`);
    return EMPTY_CONTINGENCIES;
  }
}

/** @deprecated Use getFindings() instead — insights have been consolidated into 10 findings */
export async function getInsights(): Promise<InsightData> {
  try {
    const raw = await fs.readFile(
      path.join(SYNTHESIS_DIR, "insights-archive-v1.json"),
      "utf-8"
    );
    return JSON.parse(raw);
  } catch (e) {
    console.error(`[synthesis] Failed to load insights-archive-v1.json: ${e}`);
    return EMPTY_INSIGHTS;
  }
}

export async function getFindings(): Promise<FindingData> {
  try {
    const raw = await fs.readFile(
      path.join(SYNTHESIS_DIR, "findings.json"),
      "utf-8"
    );
    return JSON.parse(raw);
  } catch (e) {
    console.error(`[synthesis] Failed to load findings.json: ${e}`);
    return EMPTY_FINDINGS;
  }
}

export async function getPrimitives(): Promise<PrimitiveData> {
  try {
    const raw = await fs.readFile(
      path.join(SYNTHESIS_DIR, "primitives.json"),
      "utf-8"
    );
    return JSON.parse(raw);
  } catch (e) {
    console.error(`[synthesis] Failed to load primitives.json: ${e}`);
    return EMPTY_PRIMITIVES;
  }
}
