import { getPurposeClaims } from "@/lib/data/purpose-claims";
import { getAllSpecimens } from "@/lib/data/specimens";
import { PurposeClaimsBrowser } from "@/components/purpose-claims/PurposeClaimsBrowser";

export const metadata = {
  title: "Purpose Claims — Field Guide to AI Organizations",
  description: "How leaders use purpose to authorize AI transformation",
};

export default async function PurposeClaimsPage({
  searchParams,
}: {
  searchParams: { specimen?: string };
}) {
  const [claimsData, allSpecimens] = await Promise.all([
    getPurposeClaims(),
    getAllSpecimens(),
  ]);

  const specimens = allSpecimens.map((s) => ({
    id: s.id,
    name: s.name,
    industry: s.habitat.industry,
    structuralModel: s.classification.structuralModel,
    structuralModelName: s.classification.structuralModelName ?? null,
  }));

  const scannedCount = new Set(claimsData.claims.map((c) => c.specimenId)).size;

  return (
    <div className="space-y-6">
      <header>
        <h1 className="font-serif text-3xl font-semibold text-forest">
          Purpose Claims
        </h1>
        <p className="mt-2 text-sm leading-relaxed text-charcoal-500">
          How leaders use purpose to authorize organizational transformation in the AI era.
          Verbatim claims collected from earnings calls, internal memos, podcasts, and press.
        </p>
        <p className="mt-1 text-xs text-charcoal-400">
          {claimsData.claims.length} claims from {scannedCount} specimens
          &middot; {allSpecimens.length - scannedCount} specimens not yet scanned
          &middot; Updated {claimsData.lastUpdated}
        </p>
      </header>

      <PurposeClaimsBrowser
        claims={claimsData.claims}
        claimTypeDefinitions={claimsData.claimTypeDefinitions}
        specimens={specimens}
        initialSpecimen={searchParams.specimen || null}
      />
    </div>
  );
}
