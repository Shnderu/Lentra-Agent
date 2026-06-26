class IntentClassifier:
    """
    CORE v1.1 — domain-free classifier

    ❌ НИКАКОЙ бизнес-логики (рейсы, билеты, деньги и т.д.)
    ✅ Только абстрактные категории
    """

    def classify(self, text: str):
        text = (text or "").lower()

        # универсальные классы системы
        if any(w in text for w in ["как", "почему", "зачем"]):
            return {
                "type": "question",
                "confidence": 0.6
            }

        if any(w in text for w in ["найди", "поиск", "покажи"]):
            return {
                "type": "search",
                "confidence": 0.7
            }

        if any(w in text for w in ["создай", "сделай", "построй"]):
            return {
                "type": "command",
                "confidence": 0.7
            }

        return {
            "type": "unknown",
            "confidence": 0.3
        }
