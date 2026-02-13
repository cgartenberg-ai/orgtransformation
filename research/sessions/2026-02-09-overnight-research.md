    # Overnight Research Run — 2026-02-09

    **Started:** 2026-02-08 21:16
    **Duration:** 419 minutes
    **Targets scanned:** 36
    **Succeeded:** 32
    **Failed:** 4
    **Method:** `scripts/overnight-research.py` via `claude -p --model opus`

    ## Results

    | Company | Q | Status | Model | Quotes | Time |
    |---------|---|--------|-------|--------|------|
    | Apple                          | Q1 | ✓ | M4 | 8 quotes | 289s |
| AMD                            | Q2 | ✗ | M? | 0 quotes | 1500s |
| Anduril                        | Q2 | ✓ | M9 | 8 quotes | 280s |
| Ford                           | Q2 | ✓ | M4 | 10 quotes | 292s |
| General Motors                 | Q2 | ✓ | M4 | 4 quotes | 284s |
| Intel                          | Q2 | ✓ | M4 | 9 quotes | 1804s |
| Lockheed Martin                | Q2 | ✓ | M4 | 8 quotes | 293s |
| Mayo Clinic                    | Q2 | ✓ | M4 | 9 quotes | 273s |
| Toyota                         | Q2 | ✓ | M4 | 5 quotes | 310s |
| UnitedHealth Group             | Q2 | ✓ | M4 | 7 quotes | 279s |
| Disney                         | Q3 | ✓ | M4 | 11 quotes | 320s |
| Caterpillar                    | Q4 | ✗ | M? | 0 quotes | 1500s |
| Deere & Co                     | Q4 | ✓ | M4 | 3 quotes | 264s |
| ExxonMobil                     | Q4 | ✓ | M6 | 3 quotes | 1802s |
| Honeywell                      | Q4 | ✓ | M4 | 10 quotes | 320s |
| BMW                            | Q2 | ✓ | M4 | 5 quotes | 282s |
| CVS Health                     | Q2 | ✓ | M4 | 5 quotes | 289s |
| Mercedes-Benz                  | Q2 | ✓ | M4 | 11 quotes | 299s |
| Mount Sinai Health System      | Q2 | ✓ | M4 | 8 quotes | 372s |
| Sutter Health                  | Q2 | ✓ | M4 | 8 quotes | 335s |
| Bloomberg                      | Q3 | ✓ | M4 | 10 quotes | 311s |
| Comcast / NBCUniversal         | Q3 | ✗ | M? | 0 quotes | 1500s |
| Netflix                        | Q3 | ✓ | M4 | 9 quotes | 332s |
| Progressive                    | Q3 | ✓ | M6 | 1 quotes | 300s |
| T-Mobile                       | Q3 | ✓ | M4 | 7 quotes | 296s |
| Visa                           | Q3 | ✓ | M4 | 3 quotes | 216s |
| FedEx                          | Q4 | ✓ | M4 | 10 quotes | 323s |
| Kroger                         | Q4 | ✓ | M4 | 5 quotes | 318s |
| NextEra Energy                 | Q4 | ✗ | M? | 0 quotes | 1500s |
| Nike                           | Q4 | ✓ | M4 | 2 quotes | 301s |
| PepsiCo                        | Q4 | ✓ | M4 | 9 quotes | 315s |
| Uber                           | Q4 | ✓ | M4 | 6 quotes | 330s |
| Blue Origin                    | Q2 | ✓ | M6 | 8 quotes | 386s |
| Honda                          | Q2 | ✓ | M4 | 5 quotes | 315s |
| Lowe's                         | Q4 | ✓ | M4 | 10 quotes | 304s |
| Ulta Beauty                    | Q4 | ✓ | M4 | 8 quotes | 289s |

    ## Next Steps

    - Review pending/*.json files for quality
    - Run `/curate` to create specimen files from research findings
    - Run `overnight-purpose-claims.py` for newly created specimens
