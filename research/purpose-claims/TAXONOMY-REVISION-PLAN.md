# Purpose Claims Taxonomy Revision Plan

## Created: February 8, 2026 (Session 6)
## Status: READY FOR EXECUTION in next session

---

## 1. Background: What Happened

In Session 6, we reviewed all 294 purpose claims together and identified fundamental problems with the v1.0 taxonomy (7 types). The taxonomy mixed categories that operate at different levels of abstraction — three types (utopian, teleological, identity) capture genuine **planes of meaning** while the other four (transformation-framing, employee-deal, sacrifice-justification, direction-under-uncertainty) are descriptive grab bags that classify by surface content rather than underlying meaning.

### The Core Reframe

The new organizing principle is: **what END does this claim point toward to justify AI transformation?**

Every purpose claim implicitly answers: "Why are we doing this?" The taxonomy should classify the *type of end* the leader invokes — not the rhetorical move being made, not the topic of the claim, but the ultimate justification being offered.

---

## 2. The New Taxonomy (v2.0) — 6 Types

| Type | The claim says... | Core question | Example |
|------|-------------------|---------------|---------|
| **utopian** | We are part of a civilizational transformation | "What epoch are we in?" | Hassabis: "radical abundance"; Benioff: "we are the last generation of CEOs to manage only humans" |
| **teleological** | We exist to achieve a specific moral/social outcome | "What concrete outcome justifies our existence?" | Hassabis: "cure all disease"; Bourla: "save the world from cancer"; SSI: "building safe superintelligence" |
| **higher-calling** | We answer to a duty/purpose that supersedes profit | "What obligation overrides economic logic?" | Amodei: "we work on science and biomedical out of proportion to its immediate profitability"; Ricks: "we have a higher calling" |
| **identity** | We do this because of who we are — group commitment | "Who are we?" | Teller: "we spend most of our time breaking things"; Nadella: "growth mindset"; Amodei: "having at least one player with a strong compass" |
| **survival** | We must change or be left behind | "What threat demands action?" | Regev: "if we proceed in this stepwise way we won't move fast enough"; Sweet: "this is reversing five decades"; Hudson: "you don't delegate the revolution" |
| **commercial-success** | This will make the business perform better | "How does this improve business outcomes?" | Nadella: "increase the ROIC on the capital spend"; Wells Fargo: "deliver an even better experience for customers" |

### Key Distinctions

**Utopian vs. Teleological vs. Higher-calling:**
- Utopian = the moment in history is the justification (epochal, civilizational)
- Teleological = a specific achievable outcome is the justification (cure cancer, build safe superintelligence)
- Higher-calling = a moral obligation that supersedes profit is the justification (we owe it to patients, we choose science over profitability)

**Survival vs. Commercial-success:**
- Survival = existential framing, adapt-or-die, the status quo is not viable
- Commercial-success = positive framing, this will make us better/more efficient/more competitive

**Identity vs. everything else:**
- Identity = the end IS the group's self-concept. "We do this because this is who we are." The justification terminates in collective identity itself.

### What's New vs. Old

| Old (v1.0) | New (v2.0) | What happened |
|------------|------------|---------------|
| utopian | **utopian** | Kept — works well |
| teleological | **teleological** | Kept — narrowed to specific moral/social outcomes |
| identity | **identity** | Kept — absorbs some employee-deal claims about organizational character |
| — | **higher-calling** | NEW — split from sacrifice-justification and teleological. Claims where moral duty supersedes profit. |
| — | **survival** | NEW — extracted from transformation-framing and direction-under-uncertainty. Adapt-or-die framing. |
| — | **commercial-success** | NEW — extracted from transformation-framing and direction-under-uncertainty. Standard business improvement logic. |
| transformation-framing | DISSOLVED | Claims redistributed to other types based on underlying end |
| employee-deal | DROPPED | Most claims don't meet purpose-claim inclusion criteria (they're managerial directives, not purpose invocations). A few are reclassified as identity. |
| sacrifice-justification | DISSOLVED | Was a surface feature (acknowledges cost), not a plane of meaning. Claims reclassified by their actual underlying end (teleological, higher-calling, identity, etc.) |
| direction-under-uncertainty | DISSOLVED | Was a grab bag. Claims reclassified by underlying end. |

---

## 3. Execution Plan

### Step 1: Update PURPOSE-CLAIMS-SPEC.md

Update Section 3 (Claim Type Taxonomy) with the v2.0 taxonomy above. Add entry to Section 10 (Taxonomy Changelog):

```
| 2026-02-08 | v2.0 | Revised from 7 types to 6. Dropped employee-deal (not purpose claims). Dissolved transformation-framing, sacrifice-justification, direction-under-uncertainty (surface features, not planes of meaning). Added higher-calling, survival, commercial-success. Reframe: types now classify the END the claim invokes, not the rhetorical move. | Session 6 analytical review of all 294 claims revealed 3 types operated at different abstraction level than other 4. |
```

### Step 2: Triage employee-deal claims (37 claims)

Read each of the 37 employee-deal claims. For each one, decide:

