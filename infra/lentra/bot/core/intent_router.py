from typing import Dict, Any
from lentra.bot.core.feature_registry import FeatureRegistry


class IntentRouter:
    """
    Routes intent → feature via registry.
    """

    def __init__(self, registry: FeatureRegistry):
        self.registry = registry

    async def route(self, intent: str, ctx: Dict[str, Any]):
        feature = self.registry.get(intent)

        if not feature:
            feature = self.registry.get("fallback")

        if not feature:
            return "No feature available"

        return await feature(ctx)
