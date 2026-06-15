from lentra.data.adapter import get_properties
from lentra.domain.ranking.engine import rank
from lentra.domain.search.query_parser import parse_query
from lentra.domain.search.diversify import diversify
from lentra.domain.search.feedback_cache import FeedbackCache

_feedback_cache = FeedbackCache()


def search_properties(payload, state=None):
    query_text = None
    user_location = None

    if payload:
        query_text = payload.get("text") or payload.get("query")
        user_location = payload.get("location")

    filters = parse_query(query_text)

    props = get_properties(filters)

    ranked = rank(
        props,
        state,
        query_text,
        user_location,
        _feedback_cache.get()
    )

    return diversify(ranked)
