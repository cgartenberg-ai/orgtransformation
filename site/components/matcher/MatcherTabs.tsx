"use client";

import { useState } from "react";

export function MatcherTabs({
  chatPanel,
  quickPanel,
}: {
  chatPanel: React.ReactNode;
  quickPanel: React.ReactNode;
}) {
  const [activeTab, setActiveTab] = useState<"chat" | "quick">("chat");

  return (
    <div>
      <div className="flex gap-1 rounded-lg bg-sage-100 p-1">
        <TabButton
          active={activeTab === "chat"}
          onClick={() => setActiveTab("chat")}
        >
          Chat Advisor
        </TabButton>
        <TabButton
          active={activeTab === "quick"}
          onClick={() => setActiveTab("quick")}
        >
          Quick Match
        </TabButton>
      </div>
      <div className="mt-6">
        {activeTab === "chat" ? chatPanel : quickPanel}
      </div>
    </div>
  );
}

function TabButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      className={`flex-1 rounded-md px-4 py-2 text-sm font-medium transition-colors ${
        active
          ? "bg-white text-forest shadow-sm"
          : "text-charcoal-500 hover:text-charcoal-700"
      }`}
    >
      {children}
    </button>
  );
}
