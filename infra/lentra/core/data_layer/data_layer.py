class DataLayer:
    def __init__(self):
        # TEMP SEED DATA (CRITICAL FOR DEV)
        self._mock_db = [
            {
                "id": "task",
                "title": "studio beach wifi",
                "meta": {
                    "price": 700,
                    "area": "beach",
                    "wifi": True
                }
            },
            {
                "id": "task",
                "title": "studio city center wifi",
                "meta": {
                    "price": 500,
                    "area": "city",
                    "wifi": True
                }
            },
            {
                "id": "task",
                "title": "villa beach luxury wifi",
                "meta": {
                    "price": 1500,
                    "area": "beach",
                    "wifi": True
                }
            }
        ]

    def _tokens(self, text: str):
        return text.lower().split()

    def fetch(self, query: str):
        q_tokens = self._tokens(query)
        results = []

        for obj in self._mock_db:
            title_tokens = self._tokens(obj["title"])

            match_score = 0
            for t in q_tokens:
                if t in title_tokens:
                    match_score += 1

            if match_score >= max(1, len(q_tokens) - 1):
                results.append(obj)

        return results
