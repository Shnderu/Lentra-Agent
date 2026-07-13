class ArchaeologyIndex:

    """
    Central map of all legacy + active intelligence systems.
    Legacy references are metadata only and must not point to removed modules.
    """

    def __init__(self):

        self.legacy_modules = {
            "ranking_engine": "lentra.domain.scoring.ranking_engine",
            "duplicate_engine": "lentra.core.market_intelligence.duplicates",
            "area_engine": "lentra.core.market_intelligence.areas",
            "search_scoring": "removed_legacy_search_service",
            "old_intelligence": "lentra.core.market_intelligence.market_intelligence_engine"
        }

    def list_legacy(self):

        return list(self.legacy_modules.keys())

    def resolve(self, name: str):

        return self.legacy_modules.get(name, None)
