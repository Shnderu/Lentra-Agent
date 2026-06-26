from typing import Dict, Any, List


def estimate_market_price(property_data: Dict[str, Any], market_samples: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    MVP pricing engine:
    - считает среднюю цену по выборке
    - определяет отклонение объекта от рынка
    """

    if not market_samples:
        return {
            "market_price": None,
            "deviation": None,
            "note": "no market data"
        }

    prices = [x.get("price") for x in market_samples if x.get("price")]

    if not prices:
        return {
            "market_price": None,
            "deviation": None,
            "note": "empty market sample"
        }

    market_price = sum(prices) / len(prices)

    current_price = property_data.get("price")

    if not current_price:
        return {
            "market_price": market_price,
            "deviation": None,
            "note": "no property price"
        }

    deviation = ((current_price - market_price) / market_price) * 100

    return {
        "market_price": round(market_price, 2),
        "deviation": round(deviation, 2),
        "raw_price": current_price
    }
