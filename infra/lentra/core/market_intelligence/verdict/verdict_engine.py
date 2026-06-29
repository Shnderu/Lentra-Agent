class VerdictEngine:

    def run(self, obj: dict):

        market_verdict = obj.get("market_verdict")

        score = obj.get("score") or 0
        risk = obj.get("risk") or 0
        confidence = obj.get("market_confidence") or obj.get("confidence") or 0.5

        # -------------------------
        # PRIMARY DECISION IS MARKET-DRIVEN
        # -------------------------
        if market_verdict == "overpriced":
            verdict = "overpriced"
        elif market_verdict == "cheap":
            verdict = "good_deal"
        else:
            verdict = "fair"

        # -------------------------
        # RISK OVERRIDE
        # -------------------------
        if risk > 0.85:
            verdict = "avoid"

        # -------------------------
        # FINAL CONFIDENCE MIX
        # -------------------------
        final_confidence = (confidence * 0.7) + ((1 - risk) * 0.3)

        obj["verdict"] = verdict
        obj["confidence"] = float(final_confidence)

        return obj
