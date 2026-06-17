from app.core.rent_intelligence import RentIntelligenceEngine
from app.core.adapters.mock_rent_adapter import MockRentAdapter
from app.core.adapters.fake_real_estate_api import FakeRealEstateAPI
from app.core.aggregation.rent_aggregator import RentAggregator
from app.core.source_health import SourceHealth
from app.core.context.context_injector import ContextInjector
from app.core.ux.response_serializer import ResponseSerializer
from app.core.contracts.query_options import QueryOptions
from app.core.contracts.query_validator import QueryValidator
import time


engine = RentIntelligenceEngine()

mock = MockRentAdapter()
real_api = FakeRealEstateAPI()

aggregator = RentAggregator()
serializer = ResponseSerializer()

health = SourceHealth()
context = ContextInjector()
validator = QueryValidator()


def safe_call(source_name, fn, query):
    start = time.time()

    try:
        result = fn(query)
        latency = time.time() - start
        health.record_success(source_name, latency)
        return result

    except Exception:
        health.record_fail(source_name)
        return []


def rent_intelligence_handler(event, span, graph):
    span.start("rent_intel")

    text = event.payload.get("text")
    user_id = event.payload.get("user_id", "default")

    intent = engine.parse(text)

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

    options = QueryOptions(
        city=intent.get("city"),
        budget=intent.get("budget"),
        limit=10,
        sort_by="score",
        offset=0
    )

    options = validator.validate(options)

    sources = []

    if health.is_healthy("mock"):
        sources.append(safe_call("mock", mock.search, query))

    if health.is_healthy("real_api"):
        sources.append(safe_call("real_api", real_api.search, query))

    span.end("rent_fetch")

    return {
        "type": "RENT_AGGREGATE",
        "payload": {
            "trace_id": event.trace_id,
            "query": query,
            "sources": sources,
            "session": intent.get("session")
        },
        "trace_id": event.trace_id
    }


def rent_aggregate_handler(event, span, graph):
    span.start("aggregate")

    payload = event.payload

    raw = aggregator.aggregate(
        payload["query"],
        payload["sources"],
        payload.get("session")
    )

    result = serializer.serialize(
        payload["trace_id"],
        raw
    )

    span.end("aggregate")

    return {
        "type": "RESPONSE",
        "payload": result.to_dict(),
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
