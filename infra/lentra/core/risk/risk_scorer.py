from typing import Dict, Any


def score_risk(property_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    MVP risk engine (heuristic scoring)

    Сигналы:
    - нет цены → высокий риск
    - подозрительно низкая цена → риск
    - нет описания → средний риск
    """

    risk_score = 0
    flags = []

    price = property_data.get("price")
    description = property_data.get("description", "")

    if price is None:
        risk_score += 50
        flags.append("no_price")

    if price is not None and price < 200:
        risk_score += 20
        flags.append("suspicious_low_price")

    if not description:
        risk_score += 10
        flags.append("no_description")

    if risk_score > 100:
        risk_score = 100

    return {
        "risk_score": risk_score,
        "flags": flags,
        "level": (
            "low" if risk_score < 30 else
            "medium" if risk_score < 70 else
            "high"
        )
    }
