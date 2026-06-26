from typing import List, Dict, Any


class RankerV2:
    """
    Market-aware ranking engine

    Скоринг:
    - deviation от рынка (чем ближе к 0 → лучше)
    - risk_score (чем ниже → лучше)
    - бонус за низкую цену относительно рынка
    """

    def _get_market_price(self, market: Dict[str, Any]) -> float:
        if not market:
            return 0.0
        return market.get("market_price") or 0.0

    def _score(self, item: Dict[str, Any], market_price: float) -> float:
        price = item.get("price") or 0
        risk = item.get("risk_score") or 0

        if market_price <= 0:
            return price

        deviation = abs(price - market_price) / market_price * 100

        # lower is better
        score = 0
        score += deviation * 0.6
        score += risk * 0.4

        return score

    def rank(self, listings: List[Dict[str, Any]], market: Dict[str, Any]) -> List[Dict[str, Any]]:
        market_price = self._get_market_price(market)

        for item in listings:
            item["ranking_score"] = self._score(item, market_price)

        return sorted(listings, key=lambda x: x.get("ranking_score", 9999))


def rank_listings_v2(listings: List[Dict[str, Any]], market: Dict[str, Any]) -> List[Dict[str, Any]]:
    engine = RankerV2()
    return engine.rank(listings, market)
