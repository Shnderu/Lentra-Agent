from core.memory.incident_memory_v8 import IncidentMemory
from core.memory.incident_similarity_v8 import IncidentSimilarity

"""
Lentra Incident Memory Fusion v8
Historical Pattern Intelligence Layer
"""


class IncidentMemoryFusion:

    def run(self, incident: dict):
        memory = IncidentMemory()
        similarity = IncidentSimilarity()

        stored = memory.store(incident)
        similar = memory.search_similar(incident)

        matches = similar.get("matches", [])

        best_score = 0
        for m in matches:
            score = similarity.score(incident, m).get("score", 0)
            best_score = max(best_score, score)

        return {
            "stored": stored,
            "similar_incidents": len(matches),
            "best_similarity_score": best_score,
            "is_recurrent": best_score >= 70
        }


if __name__ == "__main__":
    fusion = IncidentMemoryFusion()

    test = {
        "severity": "LOW",
        "graph_size": 5,
        "edges": 4
    }

    print(fusion.run(test))
