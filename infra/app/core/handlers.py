from app.core.rent_intelligence import RentIntelligenceEngine
from app.core.adapters.mock_rent_adapter import MockRentAdapter
from app.core.adapters.fake_real_estate_api import FakeRealEstateAPI
from app.core.aggregation.rent_aggregator import RentAggregator
from app.core.source_health import SourceHealth
from app.core.context.context_injector import ContextInjector
from app.core.contracts.query_options import QueryOptions
from app.core.contracts.query_validator import QueryValidator
from app.core.ux.response_serializer import ResponseSerializer
import time


engine = RentIntelligenceEngine()
mock = MockRentAdapter()
real_api = FakeRealEstateAPI()

aggregator = RentAggregator()
serializer = ResponseSerializer()

health = SourceHealth()
context = ContextInjector()
validator = QueryValidator()


def rent_intelligence_handler(event, span):
    span.start("intent")

    text = event.payload.get("text")
    user_id = event.payload.get("user_id", "default")

    intent = engine.parse(text)

    context.update(user_id, {**intent, "raw": text})
    enriched = context.enrich(user_id, intent)

    span.end("intent")

    return {
        "payload": enriched,
        "trace_id": event.trace_id
    }


def rent_fetch_handler(event, span):
    span.start("fetch")

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
        sources.append(mock.search(query))

    if health.is_healthy("real_api"):
        sources.append(real_api.search(query))

    span.end("fetch")

    return {
        "payload": {
            "query": query,
            "sources": sources,
            "session": intent.get("session"),
            "options": options
        },
        "trace_id": event.trace_id
    }


def rent_aggregate_handler(event, span):
    span.start("aggregate")

    payload = event.payload

    result = aggregator.aggregate(
        payload["query"],
        payload["sources"],
        payload.get("session")
    )

    span.end("aggregate")

    return {
        "payload": result,
        "trace_id": event.trace_id
    }


def response_handler(event, span):
    span.start("response")

    print("[RESPONSE]", event.payload)

    span.end("response")

    return event
