class IncidentSimilarity:

    def _int(self, v):
        try:
            return int(v)
        except:
            return 0

    def score(self, a: dict, b: dict):
        score = 0

        if a.get("severity") == b.get("severity"):
            score += 40

        if abs(self._int(a.get("graph_size")) - self._int(b.get("graph_size"))) < 3:
            score += 30

        if abs(self._int(a.get("edges")) - self._int(b.get("edges"))) < 3:
            score += 30

        return {
            "score": score,
            "match": score >= 70
        }
