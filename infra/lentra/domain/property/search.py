from lentra.data.adapter import get_properties
from lentra.domain.ranking.engine import rank


def search_properties(payload, state=None):

    conn = state.get("db_conn")

    props = get_properties(payload, conn=conn)

    ranked = rank(props, state)

    return ranked
