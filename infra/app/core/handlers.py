from app.services.rent_search import rent_search
from app.core.circuit_breaker import CircuitBreaker
import time


cb = CircuitBreaker(fail_threshold=2, reset_timeout=4)


def intent_router(event, span, graph):
    span.start("router")

    text = event.payload.get("text", "")

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

    query = event.payload.get("query")

    if not cb.allow():
        print("[CB] request blocked")
        return {
            "type": "RESPONSE",
            "payload": {"error": "circuit_open"},
            "trace_id": event.trace_id
        }

    try:
        t0 = time.time()

        result = rent_search(query)

        latency = time.time() - t0

        span.end("rent_service")

        cb.success()

        print(f"[RENT] ok latency={latency:.3f}s")

        span.end("rent_handler")

        return {
            "type": "RESPONSE",
            "payload": result,
            "trace_id": event.trace_id
        }

    except Exception as e:
        cb.fail()
        span.end("rent_handler")

        print(f"[RENT] fail err={e}")

        return {
            "type": "RESPONSE",
            "payload": {"error": str(e)},
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
