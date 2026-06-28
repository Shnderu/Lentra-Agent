

def build_response(query, plan, results):

    return {
        "query": query,
        "plan": plan,
        "results": [
            {
                "id": r["listing"]["id"],
                "price": r["listing"]["price"],
                "cluster_id": r["listing"].get("cluster_id"),
                "area_score": r["listing"].get("area", {}).get("score"),
                "risk": r["listing"].get("signals", {}).get("risk"),
                "signal": r["listing"].get("signals", {}).get("signal"),
                "rank": r["listing"].get("ranking", {}).get("rank"),
                "verdict": r["listing"].get("verdict"),
                "reason": r.get("reason"),
            }
            for r in results
        ],
        "meta": {
            "count": len(results)
        }
    }
