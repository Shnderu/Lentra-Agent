from lentra.data.adapter import get_properties
from lentra.domain.ranking.engine import rank
from lentra.domain.search.query_parser import parse_query


def search_properties(payload, state=None):
    """
    SEARCH ENGINE v1 entrypoint
    """

    # 1. parse user query → filters
    query_text = None

    if payload:
        query_text = payload.get("text") or payload.get("query")

    filters = parse_query(query_text)

    # 2. fetch data
    props = get_properties(filters)

    # 3. ranking
    ranked = rank(props, state)

    return ranked
