class ListingContractGuard:

    @staticmethod
    def normalize(listing: dict) -> dict:
        # -------- PRICE SAFETY --------
        listing["price"] = float(listing.get("price") or 0)

        # -------- MARKET PRICE SAFETY --------
        mp = listing.get("market_price")
        listing["market_price"] = float(mp) if mp is not None else listing["price"]

        # -------- LOCATION NORMALIZATION --------
        loc = listing.get("location")

        if isinstance(loc, str):
            listing["location"] = {
                "segment": loc,
                "micro_market": "unknown"
            }

        if isinstance(loc, dict):
            listing["location"] = {
                "segment": loc.get("segment", "unknown"),
                "micro_market": loc.get("micro_market", "unknown")
            }

        if not listing.get("location"):
            listing["location"] = {
                "segment": "unknown",
                "micro_market": "unknown"
            }

        # -------- RISK SAFETY --------
        listing["risk"] = float(listing.get("risk") or 0.5)

        return listing
