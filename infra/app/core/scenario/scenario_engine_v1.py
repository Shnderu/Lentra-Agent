from dataclasses import dataclass, field
from typing import Optional, Any


# =========================
# QUERY (reuse domain concept)
# =========================

@dataclass
class Query:
    text: str
    country: str = "Vietnam"
    intent: str = "unknown"
    budget: Optional[tuple[int, int]] = None
    location: Optional[str] = None
    meta: dict = field(default_factory=dict)


# =========================
# PIPELINE CONTRACT
# =========================

async def pipeline(query: Query):
    """
    Stub: должен быть подключен к domain_core_v1.execute_pipeline
    """
    raise NotImplementedError


# =========================
# SCENARIOS
# =========================

async def rent_search(query: Query, pipeline_fn):
    context = await pipeline_fn(query)

    return {
        "type": "rent_search",
        "results": context.ranked[:20],
        "insights": context.insights
    }


async def city_compare(query: Query, pipeline_fn, cities: list[str]):
    context = await pipeline_fn(query)

    grouped = {}
    for p in context.ranked:
        grouped.setdefault(p.city, []).append(p)

    return {
        "type": "city_compare",
        "cities": {c: grouped.get(c, []) for c in cities}
    }


async def alert(query: Query, pipeline_fn):
    context = await pipeline_fn(query)

    return {
        "type": "alert",
        "trigger_rules": {
            "budget_drop": True,
            "new_listings": True,
            "city": context.query.location
        }
    }


async def expat_filter(query: Query, pipeline_fn):
    context = await pipeline_fn(query)

    filtered = [
        p for p in context.ranked
        if p.attributes.get("expat_friendly", False)
    ]

    return {
        "type": "expat",
        "results": filtered
    }


# =========================
# ROUTER
# =========================

SCENARIOS = {
    "rent_search": rent_search,
    "city_compare": city_compare,
    "alert": alert,
    "expat": expat_filter,
}


async def run_scenario(intent: str, query: Query, pipeline_fn, **kwargs):
    handler = SCENARIOS.get(intent)

    if not handler:
        return {
            "type": "fallback",
            "message": "No scenario matched"
        }

    return await handler(query, pipeline_fn, **kwargs)
