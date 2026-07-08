from typing import Dict, Any


class DedupIndex:

    """
    Dedup Intelligence Index.

    Stores listings and performs similarity matching.
    """


    def __init__(self):

        self.records = []


        from lentra.core.market_intelligence.dedup.similarity import DedupSimilarity

        self.similarity = DedupSimilarity()



    def register(
        self,
        listing: Dict[str, Any]
    ):

        self.records.append(
            listing.copy()
        )



    def find_matches(
        self,
        listing: Dict[str, Any]
    ):

        matches = []


        for item in self.records:

            if item.get("id") == listing.get("id"):
                continue


            score = self.similarity.compare(
                listing,
                item
            )


            if score >= 0.65:

                matches.append(
                    {
                        "listing": item,
                        "score": score
                    }
                )


        return matches



    def build_context(
        self,
        listing: Dict[str, Any]
    ):


        matches = self.find_matches(
            listing
        )


        sources = {
            item["listing"].get(
                "source",
                "unknown"
            )

            for item in matches
        }


        return {

            "duplicates": len(
                matches
            ),

            "confidence": round(
                min(
                    0.95,
                    0.65 +
                    (
                        len(matches)
                        * 0.1
                    )
                ),
                2
            )
            if matches else 0.0,

            "sources": list(
                sources
            ),

            "canonical_listing":
                matches[0]["listing"].get("id")
                if matches
                else listing.get("id"),

            "matches": [
                {
                    "id": x["listing"].get("id"),
                    "score": x["score"]
                }
                for x in matches
            ]

        }
