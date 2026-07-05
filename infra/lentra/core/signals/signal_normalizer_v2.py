class SignalNormalizerV2:
    """
    PHASE 1:
    Centralized normalization of all signals
    """

    def normalize(self, payload: dict) -> dict:
        query = payload.get("query", "")
        price = float(payload.get("price") or 0)
        market_price = float(payload.get("market_price") or 1)

        # pricing signals
        deviation = abs(price - market_price) / max(market_price, 1)
        direction = "over" if price > market_price else "under"

        pricing = {
            "score": 1.0 - min(deviation, 1.0),
            "direction": direction,
            "deviation": round(deviation, 4),
            "confidence": 0.95,
        }

        # geo placeholder (will be replaced by AreaEngine in PHASE 3)
        geo = {
            "score": 0.5,
            "city": self._extract_city(query),
            "country": "Vietnam",
            "weights": {
                "expat_density": 0.5,
                "tourism": 0.5,
                "cost_index": 0.5,
            },
            "version": "geo_v2_stub",
        }

        return {
            "query": query,
            "price": price,
            "market_price": market_price,
            "signals": {
                "pricing": pricing,
                "geo": geo,
            },
            "_normalized": True,
        }

    def _extract_city(self, query: str) -> str:
        q = query.lower()

        if "da nang" in q:
            return "da_nang"
        if "nha trang" in q:
            return "nha_trang"
        if "hanoi" in q:
            return "hanoi"
        if "hcm" in q or "saigon" in q or "ho chi minh" in q:
            return "ho_chi_minh"
        if "hoi an" in q:
            return "hoi_an"
        if "dalat" in q:
            return "da_lat"

        return "unknown"
