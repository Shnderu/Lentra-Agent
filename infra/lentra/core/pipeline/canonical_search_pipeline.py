from typing import Dict, Any


class CanonicalSearchPipeline:
    """
    CANONICAL SEARCH FACADE

    Architecture boundary:

    API
      |
      v
    CanonicalSearchEntrypoint
      |
      v
    CanonicalSearchPipeline
      |
      v
    SearchPipeline
      |
      v
    Market Intelligence OS

    This layer contains no business logic.
    """


    def __init__(
        self,
        pipeline=None
    ):

        if pipeline is not None:
            self.pipeline = pipeline

        else:
            from lentra.api.pipeline.search_pipeline import SearchPipeline

            self.pipeline = SearchPipeline()


    def run(
        self,
        payload: Dict[str, Any]
    ):

        return self.pipeline.run(
            payload
        )
