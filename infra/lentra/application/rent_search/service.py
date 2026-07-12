from lentra.rent.runtime.observability.tracer.trace_recorder import TraceRecorder
from lentra.rent.runtime.observability.metrics.metrics import Metrics

from lentra.core.pipeline.canonical_search_pipeline import (
    CanonicalSearchPipeline
)

from lentra.core.pipeline.canonical_entrypoint import (
    CanonicalSearchEntrypoint
)


class RentSearchApplicationService:
    """
    Application orchestration layer.

    Delivery channels call this service.

    Search intelligence belongs to
    Canonical Market Intelligence pipeline.
    """

    def __init__(self, connector=None):

        self.connector = connector

        self.tracer = TraceRecorder()
        self.metrics = Metrics()

        pipeline = CanonicalSearchPipeline()

        self.entrypoint = CanonicalSearchEntrypoint(
            pipeline
        )


    async def search(
        self,
        payload: dict
    ):

        self.metrics.start(
            "rent_search"
        )


        self.tracer.node(
            "search_request_received",
            payload
        )


        query = payload.get(
            "text",
            ""
        )


        self.tracer.node(
            "market_intelligence_pipeline",
            {
                "query": query
            }
        )


        result = self.entrypoint.execute(
            {
                "query": query
            }
        )


        self.tracer.node(
            "market_intelligence_result",
            {
                "count": len(result)
                if isinstance(result, list)
                else 1
            }
        )


        self.metrics.end(
            "rent_search"
        )


        return {
            "result": result,
            "trace": self.tracer.dump(),
            "metrics": self.metrics.dump(),
            "mode": "market_intelligence_canonical_v1"
        }
