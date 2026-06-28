from lentra.core.dto.listing_dto import ListingDTO
from lentra.core.dto.validator import ListingValidator


class LentraPipeline:

    def __init__(self):
        # здесь уже могут быть scorer / dedup / market engine
        self.steps = []

    def run(self, input_data):

        # 1. NORMALIZE → DTO
        dto = ListingDTO.from_any(input_data)

        # 2. VALIDATE → hard gate
        ListingValidator.validate(dto)

        # 3. EXECUTION FLOW
        data = dto

        for step in self.steps:
            data = step.run(data)

        return self._finalize(data)

    def _finalize(self, dto: ListingDTO):

        return {
            "id": dto.id,
            "title": dto.title,
            "location": dto.location,
            "price": dto.price,
            "currency": dto.currency,
            "source": dto.source
        }
