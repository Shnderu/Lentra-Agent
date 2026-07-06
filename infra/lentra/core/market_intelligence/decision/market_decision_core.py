"""
CORE DECISION ENGINE (PURE)

RULE:
- no runtime imports
- no interpret()
- returns raw decision signals only
"""

def market_decision_core(data: dict) -> dict:

    risk = data.get("risk", 0)
    price = data.get("price", 0)

    score = (1 - risk) * 0.7 + (price / 1000) * 0.3

    return {
        "score": score,
        "raw_signal": "OK" if score > 0.5 else "LOW"
    }
