"""
ARCHITECTURE RULES (ENFORCED BY DESIGN)
"""

PIPELINE_MUST_BE_SINGLE = True

ALLOWED_FLOW = [
    "search",
    "ranking",
    "aggregation"
]

FORBIDDEN:
# - skipping steps
# - branching execution outside pipeline
