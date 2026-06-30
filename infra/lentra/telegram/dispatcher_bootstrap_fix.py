from lentra.core.runtime.trace_graph import TraceGraph

trace = TraceGraph()


def instrument_router(router):

    def wrapped_detect(text):
        trace.emit("intent_router", "detect", {"text": text})

        result = router.detect(text)

        trace.emit("intent_router", "result", {"intent": result})

        return result

    router.detect = wrapped_detect
    return router


def link(a: str, b: str, rel: str = "calls"):
    trace.link(a, b, rel)
