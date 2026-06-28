

def build_listing_response(insight, rank, area_score, explanation) -> dict:

    return {
        "id": insight.id,
        "cluster_id": insight.cluster_id,

        "price": {
            "value": insight.price,
            "market_avg": insight.market_avg,
            "deviation": insight.deviation
        },

        "signals": {
            "signal": insight.signal,
            "risk": insight.risk
        },

        "ranking": {
            "percentile": rank["percentile"],
            "rank": rank["rank"],
            "cluster_size": rank.get("cluster_size", 1)
        },

        "area": {
            "score": area_score
        },

        "verdict": insight.verdict,

        "explanation": explanation,

        "status": "indexed"
    }
