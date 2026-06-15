from lentra.bot.services.registry import SearchService
from lentra.bot.state.state_store import StateStore
from lentra.bot.core.state_machine import StateMachine
from lentra.bot.core.snapshot import SnapshotEngine
from lentra.bot.core.ranker import AIRanker
from lentra.bot.core.saved import SavedSearches
from lentra.bot.core.recommendation import RecommendationEngine

from lentra.bot.events.registry import bus
from lentra.bot.events.core.emitter import EventEmitter


class SearchPipeline:

    def __init__(self):
        self.search = SearchService()
        self.state_store = StateStore()
        self.sm = StateMachine()
        self.snapshot = SnapshotEngine()
        self.ranker = AIRanker()
        self.saved = SavedSearches()
        self.reco = RecommendationEngine()

        self.emitter = EventEmitter(bus)

    async def execute(self, user_id: int, query: str):

        state = self.state_store.load(user_id)

        results = await self.search.search(query=query)

        results = self.ranker.rank(results, state.filters)

        results = self.reco.recommend(user_id, results)

        search_id = self.snapshot.build_search_id(query, state.filters)

        state = self.sm.set_list(state, results, query, search_id)

        state = self.saved.add(state, query)

        self.state_store.save(state)

        # EVENT: search completed
        await self.emitter.emit(
            "search_completed",
            user_id,
            {
                "query": query,
                "search_id": search_id,
                "results_count": len(results)
            }
        )

        return state
