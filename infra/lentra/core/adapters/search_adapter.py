import json
from typing import Any, Dict, List

from lentra.core.market_intelligence.normalization.listing_normalizer import (
    ListingNormalizer,
)


class SearchAdapter:

    def __init__(
        self,
        seed_path: str = "lentra/data/seeds/da_nang_seed_v1.json"
    ):

        self.seed_path = seed_path
        self._cache = None
        self.normalizer = ListingNormalizer()


    def _load(self):

        if self._cache is None:

            with open(
                self.seed_path,
                "r"
            ) as f:

                self._cache = json.load(
                    f
                )

        return self._cache


    def build_objects(
        self,
        query: str
    ) -> List[Dict[str, Any]]:

        data = self._load()

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

                obj_copy = dict(
                    obj
                )

                obj_copy[
                    "relevance_score"
                ] = score


                scored.append(
                    obj_copy
                )


        if not scored:

            scored = data


        normalized = []


        for item in scored:

            normalized.append(
                self.normalizer.normalize(
                    item
                )
            )


        return sorted(
            normalized,
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
        ):

            if "da nang" in text:

                score += 5


        return score
