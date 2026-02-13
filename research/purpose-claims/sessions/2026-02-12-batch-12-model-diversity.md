# Purpose Claims Session: Batch 12 — Model Diversity
## February 12, 2026

**Batch theme:** One specimen per structural model (M2, M3, M6, plus M2 again) to test whether cross-model rhetorical patterns from Session 22 hold with new data.

**Registry:** 1,142 → 1,196 claims (+54)

---

## Specimens Scanned

| Specimen | Model | Claims | Quality | Distribution |
|----------|-------|--------|---------|-------------|
| Kroger | M2 | 12 | adequate | identity 4, commercial-success 5, teleological 2, higher-calling 1 |
| ExxonMobil | M6 | 12 | rich | commercial-success 7, identity 2, utopian 1, teleological 1, survival 1 |
| CrowdStrike | M3 | 16 | rich | survival 5, commercial-success 5, utopian 3, identity 3, higher-calling 2, teleological 1 |
| FedEx | M2 | 14 | rich | commercial-success 9, identity 4, utopian 1 |

---

## Field Journal Observations

### 1. CrowdStrike breaks the "industrial = no utopian" pattern

Session 19 established that non-tech/industrial CEOs produce zero utopian claims. CrowdStrike breaks this: Kurtz generates 3 utopian claims ("21st-century war with 20th-century weapons," "operators to orchestrators," "the agentic SOC isn't coming — it's here"). But cybersecurity's adversarial habitat makes epochal language authentic rather than performative — the threat IS civilizational. This suggests our `sector-rhetorical-signatures` insight needs refinement: the boundary isn't tech vs. non-tech but whether the industry's core problem is existential in nature. Defense (Anduril) and cybersecurity (CrowdStrike) have legitimate civilizational stakes that license elevated rhetoric. Grocery and logistics don't.

### 2. Rhetorical locus follows the structural center of AI capability

Kroger is the clearest case in the collection: Foster at 84.51° (the hub subsidiary) generates the richest, most varied purpose claims — spanning identity, higher-calling, teleological, and commercial-success. Both CEOs (McMullen and Sargent) are remarkably muted, sticking to operational language about berries and dinner inspiration. This maps onto the M2 model: the CoE leader carries the purpose-claims load, not the enterprise CEO. Contrast with FedEx (also M2 after audit) where Subramaniam dominates — but FedEx Dataworks is structurally closer to the CEO than 84.51° is to Kroger's CEO. Worth testing: does purpose rhetoric originate from the CoE/hub leader when that unit has organizational distinctness (separate subsidiary, separate brand)?

### 3. ExxonMobil's dual-identity phenomenon

Woods runs two distinct rhetorical tracks: internally AI is an operational efficiency tool (commercial-success), externally ExxonMobil is the enabler of the AI revolution — "low carbon power" for data centers that "alternatives such as nuclear simply can't match." The internal register is pure commercial-success; the external tilts teleological/utopian. This dual identity — internal AI adopter AND external AI enabler — may be unique to firms whose products become inputs to the AI ecosystem. NVIDIA is the closest parallel (makes chips AND uses AI internally). Could be a general pattern for "AI infrastructure providers" distinct from pure adopters.

### 4. Anti-hype as deliberate rhetorical strategy

Both Kroger ("we don't want to use AI just to use AI") and FedEx (backward-looking credibility, concrete dollar figures) practice purpose through restraint. They define organizational character by what they refuse to do — no trend-chasing, no grand promises, no epochal language. McMullen talking about berry freshness is as deliberate a rhetorical choice as Zuckerberg talking about AGI. FedEx's Subramaniam anchors in specific numbers ($1.8B of $4B savings from technology, $180M from AI image capture) — an engineer's approach to purpose rhetoric. The anti-hype register may be a retail/logistics pattern OR a CEO personality variable. Need more data to distinguish.

### 5. The layoff-purpose arc (CrowdStrike)

Kurtz's May 2025 layoff memo → September 2025 Fal.Con keynote is the most transparent example of purpose claims doing organizational work across time. The rhetorical function shifts from authorization ("AI flattens our hiring curve" = why we had to cut) to reassurance ("you are the human conscience of cyber defense" = why you still matter). The 4-month gap suggests deliberate calibration. Connects to `purpose-structure-complementarity`: purpose claims aren't just describing, they're managing the organizational consequences of structural decisions.

### 6. CrowdStrike's militarized register is habitat-driven

"AI war," "weapons," "adversaries," "double-edged sword" — language that would sound overwrought in pharma or banking is authentic in cybersecurity. The adversarial framing creates a structural feedback loop: CrowdStrike must adopt AI because adversaries are adopting AI, and customers must adopt CrowdStrike's AI because their adversaries are adopting AI. Circular logic that is both rhetorically effective and economically grounded. No other specimen in the collection uses martial language this consistently.

### 7. McMullen resignation creates a rhetorical gap at Kroger

McMullen resigned March 2025; Sargent (interim CEO) anchors in basic identity ("We care for people, and we love food"). The purpose rhetoric gap may be temporary (awaiting permanent CEO) or structural (Kroger's culture delegates AI rhetoric to the hub, not the enterprise CEO). Worth watching: when Kroger names a permanent CEO, does the new leader inject purpose rhetoric or maintain the hub-centric pattern?

---

## Cross-Model Pattern Check

Session 22 identified two cross-model patterns. Batch 12 provides partial test:

**Pattern A: Structural separation licenses non-commercial rhetoric** (explore models 14.2% vs execute models 28.5% commercial-success)
- CrowdStrike (M3, execute-oriented): 31% commercial-success (5/16) — slightly above the 28.5% benchmark
- Kroger (M2, execute-oriented): 42% commercial-success (5/12) — well above
- FedEx (M2, execute-oriented): 64% commercial-success (9/14) — far above
- ExxonMobil (M6, execute-oriented): 58% commercial-success (7/12) — far above
- **Verdict: Consistent.** All 4 execute-oriented models show high commercial-success rates. CrowdStrike is the lowest, which makes sense — its adversarial habitat pushes toward survival/utopian even though the structure is execute-oriented.

**Pattern B: M9 teleological concentration** (23.1% teleological)
- Not testable this batch (no M9 specimens).

---

## Merge Details

- Script: `scripts/merge-batch12-claims.py`
- 54 claims merged, 0 duplicates
- 4 enrichment files written to `research/purpose-claims/enrichment/`
- 4 pending files moved to `research/purpose-claims/pending/processed/`
- Registry: 1,142 → 1,196 claims across ~59 scanned specimens
