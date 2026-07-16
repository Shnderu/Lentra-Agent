from lentra.core.dto.listing_dto import ListingDTO


def normalize(listings: list) -> list:
    normalized = []

    for x in listings:
        listing = ListingDTO.from_raw(x)

        normalized.append(listing)

    return normalized
