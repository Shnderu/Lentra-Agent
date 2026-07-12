from lentra.rent.runtime.observability.tracer.trace_recorder import TraceRecorder
from lentra.rent.runtime.observability.metrics.metrics import Metrics


class RentSearchApplicationService:
    """
    Application orchestration layer.

    Telegram and other delivery channels
    must call this service instead of owning
    search workflow logic.
    """

    def __init__(self, connector):

        self.connector = connector
        self.tracer = TraceRecorder()
        self.metrics = Metrics()


    async def search(
        self,
        payload: dict
    ):

        self.metrics.start(
            "rent_search"
        )


        n0 = "search_request_received"

        self.tracer.node(
            n0,
            payload
        )


        query = {
            "text": payload.get("text"),
            "user_id": payload.get("user_id")
        }


        n1 = "connector_call"

        self.tracer.node(
            n1,
            query
        )

        self.tracer.edge(
            n0,
            n1
        )


        result = await self.connector.call(
            query
        )


        n2 = "connector_result"

        self.tracer.node(
            n2,
            {
                "items": len(
                    result.get(
                        "items",
                        []
                    )
                )
            }
        )


        self.tracer.edge(
            n1,
            n2
        )


        self.metrics.end(
            "rent_search"
        )


        return {
            "result": result,
            "trace": self.tracer.dump(),
            "metrics": self.metrics.dump()
        }
