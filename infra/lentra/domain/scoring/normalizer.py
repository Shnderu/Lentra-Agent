def normalize_price(price: float, max_price: float = 50.0) -> float:
    if not price:
        return 0.0
    return max(0.0, 1.0 - (price / max_price))


def clamp(value: float) -> float:
    return max(0.0, min(1.0, value))
