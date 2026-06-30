from lentra.core.runtime.trace_graph_v2 import RuntimeTraceV2


class IntelligenceGateway:

    def __init__(self, trace: RuntimeTraceV2 = None):
        self.trace = trace

    def execute(self, listings, query_text, source="telegram"):

        if self.trace:
            self.trace.emit(
                "gateway",
                "execute_start",
                {
                    "source": source,
                    "query": query_text
                }
            )

        result = self._run(listings, query_text)

        if self.trace:
            self.trace.emit(
                "gateway",
                "execute_done",
                {"items": len(result) if result else 0}
            )

            self.trace.link(
                "gateway.execute_start",
                "renderer.build",
                "flows_to"
            )

        return result

    def _run(self, listings, query_text):
        return listings
