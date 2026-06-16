from lentra.bot.features.registry.feature_registry import FeatureRegistry
from lentra.bot.features.registry.feature_keys import FeatureKeys

from lentra.bot.features.rent_search.service import RentSearchService


def build_feature_registry(container) -> FeatureRegistry:
    registry = FeatureRegistry()

    # RENT SEARCH feature
    registry.register(
        FeatureKeys.RENT_SEARCH,
        RentSearchService(
            repository=container.rent_repository
        )
    )

    return registry
