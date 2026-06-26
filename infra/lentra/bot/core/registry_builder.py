from lentra.bot.core.feature_registry import FeatureRegistry


def build_registry() -> FeatureRegistry:
    registry = FeatureRegistry()

    # TODO: регистрация feature handlers
    registry.register("fallback", lambda ctx: {"status": "fallback"})

    return registry
