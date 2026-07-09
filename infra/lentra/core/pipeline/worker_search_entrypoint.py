from typing import Dict, Any

from lentra.core.pipeline.canonical_search_pipeline import (
    CanonicalSearchPipeline
)

from lentra.core.pipeline.canonical_entrypoint import (
    CanonicalSearchEntrypoint
)


class WorkerSearchEntrypoint:
    """
    Worker execution boundary.

    Worker
      |
      v
    CanonicalSearchEntrypoint
      |
      v
    SearchPipeline
    """

    def __init__(self):

        self.pipeline = CanonicalSearchPipeline()

        self.entrypoint = CanonicalSearchEntrypoint(
            self.pipeline
        )


    def execute(
        self,
        payload: Dict[str, Any]
    ):

        return self.entrypoint.execute(
            payload
        )
