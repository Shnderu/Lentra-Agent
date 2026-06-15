import time


def log_search(event, result):
    meta = result.get("meta", {})

    print("[SEARCH LOG]", {
        "query": event.get("payload", {}).get("text"),
        "count": meta.get("count"),
        "latency_ms": meta.get("latency_ms"),
        "error": meta.get("error")
    })
