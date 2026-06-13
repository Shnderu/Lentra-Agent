class SearchResponseBuilder:

    @staticmethod
    def build(ranked):

        if not ranked:
            return {
                "best_choice": None,
                "alternatives": [],
                "confidence": 0
            }

        best = ranked[0]

        return {
            "best_choice": {
                "id": best["property"].id,
                "title": best["property"].title,
                "price": best["property"].price,
                "source": best["property"].source,
                "score": best["score"]
            },
            "alternatives": [
                {
                    "id": item["property"].id,
                    "title": item["property"].title,
                    "price": item["property"].price,
                    "source": item["property"].source,
                    "score": item["score"]
                }
                for item in ranked[1:]
            ],
            "confidence": best["score"]
        }
