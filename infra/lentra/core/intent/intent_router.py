from lentra.core.runtime.trace_graph_v2 import RuntimeTraceV2


class IntentRouter:

    def __init__(self, registry=None, trace: RuntimeTraceV2 = None):
        self.registry = registry
        self.trace = trace

    def detect(self, text: str):

        if self.trace:
            self.trace.emit("intent_router", "detect_start", {"text": text})

        intent = self._detect(text)

        if self.trace:
            self.trace.emit("intent_router", "detect_result", {"intent": intent})

        return intent

    def _detect(self, text: str):

        text = (text or "").lower()

        if "search" in text:
            return "search"

        if "compare" in text:
            return "compare"

        return "search"
