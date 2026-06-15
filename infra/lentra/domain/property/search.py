from lentra.data.adapter import get_properties
from lentra.domain.ranking.engine import rank
from lentra.domain.search.query_parser import parse_query


def search_properties(payload, state=None):
    """
    SEARCH ENGINE v2
    """

    query_text = None

    if payload:
        query_text = payload.get("text") or payload.get("query")

    filters = parse_query(query_text)

    props = get_properties(filters)

    ranked = rank(props, state, query_text)

    return ranked
