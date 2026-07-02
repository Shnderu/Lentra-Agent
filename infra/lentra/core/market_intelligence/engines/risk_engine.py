class RiskEngine:
    def evaluate(self, ctx):
        payload = ctx.payload

        return {
            "delta": 0.111,
            "level": "low"
        }
