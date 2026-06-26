from typing import Dict, Any, Callable
from lentra.bot.core.feature_registry import FeatureRegistry


class IntentRouter:
    """
    Thin dispatcher layer.

    ONLY responsibility:
    intent -> feature lookup in registry
    """

    def __init__(self, registry: FeatureRegistry):
        self.registry = registry

    def get_feature(self, intent: Dict[str, Any]) -> Callable:
        """
        Strict lookup without fallback logic.
        """

        intent_type = intent.get("type")

        if not intent_type:
            raise ValueError("Intent missing 'type' field")

        feature = self.registry.get(intent_type)

        if not feature:
            raise KeyError(f"No feature registered for intent: {intent_type}")

        return feature
