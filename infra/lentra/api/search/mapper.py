from lentra.api.search.schema import SearchRequest


def map_payload(payload: dict) -> SearchRequest:
    if not payload:
        return SearchRequest()

    return SearchRequest(
        query=payload.get("text") or payload.get("query"),
        city=payload.get("city"),
        budget_min=payload.get("budget_min"),
        budget_max=payload.get("budget_max"),
        lat=payload.get("lat"),
        lng=payload.get("lng"),
    )
