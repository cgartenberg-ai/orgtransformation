import fs from "fs/promises";
import path from "path";
import type {
  MechanismData,
  TensionData,
  ContingencyData,
  InsightData,
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

export async function getInsights(): Promise<InsightData> {
  try {
    const raw = await fs.readFile(
      path.join(SYNTHESIS_DIR, "insights.json"),
      "utf-8"
    );
    return JSON.parse(raw);
  } catch (e) {
    console.error(`[synthesis] Failed to load insights.json: ${e}`);
    return EMPTY_INSIGHTS;
  }
}
