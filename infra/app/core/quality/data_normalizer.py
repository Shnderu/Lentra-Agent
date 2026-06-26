from lentra.core.contracts.listing_dto import ListingDTO


class DataNormalizer:

    def normalize(self, listing: ListingDTO):

        # -------------------------
        # TITLE CLEANUP
        # -------------------------
        if listing.title:
            listing.title = listing.title.strip()

        # -------------------------
        # PRICE SANITIZATION
        # -------------------------
        if listing.price is not None:
            try:
                listing.price = int(listing.price)
                if listing.price < 0:
                    listing.price = None
            except Exception:
                listing.price = None

        # -------------------------
        # CITY NORMALIZATION
        # -------------------------
        if listing.city:
            listing.city = listing.city.strip().lower()

        # -------------------------
        # SOURCE SANITIZATION
        # -------------------------
        if listing.source:
            listing.source = listing.source.strip().lower()

        # -------------------------
        # VALIDITY RULES
        # -------------------------
        if not listing.title:
            return None

        return listing
