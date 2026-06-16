from lentra.bot.domain.mapper import ItemMapper
from lentra.bot.core.cache import ResultCache


class SearchPipeline:

    def __init__(self, search_service, state_store, fsm, cache=None, renderer=None):

        self.search = search_service
        self.state_store = state_store
        self.fsm = fsm
        self.cache = cache or ResultCache(redis=None)
        self.renderer = renderer

    async def execute(self, user_id: int, query: str, message):

        state = self.state_store.load(user_id)

        raw = await self.search.search(query)

        items = ItemMapper.from_api(raw)

        search_id = f"search:{user_id}:{query[:10]}"

        if self.cache:
            self.cache.set_results(search_id, items)

        state = self.fsm.handle(state, {
            "type": "search_completed",
            "payload": {
                "results": items,
                "query": query,
                "search_id": search_id
            }
        })

        self.state_store.save(state)

        if self.renderer:
            await self.renderer.render(state, message)

        return state
