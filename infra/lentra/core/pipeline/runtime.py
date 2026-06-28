from lentra.core.dto.listing_dto import ListingDTO
from lentra.core.dto.validator import ListingValidator


class PipelineRuntime:

    def __init__(self, pipeline):
        self.pipeline = pipeline

    def run(self, input_data):

        dto = ListingDTO.from_any(input_data)

        ListingValidator.validate(dto)

        return self.pipeline.run(dto)
