import json

from worker.sources.faswaz import FaswazSource


def run(payload: str):
    query = json.loads(payload)

    source = FaswazSource()

    results = source.search(query)

    return {
        "query": query,
        "results": results,
        "count": len(results)
    }
