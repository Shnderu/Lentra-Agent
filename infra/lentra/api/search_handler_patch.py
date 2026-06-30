from lentra.core.market_intelligence.search.search_validator import SearchValidator
from lentra.services.intelligence_gateway import IntelligenceGateway

validator = SearchValidator()
gateway = IntelligenceGateway()


def search(listings, query_text):
    payload = {
        "listings": listings,
        "query_text": query_text
    }

    validated = validator.validate_request(payload)

    result = gateway.process(
        validated["listings"],
        validated["query_text"]
    )

    return validator.validate_response(result)
