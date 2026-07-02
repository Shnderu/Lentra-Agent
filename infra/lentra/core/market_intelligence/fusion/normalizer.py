class FusionNormalizer:

    def normalize(self, pricing: dict, risk: dict, dedup: dict, expat: dict):
        """
        SINGLE SOURCE OF TRUTH NORMALIZATION

        RULES:
        - never recompute logic here
        - only align scales
        - output deterministic fusion vector
        """

        price_score = pricing.get("score", 0)
        risk_score = 1 - risk.get("risk_level", 0)
        dedup_score = 1 / (1 + dedup.get("matches", 1))
        expat_score = expat.get("expat_score", 0)

        fusion_vector = {
            "price": price_score,
            "risk": risk_score,
            "dedup": dedup_score,
            "expat": expat_score
        }

        # deterministic aggregation only
        signal_score = (
            0.4 * price_score +
            0.3 * risk_score +
            0.2 * dedup_score +
            0.1 * expat_score
        )

        return {
            "vector": fusion_vector,
            "signal": float(signal_score)
        }
