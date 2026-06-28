from lentra.core.dto.listing_dto import ListingDTO


class ListingValidator:

    @staticmethod
    def validate(listing: ListingDTO) -> None:

        if not listing.title:
            raise ValueError("ListingDTO.title is required")

        if listing.price < 0:
            raise ValueError("ListingDTO.price must be >= 0")

        if listing.location is None:
            listing.location = ""

        # жесткое правило: pipeline не принимает "сырой мусор"
        if isinstance(listing.title, dict):
            raise ValueError("Invalid title type: dict detected")

        if hasattr(listing.title, "get"):
            raise ValueError("Invalid title structure (dict-like)")
