import json
import redis

from lentra.bot.state.session import SessionState
from lentra.bot.state.state_store import StateStore

from lentra.bot.services.search_service import SearchService
from lentra.bot.core.state_machine import StateMachine
from lentra.bot.core.snapshot import SnapshotEngine
from lentra.bot.core.ranker import AIRanker
from lentra.bot.core.saved import SavedSearches
from lentra.bot.core.recommendation import RecommendationEngine

from lentra.bot.cards.builder import CardBuilder
from lentra.bot.cards.renderer import CardRenderer
from lentra.bot.cards.detail import CardDetailEngine

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

        self.cards = CardBuilder()
        self.renderer = CardRenderer()
        self.detail = CardDetailEngine()

        self.emitter = EventEmitter(bus)

    async def execute(self, user_id: int, query: str):

        state = self.state_store.load(user_id)

        results = await self.search.search(query=query)

        results = self.ranker.rank(results, state.filters)
        results = self.reco.recommend(user_id, results)

        search_id = self.snapshot.build_search_id(query, state.filters)

        state = self.sm.set_list(state, results, query, search_id)
        state = self.saved.add(state, query)

        # === UX LAYER: build cards ===
        cards = [self.cards.build(r.__dict__ if hasattr(r, "__dict__") else r) for r in results]

        # render list text (first page only for now)
        rendered_cards = [self.renderer.render_list_card(c) for c in cards[:5]]

        state.results = [
            {
                "id": c.id,
                "text": txt
            }
            for c, txt in zip(cards[:5], rendered_cards)
        ]

        self.state_store.save(state)

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
