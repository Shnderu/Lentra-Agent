# ============================================================
# PATCH V16.3 - QUALITY FILTER INTEGRATION
# ============================================================

from lentra.rent.quality.engine import QualityEngine

quality_engine = QualityEngine()


def apply_quality_filter(listings: list) -> list:
    filtered = []

    for l in listings:
        q = quality_engine.score(l)

        # фильтр мусора
        if q["trust_score"] < 40:
            continue

        l["trust_score"] = q["trust_score"]
        l["source_score"] = q["source_score"]

        filtered.append(l)

    return filtered


def run_search_pipeline_canonical(listings, query):
    from lentra.rent.search_pipeline import (
        apply_filters,
        deduplicate,
        rank,
    )

    raw = [
        {
            "id": l.id,
            "title": l.title,
            "city": l.city,
            "price": l.price,
            "rooms": l.rooms,
            "source": l.source,
            "lat": l.lat,
            "lon": l.lon,
        }
        for l in listings
    ]

    filtered = apply_filters(raw, query)
    unique = deduplicate(filtered)

    # NEW QUALITY STEP
    quality_filtered = apply_quality_filter(unique)

    ranked = rank(quality_filtered, query)

    return ranked
