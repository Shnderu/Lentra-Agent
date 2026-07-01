"""
Import boundary enforcement for Market Intelligence OS.

This module prevents circular dependencies by enforcing strict layering rules.
"""

from typing import Set


_ALLOWED_IMPORTS: Set[str] = {
    # output layer can depend only on:
    "lentra.core.market_intelligence.decision",
}


def validate_import(module: str, target: str) -> None:
    """
    Hard boundary check.

    Raises ImportError if invalid dependency detected.
    """

    # Output layer restriction example
    if module.startswith("lentra.core.market_intelligence.output"):
        if not any(target.startswith(prefix) for prefix in _ALLOWED_IMPORTS):
            raise ImportError(
                f"[MI-ARCH] Illegal import: {module} -> {target}"
            )
