

from lentra.api.search.search_api import SearchAPI


class ConciergeEngine:

    def __init__(self, search_api=None):
        self.api = search_api or SearchAPI()

    def run(self, query: str):

        plan = {
            "max_price": 700,
            "location": "My My",
            "must_have": ["internet"],
            "noise_sensitive": False,
            "internet_required": True
        }

        results = self.api.search_candidates(query)

        print(f"[CONCIERGE] RESULTS COUNT: {len(results)}")

        return {
            "query": query,
            "plan": plan,
            "results": results
        }

    def feedback(self, session_id, listing_id, action):
        return {
            "session_id": session_id,
            "listing_id": listing_id,
            "action": action,
            "status": "ok"
        }
