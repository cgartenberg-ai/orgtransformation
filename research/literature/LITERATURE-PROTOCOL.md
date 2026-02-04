# Literature Update Protocol

Follow these steps exactly. Do NOT skip steps.

---

## Step 1: Inventory — What's Already Processed

1. Read `research/literature/registry.json`
2. Extract every `sourceFile` value from the `papers` array into a set called `REGISTRY_FILES`
3. Also extract every `id` value into a set called `REGISTRY_IDS`
4. List all `.json` files in `research/literature/drafts/` (excluding `merged/` subdirectory) into a set called `EXISTING_DRAFTS`

Report:
- "Registry contains N papers"
- "Drafts directory contains N pending drafts"

## Step 2: Scan — What Papers Exist

1. List all `.pdf` files in `library/research papers/` (non-recursive — just the top level)
2. For each PDF, record the filename

Report:
- "Found N PDFs in library/research papers/"

## Step 3: Diff — What's New

For each PDF found in Step 2, check:
1. Is its filename (as a relative path `library/research papers/FILENAME`) present in `REGISTRY_FILES`? If yes → skip (already in registry)
2. Does a draft JSON already exist in `EXISTING_DRAFTS` whose contents reference this filename in `sourceFile`? If yes → skip (draft already generated)
3. Otherwise → mark as NEW

Report:
- "N papers already in registry"
- "N papers have existing drafts"
- "N NEW papers to process"
- List the new papers by filename

If there are 0 new papers, stop here and report "All papers are already processed."

## Step 4: Spawn — Create One Agent Per New Paper

For each NEW paper, spawn a background Task agent (subagent_type: "general-purpose") with:

**The prompt** should be constructed from the agent template in `research/literature/AGENT-TEMPLATE.md` with these substitutions:
- `{{PDF_PATH}}` → Full absolute path to the PDF
- `{{OUTPUT_PATH}}` → `research/literature/drafts/{id}.json` where `{id}` is derived from the filename (author-year format, kebab-case)
- `{{PAPER_FILENAME}}` → The PDF filename as it appears in the directory

**Deriving the draft ID from filename:**
- `Azoulay_Lerner.pdf` → `azoulay-lerner`
- `cohen-levinthal-1990-AbsorptiveCapacity.pdf` → `cohen-levinthal-1990`
- `Henderson-ArchitecturalInnovationReconfiguration-1990.pdf` → `henderson-clark-1990-pdf`
- `Garicano.pdf` → `garicano-2000-pdf`
- Use judgment for ambiguous cases. The id should be `authorlastname-year` format.

**Spawn all agents in a SINGLE message** (parallel tool calls) for maximum efficiency.

Report:
- "Spawned N agents"
- List each: "Agent for {filename} → drafts/{id}.json"

## Step 5: Monitor — Wait for Completion

Wait for all agents to complete. As each finishes, note success or failure.

Report:
- "N/N agents completed successfully"
- List any failures with error details

## Step 6: Validate — Check Draft Quality

For each completed draft JSON:
1. Read the file
2. Check required fields are present and non-empty: `id`, `citation`, `authors`, `year`, `journal`, `tradition`, `keyMechanism`, `predictionForAI`, `sourceFile`
3. Check `tradition` is one of: `org-econ`, `innovation`, `strategy`, `social-psych`, `other`
4. Check `status` is `"candidate"`
5. Check `year` is a number

Report:
- Summary table: id | authors | year | tradition | valid?
- Flag any issues

## Step 7: Merge — Add to Registry (User Approval Required)

**Do NOT auto-merge. Ask the user first.**

Present the user with:
1. A summary of all valid drafts
2. Ask: "Which entries should I merge into registry.json? (all / list specific IDs / none — I'll review first)"

If user approves:
1. Read current `research/literature/registry.json`
2. For each approved draft:
   - Read the draft JSON
   - Append to the `papers` array
3. Update `lastUpdated` to today's date
4. Write updated `registry.json`
5. Delete merged draft files (or move to `research/literature/drafts/merged/`)

Report:
- "Merged N entries into registry.json"
- "Registry now contains N total papers"

---

## Error Recovery

- If an agent fails, the draft won't exist. Re-run `/update-literature` to retry — the idempotency check will only spawn agents for missing drafts.
- If a draft JSON is malformed, delete it and re-run.
- If the skill is interrupted mid-spawn, re-run — already-spawned agents will complete independently, and the idempotency check prevents duplicates.
