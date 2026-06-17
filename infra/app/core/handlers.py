from app.services.rent_search import rent_search
from app.core.metrics import LatencyHistogram
import time


def intent_router(event, span, graph):
    span.start("router")

    text = event.payload.get("text", "")
    time.sleep(0.005)

    if "rent" in text.lower():
        out = {
            "type": "RENT_SEARCH",
            "payload": {"query": text},
            "trace_id": event.trace_id
        }
    else:
        out = {
            "type": "UNKNOWN",
            "payload": {"raw": text},
            "trace_id": event.trace_id
        }

    span.end("router")
    return out


def rent_search_handler(event, span, graph):
    span.start("rent_handler")

    hist: LatencyHistogram = getattr(span, "hist", None)

    query = event.payload.get("query")

    t0 = time.time()
    result = rent_search(query)
    latency = time.time() - t0

    if hist:
        hist.observe("rent_search", latency)

    span.end("rent_handler")

    return {
        "type": "RESPONSE",
        "payload": result,
        "trace_id": event.trace_id
    }


def response_handler(event, span, graph):
    span.start("response")
    print("[RESPONSE]", event.payload)
    span.end("response")


def unknown_handler(event, span, graph):
    span.start("unknown")
    print("[UNKNOWN]", event.payload)
    span.end("unknown")
