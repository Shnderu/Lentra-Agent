from lentra.core.market_intelligence.contracts.market_object_contract import (
    MarketObjectContract,
    LocationContract
)


class ContractNormalizer:

    def normalize(self, listing: dict) -> dict:

        # -------------------------
        # PRICE SAFETY
        # -------------------------
        price = listing.get("price") or 0

        # -------------------------
        # LOCATION UNIFICATION
        # -------------------------
        loc = listing.get("location", {})

        if isinstance(loc, str):
            loc = LocationContract(
                segment=loc,
                micro_market="unknown"
            ).__dict__

        elif isinstance(loc, dict):
            loc = {
                "segment": loc.get("segment", "unknown"),
                "micro_market": loc.get("micro_market", "unknown")
            }

        else:
            loc = {
                "segment": "unknown",
                "micro_market": "unknown"
            }

        return {
            "price": float(price),
            "location": loc,
            "risk": float(listing.get("risk") or 0.5),
            "confidence": float(listing.get("confidence") or 0.5)
        }
