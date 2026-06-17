from lentra.domain.search.engine import search_engine
from lentra.domain.ranking.engine import rank_engine
from lentra.domain.aggregation.engine import aggregate_engine
from lentra.core.contracts.dto import RequestDTO, ResponseDTO


def handle_request(payload: dict):

    req = RequestDTO(
        query=payload.get("query"),
        user_id=payload.get("user_id"),
        context=payload
    )

    raw = search_engine.search(req.query)
    ranked = rank_engine.rank(raw)
    result = aggregate_engine.aggregate(ranked)

    return ResponseDTO(
        query=req.query,
        results=result,
        meta={"user_id": req.user_id}
    ).__dict__
