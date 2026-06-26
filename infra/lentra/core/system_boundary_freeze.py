"""
IMPORT GRAPH FREEZE v1

RULES:
1. FORBIDDEN:
   - app.core.*
   - app.*
2. ALLOWED:
   - lentra.core.*
   - lentra.worker.*
   - lentra.runtime.*
   - lentra.bot.*
   - lentra.telegram.*

3. FLOW RULE:
   worker -> engine -> FlowGlue -> intent_router + scenario_engine

"""

FORBIDDEN_PREFIXES = [
    "app.core",
    "app."
]

ALLOWED_PREFIXES = [
    "lentra.core",
    "lentra.worker",
    "lentra.runtime",
    "lentra.bot",
    "lentra.telegram"
]


def validate_import(module: str):
    for f in FORBIDDEN_PREFIXES:
        if module.startswith(f):
            raise ImportError(f"LEGACY IMPORT BLOCKED: {module}")

    return True
