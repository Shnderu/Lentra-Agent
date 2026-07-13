from typing import Dict, Any


class UnifiedDedupEngine:
    """
    ARCH V2: pure dedup engine (NO BUSINESS LOGIC)
    """

    def evaluate(self, payload: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        context = context or {}

        signature = self._signature(payload)
        matches = self._match_count(signature, context)

        return {
            "signature": signature,
            "matches": matches
        }

    def _signature(self, payload: Dict[str, Any]) -> str:
        query = payload.get("query", "")
        price = payload.get("price", 0)
        return f"{hash(query)}:{price}"

    def _match_count(self, signature: str, context: Dict[str, Any]) -> int:
        return 1
