def resolve_verdict(deviation: float, risk_level: str) -> str:

    if risk_level == "high":
        return "avoid"

    if deviation < -5:
        return "strong_buy"

    if deviation < 0:
        return "buy"

    if deviation < 5:
        return "hold"

    return "sell"
