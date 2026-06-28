from typing import Any
from lentra.core.dto.listing_dto import ListingDTO


class PipelineValidator:
    """
    Hard boundary validator:
    - rejects broken Listing objects
    - forces DTO conversion
    """

    def validate_listing(self, data: Any) -> ListingDTO:
        try:
            dto = ListingDTO.from_raw(data)

            if not dto.title and not dto.city:
                raise ValueError("Invalid listing: missing title and city")

            return dto

        except Exception as e:
            raise ValueError(f"[PIPELINE VALIDATION ERROR] {e}")
