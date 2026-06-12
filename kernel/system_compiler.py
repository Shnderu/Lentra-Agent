import uuid

def compile_system(intent: str):
    system_id = str(uuid.uuid4())

    graph = {
        "id": system_id,
        "intent": intent,
        "nodes": []
    }

    if "rent" in intent:
        graph["nodes"] = [
            "intent_router",
            "geo_search",
            "ranking_ai",
            "result_store"
        ]
    else:
        graph["nodes"] = [
            "generic_fetch",
            "process",
            "store"
        ]

    return graph
