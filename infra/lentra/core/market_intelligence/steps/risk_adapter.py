class RiskEngine:
    """
    CONTRACT FIX: compatibility layer

    Поддерживает старый и новый интерфейс:
    - analyze(item)
    - score(item)
    - __call__(item)
    """

    def analyze(self, item: dict) -> dict:
        return self._score(item)

    def score(self, item: dict) -> dict:
        return self._score(item)

    def __call__(self, item: dict) -> dict:
        return self._score(item)

    def _score(self, item: dict) -> dict:
        price = item.get("price", 0)

        if price < 800:
            risk_score = 0.2
        elif price < 1500:
            risk_score = 0.5
        else:
            risk_score = 0.8

        item["risk"] = {
            "score": risk_score,
            "label": "low" if risk_score < 0.3 else "medium" if risk_score < 0.7 else "high"
        }

        return item
