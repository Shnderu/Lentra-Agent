from typing import Dict, Any, List


class DedupEngine:
    def cluster(self, property_obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        v0.1 heuristic dedup:
        later will be replaced with embeddings + image hash + text similarity
        """

        raw = property_obj.get("raw_query", "").lower()
        location = property_obj.get("location")

        cluster_key = []

        if location:
            cluster_key.append(location)

        if "studio" in raw:
            cluster_key.append("studio")

        if "beach" in raw:
            cluster_key.append("beach_zone")

        cluster_id = "_".join(cluster_key) if cluster_key else "unknown"

        return {
            "cluster_id": cluster_id,
            "confidence": 0.6,
            "method": "heuristic_v1"
        }


dedup_engine = DedupEngine()
