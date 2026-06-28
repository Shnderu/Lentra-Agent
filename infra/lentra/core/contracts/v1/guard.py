from lentra.core.contracts.v1.listing_dto import ListingDTO


def enforce_listing_contract(raw_listing):
    """
    HARD CONTRACT GATE:
    pipeline NEVER sees raw data
    """

    if raw_listing is None:
        raise ValueError("[CONTRACT] None input")

    if isinstance(raw_listing, str):
        raise ValueError("[CONTRACT] str is forbidden input")

    # 1) already DTO
    if isinstance(raw_listing, ListingDTO):
        return raw_listing

    # 2) normalize anything else
    try:
        dto = ListingDTO.from_raw(raw_listing)
    except Exception as e:
        raise ValueError(f"[CONTRACT] invalid listing: {e}")

    # HARD validation
    if not dto.id:
        raise ValueError("[CONTRACT] missing id")

    if dto.price is None or dto.price <= 0:
        raise ValueError("[CONTRACT] invalid price")

    return dto
