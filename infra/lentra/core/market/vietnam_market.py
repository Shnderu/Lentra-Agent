from collections import defaultdict
from typing import List, Dict

from lentra.core.dto.listing_dto import ListingDTO


VIETNAM_MARKET_ZONES = {
    "da nang": ["beach_zone", "expat_center", "river_side", "outskirts"],
    "ho chi minh city": ["district_1", "district_2", "district_7", "binh_thanh"],
    "hanoi": ["old_quarter", "tay_ho", "cau_giay"],
    "nha trang": ["beach_zone", "center", "north_area"],
}


def detect_zone(location: str) -> str:
    loc = (location or "").lower()

    if "beach" in loc:
        return "beach_zone"
    if "center" in loc:
        return "center"
    if "district 1" in loc:
        return "district_1"
    if "tay ho" in loc:
        return "tay_ho"

    return "unknown"


def build_market_index(listings: List[ListingDTO]) -> Dict:
    index = defaultdict(list)

    for listing in listings:
        location_text = str(listing.location or "")

        city = (listing.city or location_text).lower()
        zone = detect_zone(location_text)

        key = f"{city}:{zone}"

        index[key].append(
            listing.market_price or listing.price
        )

    market_stats = {}

    for key, prices in index.items():
        if not prices:
            continue

        market_stats[key] = {
            "avg_price": round(sum(prices) / len(prices), 2),
            "min": min(prices),
            "max": max(prices),
            "count": len(prices),
        }

    return market_stats
