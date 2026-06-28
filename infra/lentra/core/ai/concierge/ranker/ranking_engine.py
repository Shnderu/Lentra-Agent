

def compute_final_score(price_signal, risk, area, feedback_bias=0.0):

    if price_signal.get("signal") == "cheap":
        price_score = 1.0
    elif price_signal.get("signal") == "neutral":
        price_score = 0.6
    else:
        price_score = 0.3

    area_score = (area.get("area_score", 5) / 10)
    risk_score = 1.0 - risk.get("risk_score", 0.5)

    base = (
        price_score * 0.4 +
        area_score * 0.4 +
        risk_score * 0.2
    )

    final = base + (feedback_bias * 0.1)

    final = max(0.0, min(1.0, final))

    if final >= 0.75:
        label = "strong_recommendation"
    elif final >= 0.5:
        label = "acceptable"
    else:
        label = "weak_match"

    return {
        "final_score": round(final, 3),
        "label": label
    }
