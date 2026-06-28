from typing import Any


class ListingValidationError(Exception):
    pass


def validate_listing(raw: Any) -> None:
    """
    HARD VALIDATION GATE.
    Никаких silent fallback.
    """

    if raw is None:
        raise ListingValidationError("Listing is None")

    if isinstance(raw, str):
        raise ListingValidationError("Listing is str (invalid input)")

    if not isinstance(raw, dict) and not hasattr(raw, "price"):
        raise ListingValidationError(f"Unsupported listing type: {type(raw)}")

    # dict path
    if isinstance(raw, dict):
        if not raw.get("price"):
            raise ListingValidationError("Missing price")
        if not (raw.get("city") or raw.get("location")):
            raise ListingValidationError("Missing location")

    # object path
    else:
        if not getattr(raw, "price", None):
            raise ListingValidationError("Missing price")
        if not (getattr(raw, "city", None) or getattr(raw, "location", None)):
            raise ListingValidationError("Missing location")
