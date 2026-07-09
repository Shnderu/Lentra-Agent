from typing import Dict, Any


class MarketModule:
    """
    LEGACY COMPATIBILITY WRAPPER.

    Старый MarketModule больше не содержит
    собственную бизнес-логику.

    Источник истины:
        SearchPipeline
        Market Intelligence Layer

    Этот класс оставлен временно,
    чтобы не ломать старые импорты.
    """

    def run(
        self,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:

        query = ""

        if isinstance(payload, dict):
            query = (
                payload.get("query")
                or payload.get("title")
                or ""
            )

        return {
            "query": query,

            "snapshot": {
                "objects": []
            },

            "deprecated": True,

            "message":
                "Use CanonicalSearchPipeline instead of MarketModule."
        }
