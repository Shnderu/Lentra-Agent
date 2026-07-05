from typing import Dict, Any


class ResponseBuilder:

    @staticmethod
    def build(result: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "ok",
            "engine_keys": [
                "signals",
                "risk",
                "ranking",
                "enrichment"
            ],
            "pricing": result.get("pricing"),
            "area": result.get("area"),
            "dedup": result.get("dedup"),
            "coupling": result.get("coupling"),
            "risk": result.get("risk"),
            "ranking": result.get("ranking"),
            "enrichment": result.get("enrichment"),
        }
