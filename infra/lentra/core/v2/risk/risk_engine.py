from typing import Dict, Any


class RiskEngineV2:
    """
    MVP v2 Risk Engine
    Расширенный риск-скоринг (пока baseline + hooks под расширение)
    """

    def score(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        score = 0
        flags = []

        price = listing.get("price")
        description = listing.get("description", "")

        if price is None:
            score += 50
            flags.append("no_price")

        if price is not None and price < 200:
            score += 25
            flags.append("suspicious_low_price")

        if not description:
            score += 10
            flags.append("no_description")

        # v2 расширение: наличие дублей снижает риск
        if listing.get("duplicates"):
            score -= 10
            flags.append("has_duplicates_signal")

        score = max(0, min(100, score))

        return {
            "risk_score": score,
            "flags": flags,
            "level": (
                "low" if score < 30 else
                "medium" if score < 70 else
                "high"
            )
        }


def score_risk_v2(listing: Dict[str, Any]) -> Dict[str, Any]:
    engine = RiskEngineV2()
    return engine.score(listing)
