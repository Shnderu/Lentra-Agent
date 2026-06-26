from lentralication.search.pipeline import execute_search
from lentra.api.schemas.search_request import SearchRequest
from lentra.api.schemas.search_response import SearchResponse, PropertyResponse


def search_endpoint(payload: dict, state=None):
    req = SearchRequest(**payload)

    result = execute_search({
        "payload": {
            "text": req.query,
            "city": req.city,
            "budget_min": req.budget_min,
            "budget_max": req.budget_max,
            "location": {
                "lat": req.lat,
                "lng": req.lng
            } if req.lat and req.lng else None
        }
    }, state=state)

    mapped = [
        PropertyResponse(
            id=r["id"],
            title=r["title"],
            price=r["price"],
            city=r["city"],
            rank_score=r.get("rank_score", 0.0)
        )
        for r in result["results"]
    ]

    return SearchResponse(
        results=mapped,
        meta=result.get("meta", {})
    ).dict()
