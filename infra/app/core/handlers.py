from app.core.rent_intelligence import RentIntelligenceEngine
from app.core.adapters.mock_rent_adapter import MockRentAdapter
from app.core.adapters.fake_real_estate_api import FakeRealEstateAPI
from app.core.aggregation.rent_aggregator import RentAggregator
from app.core.source_health import SourceHealth
from app.core.context.context_injector import ContextInjector
import time


engine = RentIntelligenceEngine()

mock = MockRentAdapter()
real_api = FakeRealEstateAPI()

aggregator = RentAggregator()
health = SourceHealth()

context = ContextInjector()


def safe_call(source_name, fn, query):
    start = time.time()

    try:
        result = fn(query)
        latency = time.time() - start
        health.record_success(source_name, latency)
        return result

    except Exception as e:
        health.record_fail(source_name)
        print(f"[SOURCE FAIL] {source_name} -> {e}")
        return []


def rent_intelligence_handler(event, span, graph):
    span.start("rent_intel")

    text = event.payload.get("text")
    user_id = event.payload.get("user_id", "default")

    intent = engine.parse(text)

    # 🔥 update persistent memory
    context.update(user_id, {
        **intent,
        "raw": text
    })

    enriched = context.enrich(user_id, intent)

    span.end("rent_intel")

    if enriched.get("intent") != "RENT":
        return {
            "type": "UNKNOWN",
            "payload": {"raw": text},
            "trace_id": event.trace_id
        }

    return {
        "type": "RENT_FETCH",
        "payload": enriched,
        "trace_id": event.trace_id
    }


def rent_fetch_handler(event, span, graph):
    span.start("rent_fetch")

    intent = event.payload
    query = intent.get("city") or "default"

    sources = []

    if health.is_healthy("mock"):
        sources.append(safe_call("mock", mock.search, query))

    if health.is_healthy("real_api"):
        sources.append(safe_call("real_api", real_api.search, query))

    span.end("rent_fetch")

    return {
        "type": "RENT_AGGREGATE",
        "payload": {
            "query": query,
            "sources": sources,
            "session": intent.get("session")
        },
        "trace_id": event.trace_id
    }


def rent_aggregate_handler(event, span, graph):
    span.start("aggregate")

    result = aggregator.aggregate(
        event.payload["query"],
        event.payload["sources"],
        event.payload.get("session")
    )

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
