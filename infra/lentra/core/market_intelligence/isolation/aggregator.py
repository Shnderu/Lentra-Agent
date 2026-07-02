from typing import Dict, Any


class SafeMergeAggregator:
    """
    Combines isolated engine outputs into stable response
    """

    def merge(self, engine_results: Dict[str, Any]) -> Dict[str, Any]:
        score = 0.0
        delta = 0.0

        meta = {
            "engines": [],
            "failed": []
        }

        for name, result in engine_results.items():
            if result["status"] == "ok":
                meta["engines"].append(name)

                data = result.get("data", {})

                if isinstance(data, dict):
                    score += float(data.get("score", 0))
                    delta += float(data.get("delta", 0))

            else:
                meta["failed"].append({
                    "engine": name,
                    "error": result.get("error")
                })

        return {
            "score": score,
            "delta": delta,
            "status": "ok" if not meta["failed"] else "degraded",
            "_meta": meta
        }
