

def generate_explanation(insight, rank, area_score) -> dict:

    price = insight.price
    market_avg = insight.market_avg
    deviation = insight.deviation

    # price explanation
    if deviation < -0.1:
        price_text = "Price is significantly below market"
        price_comment = "Potential high value opportunity"
    elif deviation > 0.15:
        price_text = "Price is above market average"
        price_comment = "Risk of overpaying"
    else:
        price_text = "Price is aligned with market"
        price_comment = "Fair market deal"

    # rank explanation
    if rank["percentile"] >= 0.7:
        rank_text = "Top tier listing in cluster"
    elif rank["percentile"] >= 0.4:
        rank_text = "Mid-range listing"
    else:
        rank_text = "Lower tier compared to alternatives"

    # area explanation
    if area_score > 7.5:
        area_text = "High quality expat area"
    elif area_score > 6:
        area_text = "Decent livability area"
    else:
        area_text = "Basic infrastructure area"

    # final verdict
    if insight.signal == "cheap" and area_score > 7:
        verdict = "Strong buy: good price + good location"
    elif insight.signal == "expensive":
        verdict = "Weak deal: overpriced relative to market"
    else:
        verdict = "Neutral: acceptable option"

    return {
        "price_analysis": price_text,
        "price_comment": price_comment,
        "rank_analysis": rank_text,
        "area_analysis": area_text,
        "verdict": verdict
    }
