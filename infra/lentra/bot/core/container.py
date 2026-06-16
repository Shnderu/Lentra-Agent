from lentra.bot.state.state_store import StateStore
from lentra.bot.services.registry import Registry
from lentra.bot.services.search_pipeline import SearchPipeline
from lentra.bot.core.cache import ResultCache
from lentra.bot.core.fsm import FSMEngine
from lentra.bot.ux.renderer import UXRenderer


class Container:
    """
    CLEAN DI CONTAINER (LEVEL 9.2 STABLE)
    """

    def __init__(self):

        self.state_store = StateStore()

        self.registry = Registry()

        # infra dependencies
        self.cache = ResultCache(redis=self.state_store.redis)

        self.fsm = FSMEngine()

        self.renderer = UXRenderer(cache=self.cache)

        # service
        self.search_pipeline = SearchPipeline(
            search_service=self.registry.search_service,
            state_store=self.state_store,
            fsm=self.fsm,
            cache=self.cache,
            renderer=self.renderer
        )
