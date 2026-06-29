class RiskEngine:

    def analyze(self, payload: dict):
        return {
            "risk_score": 0.5,
            "flags": ["stub-risk-engine"],
            "status": "ok"
        }
