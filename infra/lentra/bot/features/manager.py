from lentra.bot.features.base.context import FeatureContext
from lentra.bot.core.feature_registry import FeatureRegistry


class FeatureManager:
    """
    Executes registered features.
    """

    def __init__(self, registry: FeatureRegistry):
        self.registry = registry

    def execute(self, intent: str, ctx: FeatureContext) -> str:

        feature = self.registry.get(intent)

        if not feature:
            feature = self.registry.get("fallback")

        if not feature:
            return "No feature available"

        result = feature(ctx)

        return result
