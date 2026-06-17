from lentra.rent.runtime.observability.tracer.trace_recorder import TraceRecorder
from lentra.rent.runtime.observability.metrics.metrics import Metrics


class RentSearchService:

    def __init__(self, connector):
        self.connector = connector
        self.tracer = TraceRecorder()
        self.metrics = Metrics()

    async def search(self, payload: dict):

        self.metrics.start("rent_search")

        # --- TRACE START ---
        n0 = "telegram_update_received"
        self.tracer.node(n0, payload)

        query = {
            "text": payload.get("text"),
            "user_id": payload.get("user_id")
        }

        n1 = "connector_call"
        self.tracer.node(n1, query)
        self.tracer.edge(n0, n1)

        # --- CONNECTOR CALL (STRICT CONTRACT) ---
        result = await self.connector.call(query)

        n2 = "connector_result"
        self.tracer.node(n2, {"items": len(result.get("items", []))})
        self.tracer.edge(n1, n2)

        n3 = "rent_search_end"
        self.tracer.node(n3, {})
        self.tracer.edge(n2, n3)

        self.metrics.end("rent_search")

        return {
            "text": "rent_search v1 stable",
            "raw": result,
            "trace": self.tracer.dump(),
            "metrics": self.metrics.dump()
        }
