"""
DOMAIN CORE v1 — Freeze Layer

Цель:
- фиксирует доменную модель аренды
- убирает зависимость от orchestrator/consumer/UI runtime
- задаёт единый pipeline обработки запроса
"""

from dataclasses import dataclass, field
from typing import Optional, Any


# =========================
# 1. QUERY MODEL (INTENT LAYER)
# =========================

@dataclass
class Query:
    text: str
    country: str = "Vietnam"
    intent: str = "unknown"  # rent_search | property_info | city_compare | alert | unknown
    budget: Optional[tuple[int, int]] = None
    location: Optional[str] = None
    meta: dict = field(default_factory=dict)


# =========================
# 2. PROPERTY ENTITY
# =========================

@dataclass
class Property:
    id: str
    title: str
    price: int
    currency: str
    city: str
    district: str
    source: str
    images: list[str] = field(default_factory=list)
    attributes: dict = field(default_factory=dict)


# =========================
# 3. SOURCE CONTRACT
# =========================

class ListingSource:
    """
    Adapter contract: каждый внешний источник = drop-in реализация
    """

    name: str = "base"

    async def fetch(self, query: Query) -> list[Property]:
        raise NotImplementedError


# =========================
# 4. RUNTIME CONTEXT
# =========================

@dataclass
class RentContext:
    query: Query
    properties: list[Property]
    ranked: list[Property]
    insights: dict = field(default_factory=dict)


# =========================
# 5. DOMAIN PIPELINE (CORE ENGINE)
# =========================

def execute_pipeline(
    query: Query,
    sources: list[ListingSource],
    normalize_fn,
    rank_fn,
    insight_fn
) -> RentContext:
    """
    Единственный разрешённый поток обработки домена
    """

    properties: list[Property] = []

    # 1. COLLECT
    for source in sources:
        fetched = source.fetch(query)
        if fetched:
            properties.extend(fetched)

    # 2. NORMALIZE
    normalized = normalize_fn(properties)

    # 3. RANK
    ranked = rank_fn(normalized, query)

    # 4. INSIGHTS
    insights = insight_fn(ranked)

    return RentContext(
        query=query,
        properties=properties,
        ranked=ranked,
        insights=insights
    )


# =========================
# 6. INTENT CONTRACT (FIXED MAP)
# =========================

INTENT_MAP = {
    "/rent": "rent_search",
    "/search": "rent_search",
    "/alert": "alert",
    "/compare": "city_compare",
}


def resolve_intent(text: str) -> str:
    for k, v in INTENT_MAP.items():
        if text.startswith(k):
            return v
    return "unknown"


EOFcat << 'EOF' > /opt/lentra/infra/app/core/domain/domain_core_v1.py
"""
DOMAIN CORE v1 — Freeze Layer

Цель:
- фиксирует доменную модель аренды
- убирает зависимость от orchestrator/consumer/UI runtime
- задаёт единый pipeline обработки запроса
"""

from dataclasses import dataclass, field
from typing import Optional, Any


# =========================
# 1. QUERY MODEL (INTENT LAYER)
# =========================

@dataclass
class Query:
    text: str
    country: str = "Vietnam"
    intent: str = "unknown"  # rent_search | property_info | city_compare | alert | unknown
    budget: Optional[tuple[int, int]] = None
    location: Optional[str] = None
    meta: dict = field(default_factory=dict)


# =========================
# 2. PROPERTY ENTITY
# =========================

@dataclass
class Property:
    id: str
    title: str
    price: int
    currency: str
    city: str
    district: str
    source: str
    images: list[str] = field(default_factory=list)
    attributes: dict = field(default_factory=dict)


# =========================
# 3. SOURCE CONTRACT
# =========================

class ListingSource:
    """
    Adapter contract: каждый внешний источник = drop-in реализация
    """

    name: str = "base"

    async def fetch(self, query: Query) -> list[Property]:
        raise NotImplementedError


# =========================
# 4. RUNTIME CONTEXT
# =========================

@dataclass
class RentContext:
    query: Query
    properties: list[Property]
    ranked: list[Property]
    insights: dict = field(default_factory=dict)


# =========================
# 5. DOMAIN PIPELINE (CORE ENGINE)
# =========================

def execute_pipeline(
    query: Query,
    sources: list[ListingSource],
    normalize_fn,
    rank_fn,
    insight_fn
) -> RentContext:
    """
    Единственный разрешённый поток обработки домена
    """

    properties: list[Property] = []

    # 1. COLLECT
    for source in sources:
        fetched = source.fetch(query)
        if fetched:
            properties.extend(fetched)

    # 2. NORMALIZE
    normalized = normalize_fn(properties)

    # 3. RANK
    ranked = rank_fn(normalized, query)

    # 4. INSIGHTS
    insights = insight_fn(ranked)

    return RentContext(
        query=query,
        properties=properties,
        ranked=ranked,
        insights=insights
    )


# =========================
# 6. INTENT CONTRACT (FIXED MAP)
# =========================

INTENT_MAP = {
    "/rent": "rent_search",
    "/search": "rent_search",
    "/alert": "alert",
    "/compare": "city_compare",
}


def resolve_intent(text: str) -> str:
    for k, v in INTENT_MAP.items():
        if text.startswith(k):
            return v
    return "unknown"


