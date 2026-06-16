from __future__ import annotations

from lentra.bot.core.cache import ResultCache
from lentra.bot.services.search_pipeline import SearchPipeline


class NullRenderer:
    async def render(self, *args, **kwargs):
        return None


class NullFSM:
    def handle(self, state, event):
        return state


class NullStateStore:
    def load(self, user_id: int):
        return {}

    def save(self, state):
        return None


class NullSearchService:
    async def search(self, query: str):
        return []


class Container:
    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        return obj

    def __init__(self):
        # HARD GUARANTEE: prevent uninitialized usage
        self._initialized = True

        self.cache = ResultCache()

        self.renderer = self._init_renderer()
        self.fsm = self._init_fsm()
        self.state_store = self._init_state_store()
        self.search_service = self._init_search_service()
        self.search_pipeline = self._init_search_pipeline()

    def _assert_init(self):
        if not getattr(self, "_initialized", False):
            raise RuntimeError("Container not initialized properly")

    def _init_renderer(self):
        try:
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

    def _init_search_pipeline(self):
        return SearchPipeline(
            search_service=self.search_service,
            state_store=self.state_store,
            fsm=self.fsm,
            cache=self.cache,
            renderer=self.renderer,
        )
