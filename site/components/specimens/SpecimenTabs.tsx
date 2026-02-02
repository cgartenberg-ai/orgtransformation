"use client";

import { useState } from "react";
import type { Specimen } from "@/lib/types/specimen";
import type { ConfirmedMechanism } from "@/lib/types/synthesis";
import { OverviewTab } from "./OverviewTab";
import { MechanismsTab } from "./MechanismsTab";
import { EvolutionTab } from "./EvolutionTab";
import { SourcesTab } from "./SourcesTab";
import { RelatedTab } from "./RelatedTab";

const TABS = [
  { id: "overview", label: "Overview" },
  { id: "mechanisms", label: "Principles" },
  { id: "evolution", label: "Evolution" },
  { id: "sources", label: "Sources" },
  { id: "related", label: "Related" },
] as const;

type TabId = (typeof TABS)[number]["id"];

export function SpecimenTabs({
  specimen,
  related,
  mechanismDefinitions,
}: {
  specimen: Specimen;
  related: Specimen[];
  mechanismDefinitions: ConfirmedMechanism[];
}) {
  const [activeTab, setActiveTab] = useState<TabId>("overview");

  return (
    <div>
      <div className="border-b border-sage-200">
        <nav className="-mb-px flex gap-6" aria-label="Specimen tabs">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`border-b-2 pb-3 pt-2 text-sm font-medium transition-colors ${
                activeTab === tab.id
                  ? "border-forest text-forest"
                  : "border-transparent text-charcoal-400 hover:border-sage-300 hover:text-charcoal-600"
              }`}
            >
              {tab.label}
              {tab.id === "mechanisms" && specimen.mechanisms.length > 0 && (
                <span className="ml-1.5 rounded-full bg-forest-50 px-1.5 py-0.5 text-[10px] text-forest">
                  {specimen.mechanisms.length}
                </span>
              )}
              {tab.id === "evolution" && specimen.layers.length > 0 && (
                <span className="ml-1.5 rounded-full bg-forest-50 px-1.5 py-0.5 text-[10px] text-forest">
                  {specimen.layers.length}
                </span>
              )}
              {tab.id === "sources" && specimen.sources.length > 0 && (
                <span className="ml-1.5 rounded-full bg-forest-50 px-1.5 py-0.5 text-[10px] text-forest">
                  {specimen.sources.length}
                </span>
              )}
            </button>
          ))}
        </nav>
      </div>

      <div className="mt-6">
        {activeTab === "overview" && <OverviewTab specimen={specimen} />}
        {activeTab === "mechanisms" && (
          <MechanismsTab
            specimen={specimen}
            mechanismDefinitions={mechanismDefinitions}
          />
        )}
        {activeTab === "evolution" && <EvolutionTab specimen={specimen} />}
        {activeTab === "sources" && <SourcesTab specimen={specimen} />}
        {activeTab === "related" && (
          <RelatedTab specimen={specimen} related={related} />
        )}
      </div>
    </div>
  );
}
