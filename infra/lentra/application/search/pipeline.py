import time
from lentra.domain.property.search import search_properties
from lentralication.contracts.guards import safe_get_payload
from lentralication.search.logger import log_search


def execute_search(event: dict, state=None):
    start = time.time()

    payload = safe_get_payload(event)

    try:
        results = search_properties(payload, state)

        duration = time.time() - start

        response = {
            "results": results,
            "meta": {
                "count": len(results),
                "latency_ms": int(duration * 1000)
            }
        }

        log_search(event, response)

        return response

    except Exception as e:
        response = {
            "results": [],
            "meta": {
                "error": str(e),
                "count": 0
            }
        }

        log_search(event, response)

        return response
