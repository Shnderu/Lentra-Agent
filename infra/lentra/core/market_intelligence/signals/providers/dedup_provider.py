from typing import Dict, Any


class DedupSignalProvider:
    name = "dedup"

    def compute(self, engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
        raw = engine_outputs.get("dedup", {})

        return {
            "score": float(raw.get("score", 0.0)),
            "confidence": float(raw.get("confidence", 1.0)),
            "meta": raw,
        }
