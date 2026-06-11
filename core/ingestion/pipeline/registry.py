from core.ingestion.providers.facebook import FacebookProvider
from core.ingestion.providers.faswaz import FaswazProvider


class ProviderRegistry:
    def __init__(self):
        self.providers = [
            FacebookProvider(),
            FaswazProvider()
        ]

    def get_all(self):
        return self.providers
