from typing import Dict, Any

class DedupLayer:
    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        payload = dict(payload)

        # only enrichment
        payload["dedup"] = {
            "status": "processed",
            "duplicates_found": payload.get("duplicates", 0)
        }

        return payload
