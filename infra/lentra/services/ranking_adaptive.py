from lentra.services.feature_store import get_user_affinity
from lentra.services.ranking_service import compute_score


def rank(properties, user_id=None):
    affinity = get_user_affinity(user_id) if user_id else {}

    results = []

    for p in properties:
        base_score = compute_score(p, user={"prefers_sea_view": True} if user_id else None)

        boost = affinity.get(p.id, 0) * 2.5  # learning weight

        final_score = base_score + boost

        results.append({
            "id": p.id,
            "title": p.title,
            "score": final_score
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)
