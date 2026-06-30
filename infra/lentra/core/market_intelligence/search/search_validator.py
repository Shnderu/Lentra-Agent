from typing import List, Dict, Any
from lentra.core.market_intelligence.contracts.search_contract import SearchListing


class SearchValidator:

    def validate_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(payload.get("listings"), list):
            raise ValueError("listings must be a list")

        if not payload.get("query_text"):
            payload["query_text"] = ""

        cleaned = []
        for item in payload["listings"]:
            if not isinstance(item, dict):
                continue

            cleaned.append({
                "price": item.get("price", 0),
                "title": item.get("title", ""),
                "city": item.get("city"),
                "location": item.get("location"),
            })

        payload["listings"] = cleaned
        return payload

    def validate_response(self, result: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []

        for item in result:
            if not isinstance(item, dict):
                continue

            normalized.append({
                "price": item.get("price", 0),
                "title": item.get("title", ""),
                "event_emitted": bool(item.get("event_emitted", False))
            })

        return normalized
