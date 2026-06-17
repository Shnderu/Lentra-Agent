from lentra.domain.search.engine import search_engine
from lentra.domain.ranking.engine import rank_engine
from lentra.domain.aggregation.engine import aggregate_engine


def handle_request(payload: dict):

    query = payload.get("query")

    raw = search_engine.search(query)
    ranked = rank_engine.rank(raw)
    result = aggregate_engine.aggregate(ranked)

    return {
        "query": query,
        "results": result
    }
