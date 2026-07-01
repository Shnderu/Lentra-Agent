from typing import Set


class MarketIntelligenceDependencyGuard:
    """
    Enforces strict dependency boundaries inside Market Intelligence core.

    RULES:
    - decision layer CANNOT import output layer
    - output layer CANNOT import decision layer
    - engine is the only orchestrator
    """

    FORBIDDEN_IMPORTS: Set[str] = {
        "lentra.core.market_intelligence.output",
        "lentra.core.market_intelligence.decision.signal_authority_resolver",
    }

    ALLOWED_ROOTS: Set[str] = {
        "lentra.core.market_intelligence",
    }

    @classmethod
    def validate_import(cls, module_name: str, from_module: str) -> None:
        """
        Runtime import safety check.

        Raises:
            ImportError if forbidden dependency detected
        """

        for forbidden in cls.FORBIDDEN_IMPORTS:
            if module_name.startswith(forbidden):
                raise ImportError(
                    f"[MI-GUARD] Forbidden dependency detected: {from_module} → {module_name}"
                )

    @classmethod
    def is_allowed_context(cls, module_name: str) -> bool:
        return any(module_name.startswith(root) for root in cls.ALLOWED_ROOTS)
