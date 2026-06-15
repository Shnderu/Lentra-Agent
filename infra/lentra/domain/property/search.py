from lentra.data.adapter import get_properties
from lentra.domain.ranking.engine import rank


def search_properties(payload, state=None):
    props = get_properties(payload)

    # feedback disabled (critical stability mode)
    ranked = rank(props, state=None)

    return ranked
