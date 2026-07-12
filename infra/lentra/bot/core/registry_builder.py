from lentra.bot.core.feature_registry import FeatureRegistry


def build_registry(
    rent_search_handler=None
) -> FeatureRegistry:

    registry = FeatureRegistry()

    registry.register(
        "fallback",
        lambda ctx: {
            "status": "fallback"
        }
    )

    if rent_search_handler:

        registry.register(
            "rent_search",
            rent_search_handler
        )

    return registry
