from __future__ import annotations

from dataclasses import dataclass

from lentra.bot.core.cache import Cache, ResultCache
from lentra.bot.services.search_pipeline import SearchPipeline


# ---- SAFE DEFAULTS (NO-FAIL STUBS) ----

class NullRenderer:
    async def render(self, *args, **kwargs):
        return None


class NullFSM:
    def handle(self, state, event):
        return state


class NullSearchService:
    async def search(self, query: str):
        return []


class NullStateStore:
    def load(self, user_id: int):
        return {}

    def save(self, state):
        return None


# ---- CONTAINER ----

class Container:
    """
    Stable DI container.

    Key principle:
    - NEVER raise during construction
    - ALWAYS produce usable defaults
    - system must boot even with broken services
    """

    def __init__(self):
        # core primitives
        self.cache = self._init_cache()
        self.result_cache = self._init_result_cache()

        # infrastructure services (safe fallbacks)
        self.renderer = self._init_renderer()
        self.fsm = self._init_fsm()
        self.state_store = self._init_state_store()
        self.search_service = self._init_search_service()

        # pipelines
        self.search_pipeline = self._init_search_pipeline()

    # ---------------- CACHE ----------------

    def _init_cache(self) -> Cache:
        try:
            return Cache()
        except Exception:
            return Cache()

    def _init_result_cache(self) -> ResultCache:
        try:
            return ResultCache()
        except Exception:
            return ResultCache()

    # ---------------- SERVICES ----------------

    def _init_renderer(self):
        try:
            # optional real renderer (if exists in project)
            from lentra.bot.core.renderer import UXRenderer
            return UXRenderer(cache=self.cache)
        except Exception:
            return NullRenderer()

    def _init_fsm(self):
        try:
            from lentra.bot.core.fsm import FSM
            return FSM()
        except Exception:
            return NullFSM()

    def _init_state_store(self):
        try:
            from lentra.bot.core.state_store import StateStore
            return StateStore()
        except Exception:
            return NullStateStore()

    def _init_search_service(self):
        try:
            from lentra.bot.services.search_service import SearchService
            return SearchService()
        except Exception:
            return NullSearchService()

    # ---------------- PIPELINES ----------------

    def _init_search_pipeline(self):
        try:
            return SearchPipeline(
                search_service=self.search_service,
                state_store=self.state_store,
                fsm=self.fsm,
                cache=self.result_cache,
                renderer=self.renderer,
            )
        except Exception:
            # absolute fallback — bot must start always
            return SearchPipeline(
                search_service=NullSearchService(),
                state_store=NullStateStore(),
                fsm=NullFSM(),
                cache=self.result_cache,
                renderer=NullRenderer(),
            )
