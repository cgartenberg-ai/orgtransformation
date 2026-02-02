import { getAllSpecimens } from "@/lib/data/specimens";
import { MatcherForm } from "@/components/matcher/MatcherForm";
import { ChatMatcher } from "@/components/matcher/ChatMatcher";
import { MatcherTabs } from "@/components/matcher/MatcherTabs";

export const metadata = {
  title: "Find Your Match — Field Guide to AI Organizations",
  description:
    "Chat with an AI advisor or use quick matching to find organizations facing constraints like yours",
};

export default async function MatcherPage() {
  const specimens = await getAllSpecimens();
  const active = specimens.filter((s) => s.meta.status !== "Archived");

  return (
    <div className="space-y-6">
      <header>
        <h1 className="font-serif text-3xl font-semibold text-forest">
          Find Your Match
        </h1>
        <p className="mt-2 text-charcoal-500">
          Describe your organization and we&rsquo;ll help you find the
          structural species that fits your situation.
        </p>
      </header>

      <MatcherTabs
        chatPanel={<ChatMatcher />}
        quickPanel={<MatcherForm specimens={active} />}
      />
    </div>
  );
}
