from __future__ import annotations

from lentra.bot.core.cache import ResultCache
from lentra.bot.services.search_pipeline import SearchPipeline


class Container:
    """
    Stable DI container.
    System must boot even if optional services are broken.
    """

    def __init__(self):
        # single cache implementation
        self.cache = self._init_cache()

        # pipeline
        self.search_pipeline = self._init_search_pipeline()

    def _init_cache(self):
        try:
            return ResultCache()
        except Exception:
            return ResultCache()

    def _init_search_pipeline(self):
        try:
            return SearchPipeline(
                cache=self.cache
            )
        except Exception:
            return SearchPipeline(
                cache=self.cache
            )
