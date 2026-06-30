from typing import List, Dict, Any, TypedDict, Optional


# =========================
# INPUT CONTRACT
# =========================

class Listing(TypedDict, total=False):
    price: float
    title: str
    city: str
    location: str


class AnalyzeIntent(TypedDict, total=False):
    listings: List[Listing]
    query_text: Optional[str]


# =========================
# OUTPUT CONTRACT
# =========================

class EnrichedListing(TypedDict, total=False):
    price: float
    title: str

    # enrichment layers
    is_duplicate: bool
    risk_score: float
    geo_score: float
    expat_score: float

    # ranking
    final_score: float

    # observability
    event_emitted: bool


class PipelineResult(TypedDict, total=False):
    listings: List[EnrichedListing]
    query_text: str
