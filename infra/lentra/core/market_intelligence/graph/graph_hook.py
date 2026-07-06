"""
CORE HOOK = DECLARATIVE ONLY
"""

class GraphHook:

    def meta(self):
        return {
            "hook": "core_only",
            "runtime": False
        }
