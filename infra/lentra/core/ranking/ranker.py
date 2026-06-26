from lentra.core.models.listing import Listing


def rank_listings(listings: list) -> list:
    return sorted(
        listings,
        key=lambda x: (
            x.risk_score or 0,
            x.price or 0
        )
    )
