from lentra.bot.handlers.instrumentation import HandlerTraceWrapper


class IntentRouter:

    def __init__(self, trace=None):
        self.trace = trace
        self.instrument = HandlerTraceWrapper(trace) if trace else None

    def detect(self, text: str):

        if self.instrument:
            return self.instrument.wrap("intent_router.detect", self._detect_impl)(text)

        return self._detect_impl(text)

    def _detect_impl(self, text: str):

        text = (text or "").lower()

        if "compare" in text:
            return "compare"

        if "price" in text or "rent" in text:
            return "search"

        if "explain" in text:
            return "explain"

        return "unknown"
