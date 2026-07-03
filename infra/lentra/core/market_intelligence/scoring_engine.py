from dataclasses import dataclass


def clamp(v: float, min_v: float = 0.0, max_v: float = 1.0) -> float:
    return max(min_v, min(max_v, v))


@dataclass
class MarketInput:
    price: float
    market_price: float
    freshness: float = 0.5
    duplication_anomaly: float = 0.0
    price_anomaly: float = 0.0
    internet: float = 0.5
    safety: float = 0.5
    infrastructure: float = 0.5
    expat_density: float = 0.5
    dedup_type: str = "none"  # exact / probable / weak / none
    has_photos: bool = False
    has_exact_location: bool = False
    has_price_history: bool = False
    has_reposts: bool = False


class MarketScoringEngine:

    def price_score(self, price: float, market_price: float) -> float:
        if market_price <= 0:
            return 0.5

        deviation = (price - market_price) / market_price
        score = 1.0 - deviation
        return clamp(score)

    def risk_score(self, inp: MarketInput) -> float:
        return clamp(
            0.4 * inp.freshness +
            0.3 * inp.duplication_anomaly +
            0.3 * inp.price_anomaly
        )

    def area_score(self, inp: MarketInput) -> float:
        return clamp(
            (inp.internet +
             inp.safety +
             inp.infrastructure +
             inp.expat_density) / 4.0
        )

    def dedup_score(self, dedup_type: str) -> float:
        if dedup_type == "exact":
            return 1.0
        if dedup_type == "probable":
            return 0.7
        if dedup_type == "weak":
            return 0.3
        return 0.0

    def signals_score(self, inp: MarketInput) -> float:
        signals = [
            inp.has_photos,
            inp.has_exact_location,
            inp.has_price_history,
            inp.has_reposts
        ]
        return sum(1 for s in signals if s) / 4.0

    def decision(self, score: float) -> str:
        if score >= 0.75:
            return "GOOD"
        if score >= 0.5:
            return "REVIEW"
        return "BAD"

    def compute(self, inp: MarketInput, weights: dict = None):
        weights = weights or {
            "price": 0.3,
            "risk": 0.25,
            "signals": 0.2,
            "area": 0.15,
            "dedup": 0.1,
        }

        price = self.price_score(inp.price, inp.market_price)
        risk = self.risk_score(inp)
        signals = self.signals_score(inp)
        area = self.area_score(inp)
        dedup = self.dedup_score(inp.dedup_type)

        raw = (
            price * weights["price"] +
            risk * weights["risk"] +
            signals * weights["signals"] +
            area * weights["area"] +
            dedup * weights["dedup"]
        )

        return {
            "score": round(raw, 4),
            "raw_score": round(raw, 4),
            "decision": self.decision(raw),
            "features": {
                "price": price,
                "risk": risk,
                "signals": signals,
                "area": area,
                "dedup": dedup,
            },
            "weights": weights
        }
