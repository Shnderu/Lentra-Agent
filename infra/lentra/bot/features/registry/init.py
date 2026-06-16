from lentra.bot.features.rent_search.service import RentSearchService


class FeatureRegistry:
    def __init__(self, container):
        self.container = container
        self.rent_search = container.rent_search_service


def build_feature_registry(container):
    return FeatureRegistry(container)
