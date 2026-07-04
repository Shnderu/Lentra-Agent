class MarketIntelligenceEngine:

    def __init__(self, config=None):
        self.config = config or {}

    def compute(self, payload: dict) -> dict:

        price = payload.get("price", 0)
        market = payload.get("market_price", 0)

        deviation = abs(price - market) / market if market else 0

        # -----------------------
        # CORE SIGNALS
        # -----------------------
        pricing_score = 1 - deviation

        area_score = 0.8

        dedup = {
            "score": 1.0,
            "confidence": 1.0
        }

        risk_level = min(1.0, deviation + 0.1)

        # -----------------------
        # COUPLING (bounded)
        # -----------------------
        entropy = deviation
        entropy_dampener = 1 - entropy

        coupling_raw = (
            (pricing_score * 0.55) +
            (area_score * 0.25) +
            (dedup["confidence"] * 0.20)
        )

        coupling_score = coupling_raw * entropy_dampener
        coupling_score = max(0.25, min(0.75, coupling_score))

        # -----------------------
        # RANKING
        # -----------------------
        ranking_score = pricing_score

        # -----------------------
        # DECISION LAYER (EMBEDDED)
        # -----------------------
        final_score = (
            ranking_score * 0.45 +
            coupling_score * 0.25 +
            (1 - risk_level) * 0.30
        )

        if final_score >= 0.75:
            decision = "BUY"
        elif final_score >= 0.55:
            decision = "HOLD"
        else:
            decision = "AVOID"

        confidence = min(pricing_score, 1 - risk_level)

        return {
            "dedup": dedup,
            "ranking": {
                "score": ranking_score,
                "version": "ranking_v3_norm_v0.9"
            },
            "risk": {
                "risk_level": risk_level
            },
            "signals": {
                "pricing": {
                    "score": pricing_score,
                    "direction": "over" if price > market else "under",
                    "deviation": round(deviation, 4),
                    "confidence": pricing_score
                },
                "area": {
                    "score": area_score,
                    "note": "vietnam_area_model",
                    "country": "Vietnam"
                },
                "dedup": dedup,
                "coupling": {
                    "score": coupling_score,
                    "factors": {
                        "price_market_gap": deviation,
                        "entropy": entropy,
                        "entropy_dampener": entropy_dampener
                    }
                }
            },
            "decision": {
                "decision": decision,
                "final_score": round(final_score, 4),
                "confidence": round(confidence, 4),
                "explanation": {
                    "ranking": ranking_score,
                    "coupling": coupling_score,
                    "risk": risk_level
                }
            },
            "features": {
                "raw_context": payload
            }
        }
