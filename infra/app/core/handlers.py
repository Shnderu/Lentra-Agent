from app.services.rent_search import rent_search
from app.core.rent_intelligence import RentIntelligenceEngine
import time


engine = RentIntelligenceEngine()


def intent_router(event, span, graph):
    span.start("router")

    text = event.payload.get("text", "")

    span.end("router")

    return {
        "type": "INTENT",
        "payload": {"text": text},
        "trace_id": event.trace_id
    }


def rent_intelligence_handler(event, span, graph):
    span.start("rent_intel")

    text = event.payload.get("text")

    intent = engine.parse(text)

    print(f"[INTEL] {intent}")

    span.end("rent_intel")

    if intent["intent"] != "RENT":
        return {
            "type": "UNKNOWN",
            "payload": {"raw": text},
            "trace_id": event.trace_id
        }

    return {
        "type": "RENT_SEARCH",
        "payload": intent,
        "trace_id": event.trace_id
    }


def rent_search_handler(event, span, graph):
    span.start("rent_handler")

    intent = event.payload

    query = intent.get("city") or "default"

    t0 = time.time()
    result = rent_search(query)
    latency = time.time() - t0

    print(f"[RENT] latency={latency:.3f}s")

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
