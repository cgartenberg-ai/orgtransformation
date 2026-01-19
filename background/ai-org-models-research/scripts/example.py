#!/usr/bin/env python3
"""
AI Organizational Models Research - Search Helper

Example usage patterns for researching AI organizational models.
These are search query templates, not executable automation.
"""

# Search query templates for different source types

SEC_FILING_QUERIES = [
    '10-K "artificial intelligence" "research and development"',
    '10-K "machine learning" "capital expenditure"',
    'DEF 14A "AI" "executive compensation"',
    '8-K "AI" "strategic initiative"',
]

PODCAST_SEARCH_TERMS = [
    "AI lab",
    "AI incubator",
    "AI spin-off",
    "product venture lab",
    "zero to one AI",
    "internal AI startup",
]

PRESS_SEARCH_PATTERNS = [
    '"Chief AI Officer" appointed',
    '"AI lab" launched',
    '"AI incubator" corporate',
    '"AI venture" internal',
]

LINKEDIN_SEARCH_PATTERNS = [
    'title:"Chief AI Officer"',
    'title:"VP AI"',
    'title:"Head of AI"',
    'title:"AI Research Director"',
]

def print_search_queries():
    """Print all search query templates."""
    print("=== SEC Filing Queries ===")
    for q in SEC_FILING_QUERIES:
        print(f"  {q}")

    print("\n=== Podcast Search Terms ===")
    for q in PODCAST_SEARCH_TERMS:
        print(f"  {q}")

    print("\n=== Press Search Patterns ===")
    for q in PRESS_SEARCH_PATTERNS:
        print(f"  {q}")

    print("\n=== LinkedIn Search Patterns ===")
    for q in LINKEDIN_SEARCH_PATTERNS:
        print(f"  {q}")

if __name__ == "__main__":
    print_search_queries()
