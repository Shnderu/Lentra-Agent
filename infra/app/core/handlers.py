from app.core.rent_intelligence import RentIntelligenceEngine
from app.core.adapters.mock_rent_adapter import MockRentAdapter
from app.core.adapters.fake_real_estate_api import FakeRealEstateAPI
from app.core.aggregation.rent_aggregator import RentAggregator
import time


engine = RentIntelligenceEngine()

mock = MockRentAdapter()
real_api = FakeRealEstateAPI()

aggregator = RentAggregator()


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
        "type": "RENT_FETCH",
        "payload": intent,
        "trace_id": event.trace_id
    }


def rent_fetch_handler(event, span, graph):
    span.start("rent_fetch")

    intent = event.payload
    query = intent.get("city") or "default"

    # 🔥 MULTI SOURCE CALL
    sources = []

    try:
        sources.append(mock.search(query))
    except Exception as e:
        print("[MOCK FAIL]", e)

    try:
        sources.append(real_api.search(query))
    except Exception as e:
        print("[REAL API FAIL]", e)

    span.end("rent_fetch")

    return {
        "type": "RENT_AGGREGATE",
        "payload": {
            "query": query,
            "sources": sources
        },
        "trace_id": event.trace_id
    }


def rent_aggregate_handler(event, span, graph):
    span.start("aggregate")

    payload = event.payload

    result = aggregator.aggregate(
        payload["query"],
        payload["sources"]
    )

    print(f"[AGGREGATED] total={result.total}")

    span.end("aggregate")

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
