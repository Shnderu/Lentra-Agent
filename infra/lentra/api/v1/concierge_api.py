

from lentra.api.search.search_api import SearchAPI
from lentra.core.ai.concierge.concierge_engine import ConciergeEngine
from lentra.core.pipeline.safe_runner import safe_run
from lentra.core.contracts.v1.response_schema import build_response


class ConciergeAPIv1:

    def __init__(self):
        self.engine = ConciergeEngine(SearchAPI())

    def search(self, query):

        raw = self.engine.run(query)

        if "error" in raw:
            return raw

        return build_response(
            query=raw["query"],
            plan=raw["plan"],
            results=raw["results"]
        )
