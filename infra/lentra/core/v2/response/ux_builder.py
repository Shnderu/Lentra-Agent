from typing import Dict, Any, List


class UXBuilderV2:

    def build_card(self, listing: Dict[str, Any], market: Dict[str, Any]) -> Dict[str, Any]:
        """
        UX-ready объект для UI / Telegram / web
        """

        ai = listing.get("ai_score_v2", {})
        risk = listing.get("risk_v2", {})
        area = listing.get("area_v2", {})

        return {
            "id": listing.get("id"),
            "title": listing.get("title"),
            "price": listing.get("price"),
            "currency": listing.get("currency"),
            "location": listing.get("location"),

            "market_price": market.get("market_price"),
            "price_deviation": self._deviation(listing, market),

            "risk_score": listing.get("risk_score"),
            "risk_level": risk.get("level"),

            "area_score": area.get("area_score"),

            "ai_score": ai.get("score"),
            "verdict": ai.get("verdict"),

            "insights": self._insights(listing, market, ai, risk, area)
        }

    def _deviation(self, listing: Dict[str, Any], market: Dict[str, Any]):
        price = listing.get("price")
        market_price = market.get("market_price")

        if not price or not market_price:
            return None

        return round(((price - market_price) / market_price) * 100, 2)

    def _insights(self, listing, market, ai, risk, area) -> List[str]:
        insights = []

        if ai.get("verdict") == "excellent_deal":
            insights.append("Цена ниже рыночной при нормальном риске")

        if risk.get("risk_score", 0) > 60:
            insights.append("Повышенный риск объявления")

        if area.get("area_score", 0) >= 8:
            insights.append("Сильная локация для экспатов")

        if listing.get("price") and market.get("market_price"):
            if listing["price"] > market["market_price"]:
                insights.append("Цена выше среднего по рынку")

        return insights
