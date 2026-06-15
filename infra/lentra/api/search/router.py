from lentra.application.search.search_service import SearchService
from lentra.api.schemas.search_request import SearchRequest
from lentra.api.schemas.search_response import SearchResponse, PropertyResponse


service = SearchService()


def search_endpoint(payload: dict, state=None):
    req = SearchRequest(**payload)

    results = service.search(req, state)

    mapped = [
        PropertyResponse(
            id=r["id"],
            title=r["title"],
            price=r["price"],
            city=r["city"],
            rank_score=r.get("rank_score", 0.0)
        )
        for r in results
    ]

    return SearchResponse(results=mapped, meta={
        "count": len(mapped)
    }).dict()
