# ============================================================
# RENT SEARCH PIPELINE LEGACY COMPATIBILITY V5
# ============================================================

"""
LEGACY PIPELINE

This module is kept only for backward compatibility.

Canonical runtime path:

API
 |
CanonicalSearchEntrypoint
 |
CanonicalSearchPipeline
 |
Market Intelligence Core


This legacy delivery pipeline must not own:
- ranking
- market intelligence
- decision logic
"""


class SearchPipeline:

    def __init__(self):
        pass


    def run(
        self,
        query: str,
        candidates: list
    ):

        if not candidates:
            return []


        return {
            "query": query,
            "results": candidates,
            "count": len(candidates),
            "mode": "legacy_passthrough"
        }
