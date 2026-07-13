"""
COMPAT LAYER v1
Legacy search_engine bridge

DO NOT EXTEND ARCHITECTURE HERE.
This exists only to unblock API startup.
"""

class SearchEngineCompat:
    def search(self, query: str):
        # redirect to scenario/intent layer in future
        return {
            "query": query,
            "result": "compat_stub",
            "warning": "search_engine is deprecated"
        }

search_engine = SearchEngineCompat()


def search(query: str) -> dict:
    """
    Minimal module-level search contract.

    Exposes:
        from core.search.engine import search

    Returns a dict with at least:
        {
          "query": str,
          "results": list,
          "status": "ok"
        }
    """
    return {
        "query": query,
        "results": [],
        "status": "ok",
    }
