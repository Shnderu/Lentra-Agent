from typing import Dict, Any

from lentra.api.pipeline.search_pipeline import SearchPipeline


class CanonicalSearchPipeline:
    """
    CANONICAL SEARCH FACADE

    ARCH RULE:

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

    This class MUST NOT contain business logic.

    SearchPipeline is the single source of truth.
    """

    def __init__(self):

        self.pipeline = SearchPipeline()


    def run(
        self,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:

        return self.pipeline.run(
            payload
        )
