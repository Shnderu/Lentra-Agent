from typing import Dict, Any, List


def score_risk_v2(property_data: Dict[str, Any], market_context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    V2 Risk Engine (MVP+):
    - расширенные флаги
    - учет отклонения от рынка
    - базовая анти-скам логика под SEA рынок
    """

    risk_score = 0
    flags: List[str] = []

    price = property_data.get("price")
    description = property_data.get("description", "")
    location = property_data.get("location", "")

    # --- базовые сигналы ---
    if price is None:
        risk_score += 50
        flags.append("no_price")

    if not description:
        risk_score += 10
        flags.append("no_description")

    # --- SEA scam heuristics ---
    if isinstance(description, str):
        desc_low = description.lower()

        if any(x in desc_low for x in ["urgent", "today only", "last unit"]):
            risk_score += 15
            flags.append("pressure_selling")

        if any(x in desc_low for x in ["whatsapp only", "telegram only"]):
            risk_score += 10
            flags.append("off_platform_contact")

    # --- price anomaly ---
    market_price = None
    deviation = None

    if market_context:
        market_price = market_context.get("market_price")
        deviation = market_context.get("deviation")

        if deviation is not None:
            if deviation < -30:
                risk_score += 25
                flags.append("too_cheap_vs_market")

            if deviation > 80:
                risk_score += 20
                flags.append("overpriced_anomaly")

    # --- location weak signal ---
    if not location:
        risk_score += 5
        flags.append("no_location")

    # clamp
    if risk_score > 100:
        risk_score = 100

    level = (
        "low" if risk_score < 30 else
        "medium" if risk_score < 70 else
        "high"
    )

    return {
        "risk_score": risk_score,
        "level": level,
        "flags": flags,
        "market_context": {
            "market_price": market_price,
            "deviation": deviation
        },
        "engine": "v2"
    }
