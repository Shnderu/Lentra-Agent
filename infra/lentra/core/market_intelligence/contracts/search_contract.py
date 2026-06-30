from typing import List, TypedDict, Optional


class SearchListing(TypedDict, total=False):
    price: float
    title: str
    city: Optional[str]
    location: Optional[str]


class SearchRequest(TypedDict, total=False):
    listings: List[SearchListing]
    query_text: str


class SearchResponseItem(TypedDict, total=False):
    price: float
    title: str

    # pipeline flags
    event_emitted: bool

    # future compatibility hooks
    score: float
