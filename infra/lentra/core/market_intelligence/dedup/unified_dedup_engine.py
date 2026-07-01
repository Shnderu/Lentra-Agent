from typing import Dict, Any, List
import hashlib


class UnifiedDedupEngine:

    def __init__(self):
        self._clusters = {}

    def analyze(self, item: Dict[str, Any]) -> Dict[str, Any]:
        sig = self._build_signature(item)

        cluster_size = len(self._clusters.get(sig, [])) + 1

        return {
            **item,
            "dedup_signature": sig,
            "is_duplicate": cluster_size > 1,
            "cluster_size": cluster_size,
        }

    def evaluate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Unified Gateway contract.
        """

        result = self.analyze(payload)

        return {
            "duplicates": max(result.get("cluster_size", 1) - 1, 0),
            "signature": result.get("dedup_signature"),
            **result,
        }

    def deduplicate(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        STEP 3C FINAL: deterministic snapshot clustering
        """

        clusters: Dict[str, List[Dict[str, Any]]] = {}

        for item in items:
            sig = self._build_signature(item)
            clusters.setdefault(sig, []).append(item)

        enriched = []
        duplicate_count = 0

        for sig, group in clusters.items():

            is_dup = len(group) > 1

            if is_dup:
                duplicate_count += len(group) - 1

            for item in group:
                enriched.append({
                    **item,
                    "dedup_signature": sig,
                    "is_duplicate": is_dup,
                    "cluster_size": len(group)
                })

        return {
            "duplicates": duplicate_count,
            "items": enriched
        }

    def _build_signature(self, item: Dict[str, Any]) -> str:
        raw = f"{item.get('id','')}::{item.get('price','')}"
        return hashlib.md5(raw.encode()).hexdigest()
