"""
Lentra Predictive Engine v9
Risk Scoring + Early Failure Prediction
"""

class RiskEngine:

    def compute_risk(self, incident: dict):
        score = 0

        # severity impact
        severity = incident.get("severity", "NONE")

        if severity == "LOW":
            score += 20
        elif severity == "MEDIUM":
            score += 50
        elif severity == "HIGH":
            score += 80

        # graph complexity
        graph_size = incident.get("graph_size", 0)
        edges = incident.get("edges", 0)

        if graph_size > 10:
            score += 20
        if edges > graph_size:
            score += 10

        # recurrence signal
        if incident.get("is_recurrent", False):
            score += 25

        return {
            "risk_score": min(score, 100),
            "level": self._level(score)
        }

    def _level(self, score):
        if score < 30:
            return "SAFE"
        elif score < 60:
            return "WATCH"
        elif score < 80:
            return "WARNING"
        return "CRITICAL"


if __name__ == "__main__":
    engine = RiskEngine()

    print(engine.compute_risk({
        "severity": "MEDIUM",
        "graph_size": 12,
        "edges": 15,
        "is_recurrent": True
    }))
