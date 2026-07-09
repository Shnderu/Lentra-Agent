from typing import Any, Dict


class CanonicalSearchEntrypoint:
    """
    SINGLE SEARCH ENTRYPOINT

    HARD ARCHITECTURE BOUNDARY:

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


    No:
    - dedup execution
    - ranking execution
    - market execution
    - intelligence execution

    allowed outside SearchPipeline.
    """


    def __init__(
        self,
        pipeline
    ):

        self.pipeline = pipeline



    def execute(
        self,
        payload: Dict[str, Any]
    ):

        if not payload:
            return {
                "results": [],
                "count": 0
            }


        return self.pipeline.run(
            payload
        )
