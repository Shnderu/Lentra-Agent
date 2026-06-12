"""
Lentra Incident Similarity Engine v8
Lightweight heuristic matcher
"""


class IncidentSimilarity:

    def score(self, a: dict, b: dict):
        score = 0

        if a.get("severity") == b.get("severity"):
            score += 40

        if abs(a.get("graph_size", 0) - b.get("graph_size", 0)) < 3:
            score += 30

        if abs(a.get("edges", 0) - b.get("edges", 0)) < 3:
            score += 30

        return {
            "score": score,
            "match": score >= 70
        }


if __name__ == "__main__":
    sim = IncidentSimilarity()

    print(sim.score(
        {"severity": "LOW", "graph_size": 5, "edges": 4},
        {"severity": "LOW", "graph_size": 6, "edges": 5}
    ))
