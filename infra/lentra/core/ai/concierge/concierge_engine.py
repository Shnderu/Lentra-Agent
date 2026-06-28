

from lentra.core.ai.concierge.planner.query_planner import plan_query
from lentra.core.ai.concierge.ranker.search_ranker import rank_listings
from lentra.core.ai.concierge.reasoner.reasoner import explain_choice

from lentra.core.market_intelligence.normalization.listing_normalizer import normalize_listing

from lentra.core.ai.feedback.store.feedback_store import log_feedback


class ConciergeEngine:

    def __init__(self, search_api):
        self.search_api = search_api

    def run(self, query: str, user_id="default"):

        plan = plan_query(query)

        # FIX: use RAW vector search output ONLY
        raw_candidates = self.search_api.search_candidates(query)

        # normalize ONLY (NO pipeline re-run)
        processed = [normalize_listing(c) for c in raw_candidates]

        ranked = rank_listings(processed, plan, user_id)

        results = []

        for l in ranked[:5]:

            results.append({
                "listing": l,
                "reason": explain_choice(l, plan)
            })

        return {
            "query": query,
            "plan": plan,
            "results": results
        }

    def feedback(self, user_id: str, listing_id: str, action: str):

        log_feedback(user_id, listing_id, action)

        return {"status": "ok"}
