from app.core.rent_intelligence import RentIntelligenceEngine
from app.core.adapters.mock_rent_adapter import MockRentAdapter
from app.core.adapters.fake_real_estate_api import FakeRealEstateAPI
from app.core.aggregation.rent_aggregator import RentAggregator
from app.core.source_health import SourceHealth
from app.core.session.session_manager import SessionManager

import time


engine = RentIntelligenceEngine()

mock = MockRentAdapter()
real_api = FakeRealEstateAPI()

aggregator = RentAggregator()
health = SourceHealth()

session = SessionManager()


def safe_call(source_name, fn, query):
    start = time.time()

    try:
        result = fn(query)
        health.record_success(source_name, time.time() - start)
        return result

    except Exception as e:
        health.record_fail(source_name)
        print(f"[SOURCE FAIL] {source_name} -> {e}")
        return []


def rent_intelligence_handler(event, span, graph):
    span.start("rent_intel")

    text = event.payload.get("text")
    user_id = event.payload.get("user_id", "default")

    context = session.extract_context(user_id)

    intent = engine.parse(text)

    # 🔥 CONTEXT INJECTION
    if context.get("city") and not intent.get("city"):
        intent["city"] = context["city"]

    if context.get("budget") and not intent.get("budget"):
        intent["budget"] = context["budget"]

    print(f"[INTEL] {intent} | context={context}")

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
        "user_id": user_id,
        "trace_id": event.trace_id
    }


def rent_fetch_handler(event, span, graph):
    span.start("rent_fetch")

    intent = event.payload
    user_id = event.get("user_id", "default")

    query = intent.get("city") or "default"

    sources = [
        safe_call("mock", mock.search, query),
        safe_call("real_api", real_api.search, query)
    ]

    span.end("rent_fetch")

    return {
        "type": "RENT_AGGREGATE",
        "payload": {
            "query": query,
            "sources": sources
        },
        "intent": intent,
        "user_id": user_id,
        "trace_id": event.trace_id
    }


def rent_aggregate_handler(event, span, graph):
    span.start("aggregate")

    result = aggregator.aggregate(
        event.payload["query"],
        event.payload["sources"]
    )

    span.end("aggregate")

    return {
        "type": "RESPONSE",
        "payload": result,
        "intent": event.get("intent"),
        "user_id": event.get("user_id", "default"),
        "trace_id": event.trace_id
    }


def response_handler(event, span, graph):
    span.start("response")

    user_id = event.get("user_id", "default")
    intent = event.get("intent", {})

    # 🔥 UPDATE MEMORY
    session.update_context(user_id, intent)

    print("[RESPONSE]", event.payload)

    span.end("response")


def unknown_handler(event, span, graph):
    span.start("unknown")
    print("[UNKNOWN]", event.payload)
    span.end("unknown")
