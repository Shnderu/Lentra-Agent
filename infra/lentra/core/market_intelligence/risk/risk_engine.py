class RiskEngine:

    def __init__(self):
        pass

    def evaluate(self, item):
        item["risk_score"] = 0.5
        return item
