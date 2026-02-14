# Data Changelog

Append-only audit log. Every automated script that modifies data files logs here.

Format: `## YYYY-MM-DD HH:MM:SS — script-name` followed by bullet points.

---

## 2026-02-14 13:47:43 — fix-contingencies-talent (inline)
- Merged non-traditional (1 specimens) into nonTraditional -> 7 unique specimens
- Removed redundant talent-rich (1) and talent-constrained (1) keys


## 2026-02-14 13:48:09 — fix-contingencies-talent
- Merged non-traditional (6) into nonTraditional -> 12 unique specimens
- Moved 18 talent-rich-only specimens to high: ['apple', 'blue-origin', 'bmw', 'bosch-bcai', 'crowdstrike', 'disney', 'google-deepmind', 'intel', 'lionsgate', 'mercedes-benz', 'netflix', 'nike', 'recruit-holdings', 'salesforce', 'sap', 'tesla', 'thomson-reuters', 'uber']
- Moved 14 talent-constrained-only specimens to low: ['delta-air-lines', 'dow-chemical', 'exxonmobil', 'ford', 'general-motors', 'honda', 'honeywell', 'hp-inc', 'hyundai-robotics', 'intel', 'lockheed-martin', 'panasonic', 'toyota', 'ulta-beauty']
- Removed redundant talent-rich and talent-constrained keys


## 2026-02-14 13:49:02 — fix-registry-gov-specimens
- nasa: Active -> Inactive
- new-york-state: Stub -> Inactive
- pentagon-cdao: Active -> Inactive
- us-air-force: Stub -> Inactive
- us-cyber-command: Stub -> Inactive
- Registry totalSpecimens: 149 -> 144 (excluding 5 inactive)


## 2026-02-14 13:50:09 — fix-gov-specimen-files
- nasa.json: meta.status Active -> Inactive
- us-cyber-command.json: meta.status Stub -> Inactive
- new-york-state.json: meta.status Stub -> Inactive
- us-air-force.json: meta.status Stub -> Inactive
- pentagon-cdao.json: meta.status Active -> Inactive


## 2026-02-14 13:51:41 — tag-null-url-sources
- Tagged 172 null-URL sources across 55 specimens
-   [paywall]: 5, [no URL]: 167


## 2026-02-14 13:53:07 — backfill-insight-sessions
- healthcare-governance-enables-scale: discoveredIn -> synthesis/sessions/2026-02-09-synthesis-batch3.md
- services-business-model-crisis: discoveredIn -> synthesis/sessions/2026-02-09-synthesis-batch3.md
- ai-chief-scientist-governance-signal: discoveredIn -> synthesis/sessions/2026-02-09-synthesis-batch3.md
- aero-defense-structural-divergence: discoveredIn -> synthesis/sessions/2026-02-09-synthesis-batch5.md
- contextual-via-education: discoveredIn -> synthesis/sessions/2026-02-09-synthesis-batch5.md
- government-caio-instability: discoveredIn -> synthesis/sessions/2026-02-09-synthesis-batch5.md
- ai-native-no-structure-paradox: discoveredIn -> synthesis/sessions/2026-02-09-synthesis-batch5.md
- media-serve-creativity-framing: discoveredIn -> synthesis/sessions/2026-02-09-synthesis-batch6.md
- retail-no-caio-pattern: discoveredIn -> curation/sessions/2026-02-12-m4-taxonomy-audit.md
- telecom-structural-divergence: discoveredIn -> pre-session-tracking
- ai-cic-intermediate-form: discoveredIn -> pre-session-tracking
- ai-disruption-negative-specimens: discoveredIn -> synthesis/sessions/2026-02-12-batch7-placement.md
- ai-code-generation-internal-transformation: discoveredIn -> synthesis/sessions/2026-02-09-synthesis-batch8.md
- capex-commitment-device: discoveredIn -> pre-session-tracking
- ai-washing-as-classification-signal: discoveredIn -> pre-session-tracking
- customer-adoption-as-ai-structural-maturity-indicator: discoveredIn -> synthesis/sessions/2026-02-09-synthesis-batch9.md
- heritage-as-authorization: discoveredIn -> research/purpose-claims/sessions/2026-02-13-batch-13-14-insights.md
- audience-dependent-claim-ordering: discoveredIn -> research/purpose-claims/sessions/2026-02-13-batch-13-14-insights.md
- ceo-departure-natural-experiment: discoveredIn -> research/purpose-claims/sessions/2026-02-13-batch-13-14-insights.md
- mission-identity-anodyne-rhetoric: discoveredIn -> synthesis/sessions/2026-02-13-finserv-healthcare-botanist.md

