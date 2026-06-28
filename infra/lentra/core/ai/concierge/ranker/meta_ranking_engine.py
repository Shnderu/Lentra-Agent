

def compute_meta_score(
    price_signal,
    risk,
    scam,
    area,
    feedback_bias=0.0
):

    # PRICE SCORE
    if price_signal.get("signal") == "cheap":
        price_score = 1.0
    elif price_signal.get("signal") == "neutral":
        price_score = 0.6
    else:
        price_score = 0.3

    # AREA SCORE
    area_score = (area.get("area_score", 5) / 10)

    # RISK SCORE (inverse)
    risk_score = 1.0 - risk.get("risk_score", 0.5)

    # SCAM SCORE (inverse)
    scam_score = 1.0 - scam.get("scam_score", 0.5)

    # FEEDBACK SCORE
    feedback_score = max(0.0, min(1.0, feedback_bias))

    # FINAL SCORE
    final = (
        price_score * 0.30 +
        area_score * 0.30 +
        risk_score * 0.15 +
        scam_score * 0.15 +
        feedback_score * 0.10
    )

    final = max(0.0, min(1.0, final))

    # LABELING
    reasons = []

    if price_score > 0.8:
        reasons.append("good price vs market")

    if area_score > 0.7:
        reasons.append("strong area quality")

    if risk_score < 0.4:
        reasons.append("moderate risk detected")

    if scam_score < 0.4:
        reasons.append("possible scam signals")

    if feedback_score > 0.5:
        reasons.append("user preference boost")

    if final >= 0.75:
        label = "top_pick"
    elif final >= 0.5:
        label = "acceptable"
    else:
        label = "weak_match"

    return {
        "final_score": round(final, 3),
        "label": label,
        "reasons": reasons
    }
