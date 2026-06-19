from dataclasses import dataclass, field
from typing import Optional


# =========================
# QUERY MODEL (minimal contract)
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
# INTENT TYPES (DOMAIN FIXED SET)
# =========================

INTENTS = {
    "rent": "rent_search",
    "search": "rent_search",
    "compare": "city_compare",
    "alert": "alert",
    "expat": "expat",
}


# =========================
# INTENT RESOLVER
# =========================

def resolve_intent(text: str) -> str:
    """
    Deterministic routing layer.
    Никакого ML / событий / внешних зависимостей.
    """

    t = text.lower().strip()

    if t.startswith("/rent"):
        return "rent_search"

    if t.startswith("/compare"):
        return "city_compare"

    if t.startswith("/alert"):
        return "alert"

    if t.startswith("/expat"):
        return "expat"

    if t.startswith("/search"):
        return "rent_search"

    return "rent_search"  # default safe fallback


# =========================
# QUERY BUILDER
# =========================

def build_query(text: str, meta: dict | None = None) -> Query:
    meta = meta or {}

    return Query(
        text=text,
        intent=resolve_intent(text),
        meta=meta
    )
