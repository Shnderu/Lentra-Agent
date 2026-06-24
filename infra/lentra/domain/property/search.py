from lentra.data.adapter import get_properties
from lentra.domain.property.ranking import rank_property


def search_properties(payload: dict, conn):
    props = get_properties(payload, conn=conn)

    enriched = []

    for p in props:

        item = dict(p)

        item["rank_score"] = rank_property(
            item,
            payload
        )

        enriched.append(item)

    enriched.sort(
        key=lambda x: x["rank_score"],
        reverse=True
    )

    return enriched
