from lentra.domain.vietnam.adapter import get_vietnam_properties
from lentra.domain.v1.ranking import rank_properties
from lentra.domain.v1.ux_builder import build_property_list


def handle(payload, state):

    properties = get_vietnam_properties(payload, state)

    ranked = rank_properties(properties, payload)

    return build_property_list(ranked)
