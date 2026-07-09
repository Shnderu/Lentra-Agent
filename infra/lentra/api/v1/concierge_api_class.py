from lentra.core.pipeline.canonical_search_pipeline import (
    CanonicalSearchPipeline
)

from lentra.core.pipeline.canonical_entrypoint import (
    CanonicalSearchEntrypoint
)

from lentra.core.pipeline.search_pipeline import SearchPipeline



class ConciergeAPIv1:

    def __init__(self):

        self.pipeline = CanonicalSearchPipeline(
            SearchPipeline()
        )

        self.entrypoint = CanonicalSearchEntrypoint(
            self.pipeline
        )


    def search(
        self,
        query: str
    ):

        raw_listing = {

            "id": "api-1",

            "title": query,

            "price": 600,

            "market_avg": 550,

            "currency": "USD",

            "city": "Da Nang",

            "location": "My Khe",

            "source": "api",

            "query": query

        }


        return self.entrypoint.execute(
            {
                "query": query,
                "objects": [
                    raw_listing
                ]
            }
        )