**A. Reclassify as identity** — if the claim is fundamentally about organizational character expressed through employee expectations. Examples:
- Regev: "Everyone should feel very comfortable talking with an accent" → identity (defines who Genentech is)
- Teller: "We have bonused every single person on teams that ended their projects" → identity (defines who X is)

**B. Reclassify as another v2.0 type** — if the claim has a clear underlying end that fits another category.

**C. Drop from registry** — if the claim is a managerial directive that doesn't actually invoke purpose/identity/values/mission. Mark as `"status": "dropped-v2"` rather than deleting (per never-delete rule). Examples of likely drops:
- Lütke: "Before asking for more headcount, teams must demonstrate why the work cannot be done with AI" → policy directive, not purpose claim
- Benioff: "I've reduced it from 9,000 heads to about 5,000" → staffing fact
- Bancel: "AI training is required for all Moderna team members" → HR mandate

**Expected outcome:** ~5-8 reclassified as identity or other types, ~25-30 marked as dropped.

### Step 3: Reclassify transformation-framing claims (59 claims)

Read each. Assign to the v2.0 type based on what END the claim serves. Expected distribution:
- Some → **survival** (adapt-or-die framing)
- Some → **commercial-success** (business improvement)
- Some → **identity** (who we are becoming)
- Some → **utopian** (epochal scale claims)
- Some → **dropped** (empirical statements that don't invoke purpose, e.g., "100% of our knowledge workers are active daily users of ChatGPT")

### Step 4: Reclassify sacrifice-justification claims (24 claims)

Read each. The "sacrifice" surface feature is not the type — classify by the END invoked to justify the sacrifice:
- Ricks "we have a higher calling" → **higher-calling**
- Teller "this team has done more by ending their project" → **identity**
- Scharf "the worst thing you can do is rehire someone" → **commercial-success** (or drop — may not be a purpose claim)
- Hudson "the jobs that go are the people that refuse to use AI" → **survival**

### Step 5: Reclassify direction-under-uncertainty claims (58 claims)

Read each. Classify by underlying end:
- Claims about navigating uncertainty through conviction → check if end is identity, higher-calling, survival, or commercial
- Claims that are just business management ("increase ROIC") → **commercial-success** or drop
- Claims about epistemic humility ("95% of AI projects fail") → evaluate whether these are purpose claims at all

### Step 6: Review utopian, teleological, identity claims (116 claims)

Quick pass — most should stay, but check for:
- Identity claims that are actually competitive positioning ("no business is better positioned than Salesforce") → possibly **commercial-success**
- Identity claims that are capability signaling ("most talent-dense research effort") → possibly **commercial-success**
- Teleological claims that are actually higher-calling (moral obligation, not specific outcome)

### Step 7: Review commercial-success claims

After reclassification, review the commercial-success pile. These ARE legitimate purpose claims — commercial success is a genuine end that leaders invoke to justify AI transformation. The point of keeping this category is that it provides the baseline: some leaders justify massive architectural upheaval with nothing more than commercial logic, while others reach for moral obligation or civilizational destiny. Without commercial-success, we lose the ability to measure that variation.

Only drop a claim from commercial-success if it's not actually articulating an end at all — e.g., it's just reporting a fact ("we have 340 live AI use cases") rather than invoking a purpose ("we're doing this to deliver better customer experience").

### Step 8: Update registry.json

Use a Python script (not manual JSON editing — files too large). The script should:
1. Read registry.json
2. For each claim, update `claimType` to new v2.0 type
3. For dropped claims, set `"status": "dropped-v2"` and add `"dropReason": "..."` in notes
4. Preserve all other fields unchanged
5. Write updated registry.json

### Step 9: Update scan-tracker and analytical notes

- Update claim counts in scan-tracker.json
- Update analytical-notes.md with new type distribution
- Note any specimens that lost all claims after drops (changed quality level)

### Step 10: Update site components

Only **2 files** contain hardcoded old type strings. Everything else flows through the type system.

**File 1: `site/lib/types/purpose-claims.ts`**
- Update the `ClaimType` union type: remove `"transformation-framing"`, `"employee-deal"`, `"sacrifice-justification"`, `"direction-under-uncertainty"`
- Add `"higher-calling"`, `"survival"`, `"commercial-success"`
- Final union: `"utopian" | "identity" | "teleological" | "higher-calling" | "survival" | "commercial-success"`
- Add `status?: string` to the `PurposeClaim` interface (for dropped claims with `"dropped-v2"`)

**File 2: `site/components/purpose-claims/claim-constants.ts`**
- Update `CLAIM_TYPE_LABELS`: remove old 4, add new 3 (`"higher-calling": "Higher Calling"`, `"survival": "Survival"`, `"commercial-success": "Commercial"`)
- Update `CLAIM_TYPE_COLORS`: remove old 4, assign colors to new 3. Suggested:
  - `higher-calling`: reuse rose tones (was employee-deal) — `{ bg: "bg-rose-50", text: "text-rose-600", border: "border-rose-300", hex: "#e11d48" }`
  - `survival`: reuse charcoal/slate tones (was sacrifice) — `{ bg: "bg-charcoal-50", text: "text-charcoal-600", border: "border-charcoal-200", hex: "#535657" }`
  - `commercial-success`: reuse sky tones (was direction) — `{ bg: "bg-sky-50", text: "text-sky-700", border: "border-sky-300", hex: "#0284c7" }`
- Update `CLAIM_TYPES_ORDER` to reflect new 6 types in meaningful order: `["utopian", "teleological", "higher-calling", "identity", "survival", "commercial-success"]`

**After updating both files:** Run `cd site && npm run build` to verify no TypeScript errors. The build will catch any component that references a removed type.

**Data loading:** The site reads `registry.json` directly. Dropped claims (with `"status": "dropped-v2"`) should be filtered out in the data access layer. Check `site/lib/data/` for the function that loads claims and add a filter: `claims.filter(c => c.status !== "dropped-v2")`.

---

## 4. Decision Rules for Edge Cases

When a claim could fit multiple new types:

1. **Ask: what END is the speaker invoking?** Not what they're talking about, but what justifies what they're talking about.
2. If genuinely ambiguous, use `secondaryType` field.
3. If the claim doesn't invoke any end beyond standard business operations, it's probably not a purpose claim — drop it.
4. When in doubt between higher-calling and teleological: if there's a *specific outcome* named (cure cancer, build safe superintelligence), it's teleological. If it's a *general moral obligation* (we owe it to patients, we choose science over profit), it's higher-calling.
5. When in doubt between survival and commercial-success: if the framing is *existential threat* (we'll be left behind, the old way is broken), it's survival. If the framing is *opportunity* (this will make us better), it's commercial-success.

### Critical: The old categories are GONE

Do NOT classify by surface content. The old types (transformation-framing, employee-deal, sacrifice-justification, direction-under-uncertainty) no longer exist. A claim that mentions job loss is NOT "employee-deal" — ask what END the speaker invokes to justify the job loss. A claim that mentions sacrifice is NOT "sacrifice-justification" — ask what END makes the sacrifice worthwhile. Always and only classify by the underlying end.

### Fields to preserve vs. update

- **`claimType`** — UPDATE to v2.0 type. This is the main change.
- **`secondaryType`** — UPDATE if applicable. A claim can invoke multiple ends. Keep this field.
- **`rhetoricalFunction`** — DO NOT UPDATE. This field describes what organizational work the claim does (authorizes investment, justifies sacrifice, resets expectations, etc.). That's a different dimension from what end it serves. The existing rhetoricalFunction descriptions remain valid under v2.0.
- **`taxonomyFlag`** — CLEAR any v1.0 flags that are resolved by the new taxonomy. Add new flags only for claims that genuinely don't fit v2.0.
- All other fields (text, speaker, source, context, etc.) — DO NOT TOUCH.

---

## 5. What This Enables

The v2.0 taxonomy creates a meaningful spectrum of ends:

```
utopian → teleological → higher-calling → identity → survival → commercial-success
```

These are six genuinely different ends that leaders invoke. They are NOT ranked from "better" to "worse" — commercial-success is as legitimate an end as utopian. The analytical payoff is:

1. **Leaders differ in what end they invoke.** Some justify AI transformation with commercial logic. Others invoke civilizational destiny. Others anchor to moral obligation. The *type of end* is itself a variable worth measuring.
2. **Industries may cluster.** Do pharma leaders reach for teleological ends (patients) more than tech leaders? Do financial services leaders cluster around commercial-success or survival?
3. **The same leader may invoke different ends for different audiences.** Earnings calls vs. internal memos vs. podcasts.
4. **The variation across ends is the interesting finding** for the ambidexterity project. We need commercial-success as a full category precisely because it provides the baseline — without it, we can't see the leaders who stay within business logic vs. those who reach beyond it.

---

## 6. Files to Modify

| File | What changes |
|------|-------------|
| `research/purpose-claims/PURPOSE-CLAIMS-SPEC.md` | Section 3 taxonomy, Section 10 changelog |
| `research/purpose-claims/registry.json` | claimType field for all 294 claims; status field for drops |
| `research/purpose-claims/scan-tracker.json` | Updated claim counts |
| `research/purpose-claims/analytical-notes.md` | New type distribution, updated hypotheses |
| `site/components/purpose-claims/claim-constants.ts` | New type enum, colors, labels |
| `HANDOFF.md` | Updated after completion |
| `APP_STATE.md` | Updated claim counts and taxonomy version |

---

## 7. Estimated Scope

- ~294 claims to review and reclassify
- ~30-40 claims likely to be dropped (mostly employee-deal + some transformation-framing/direction-under-uncertainty that are just business statements)
- Final registry: ~255-265 active claims across 6 types
- Execution: this is a careful analytical task, not a bulk operation. Each reclassification should be a judgment call about what end the claim serves.
- Recommend doing this in batches by old type: employee-deal first (smallest, clearest decisions), then sacrifice-justification, then transformation-framing, then direction-under-uncertainty, then quick review of the keepers.
