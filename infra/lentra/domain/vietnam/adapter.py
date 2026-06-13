from lentra.domain.property.search import search_properties
from lentra.domain.ranking.rank import rank_properties


def get_vietnam_properties(payload, state=None):
    props = search_properties(payload, state)
    ranked = rank_properties(props, state)

    return ranked
