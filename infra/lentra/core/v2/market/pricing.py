from typing import Dict, Any, List


def estimate_market_price_v2(property_data: Dict[str, Any], market_samples: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    V2 Market Engine:
    - более строгая нормализация цены
    - задел под geo/seasonality/segmenting
    """

    if not market_samples:
        return {
            "market_price": None,
            "deviation": None,
            "note": "no market data"
        }

    prices = [
        float(x.get("price", 0))
        for x in market_samples
        if x.get("price") is not None
    ]

    if not prices:
        return {
            "market_price": None,
            "deviation": None,
            "note": "empty market sample"
        }

    market_price = sum(prices) / len(prices)

    current_price = property_data.get("price")

    if current_price is None:
        return {
            "market_price": market_price,
            "deviation": None,
            "note": "no property price"
        }

    try:
        current_price = float(current_price)
    except Exception:
        return {
            "market_price": market_price,
            "deviation": None,
            "note": "invalid property price"
        }

    deviation = ((current_price - market_price) / market_price) * 100

    return {
        "market_price": round(market_price, 2),
        "deviation": round(deviation, 2),
        "raw_price": current_price,
        "engine": "v2"
    }
