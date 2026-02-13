    # Overnight Curate Run — 2026-02-09

    **Started:** 2026-02-09 07:23
    **Duration:** 1 minutes
    **Curated:** 1 | **New:** 1 | **Updated:** 0 | **Failed:** 0
    **Method:** `scripts/overnight-curate.py` via `claude -p --model opus`

    ## Results

    | Specimen                       | Action  | Model | Orientation | Conf.  | Compl. | Quotes | Sources | Time   |
    |--------------------------------|---------|-------|-------------|--------|--------|--------|---------|--------|
    | apple                          | new     | M4  | Structural  | Medium | High   |      8 |       8 |    74s |

    ## Model Distribution (this batch)

    | Model                                | Count | Existing | New Total |
    |--------------------------------------|-------|----------|-----------|
    | M4 Hybrid/Hub-and-Spoke           |     1 |       28 |        29 |

    ## Orientation Distribution

    | Orientation | Count |
    |-------------|-------|
    | Structural  |     1 |

    ## Confidence Distribution

    | Level  | Count |
    |--------|-------|
    | Medium |     1 |

    ## Industries Covered

    | Industry                  | Count |
    |---------------------------|-------|
    | Big Tech                  |     1 |

    ## Taxonomy Feedback (collected from specimens)

    - **apple**: Apple's restructure is a clean M4 Hub-and-Spoke case: central standards/research coordination (Subramanya) with distributed execution across functional SVPs. The functional organizational structure (vs. product divisions) creates an interesting variant where 'spokes' are expertise-based rather than product-based.
- **apple**: The transition from Giannandrea's centralized SVP-level team to Subramanya's VP-level hub under Federighi may signal reduced organizational prominence for AI-as-separate-function in favor of AI-as-embedded-capability.

    ## Skipped Files

    | File                                               | Reason                     |
    |----------------------------------------------------|----------------------------|
    | earnings-discovery-q4-2025.json                    | Multi-company session file |
| earnings-q4-2025-amazon-google.json                | Multi-company session file |
| financial-services-earnings-q4-2025.json           | Multi-company session file |
| general-sweep-feb-2026-v2.json                     | Multi-company session file |
| general-sweep-feb-2026.json                        | Multi-company session file |
| goldman-sachs-deep-scan.json                       | Multi-company session file |
| morgan-stanley-deep-scan.json                      | Multi-company session file |
| pharma-earnings-q4-2025.json                       | Multi-company session file |
| podcast-deep-scan-feb-2026.json                    | Multi-company session file |
| podcast-substack-feed-check.json                   | Multi-company session file |

    ## Failed Specimens

    | Specimen                       | Error                                              |
    |--------------------------------|----------------------------------------------------|
    | (none) | |

    ## Next Steps

    - Run `/synthesize` to process 1 newly queued specimens
    - Run `overnight-purpose-claims.py` for 1 newly created specimens
    - Review failed specimens in `research/curate-retry-queue.json`
    - Process 10 multi-company session files via interactive `/curate`
