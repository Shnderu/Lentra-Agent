import json
from typing import Any, Dict, List

from lentra.core.market_intelligence.normalization.listing_normalizer import (
    ListingNormalizer,
)

from lentra.core.data_layer.store.persistence import (
    PersistenceLayer,
)


class SearchAdapter:
    """
    SEARCH DATA ADAPTER

    Architecture:

        Seed / future connectors
                  |
                  v
        ListingNormalizer
                  |
                  v
        PersistenceLayer
                  |
                  v
        SearchPipeline


    Responsibility:
    - provide normalized listings
    - hide storage implementation
    - no intelligence logic here
    """

    def __init__(
        self,
        seed_path: str = "lentra/data/seeds/da_nang_seed_v1.json"
    ):

        self.seed_path = seed_path

        self.store = PersistenceLayer()

        self.normalizer = ListingNormalizer()

        self._initialized = False


    def _bootstrap(self):

        if self._initialized:
            return


        with open(
            self.seed_path,
            "r",
            encoding="utf-8"
        ) as f:

            raw_items = json.load(
                f
            )


        for item in raw_items:

            normalized = self.normalizer.normalize(
                item
            )

            self.store.upsert(
                normalized
            )


        self._initialized = True



    def build_objects(
        self,
        query: str
    ) -> List[Dict[str, Any]]:


        self._bootstrap()


        data = self.store.all()


        if not query:

            return []


        q = query.lower()


        scored = []


        for obj in data:

            text = (
                f"{obj.get('title','')} "
                f"{obj.get('description','')} "
                f"{obj.get('location','')}"
            ).lower()


            score = self._semantic_score(
                q,
                text
            )


            if score > 0:

                item = dict(
                    obj
                )

                item[
                    "relevance_score"
                ] = score


                scored.append(
                    item
                )


        if not scored:

            scored = [
                dict(item)
                for item in data
            ]


        return sorted(
            scored,
            key=lambda x: x.get(
                "relevance_score",
                0
            ),
            reverse=True
        )



    def _semantic_score(
        self,
        query: str,
        text: str
    ) -> int:

        score = 0


        if query in text:

            score += 10


        q_tokens = set(
            query.split()
        )

        t_tokens = set(
            text.split()
        )


        score += len(
            q_tokens & t_tokens
        )


        if (
            "da" in q_tokens
            and "nang" in q_tokens
            and "da nang" in text
        ):

            score += 5


        return score
