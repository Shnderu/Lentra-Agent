from lentra.core.dto.listing_dto import ListingDTO
from lentra.core.dto.validator import ListingValidator


class LentraPipeline:

    def __init__(self):
        self.steps = []

    def run(self, input_data):

        # HARD GATE: normalize EVERYTHING
        dto = ListingDTO.from_any(input_data)

        # HARD VALIDATION (fail fast, no silent corruption)
        ListingValidator.validate(dto)

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
from lentra.core.pipeline.retry import RetryPolicy


class LentraPipeline:

    def __init__(self):
        self.steps = []
        self.retry = RetryPolicy(retries=3)

    def run(self, input_data):

        def _run():
            dto = ListingDTO.from_any(input_data)
            ListingValidator.validate(dto)

            data = dto

            for step in self.steps:
                data = step.run(data)

            return self._finalize(data)

        return self.retry.execute(_run)
