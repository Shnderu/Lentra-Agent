from lentra.data.adapter import get_properties
from lentra.domain.property.ranking import rank_property


def search_properties(payload: dict, conn):
    props = get_properties(payload, conn=conn)

    enriched = []
    for p in props:
        p["rank_score"] = rank_property(p, payload)
        enriched.append(p)

    enriched.sort(key=lambda x: x["rank_score"], reverse=True)

    return enriched
