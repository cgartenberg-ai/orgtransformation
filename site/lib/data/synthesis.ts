import fs from "fs/promises";
import path from "path";
import type {
  MechanismData,
  TensionData,
  ContingencyData,
} from "@/lib/types/synthesis";

const SYNTHESIS_DIR = path.resolve(process.cwd(), "..", "synthesis");

export async function getMechanisms(): Promise<MechanismData> {
  const raw = await fs.readFile(
    path.join(SYNTHESIS_DIR, "mechanisms.json"),
    "utf-8"
  );
  return JSON.parse(raw);
}

export async function getTensions(): Promise<TensionData> {
  const raw = await fs.readFile(
    path.join(SYNTHESIS_DIR, "tensions.json"),
    "utf-8"
  );
  return JSON.parse(raw);
}

export async function getContingencies(): Promise<ContingencyData> {
  const raw = await fs.readFile(
    path.join(SYNTHESIS_DIR, "contingencies.json"),
    "utf-8"
  );
  return JSON.parse(raw);
}
