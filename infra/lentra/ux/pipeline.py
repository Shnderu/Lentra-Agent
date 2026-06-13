from lentra.market.ranker import rank_properties
from lentra.ux.formatter import format_property_response

def build_user_response(items: list):
    ranked = rank_properties(items)
    return format_property_response(ranked)
