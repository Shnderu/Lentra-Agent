def trace_router(container, router, payload=None):
    container.graph.add("router", "enter", payload or {})

    try:
        # безопасный "пустой проход"
        result = str(router)
        container.graph.add("router", "exit", {"ok": True})
        return result
    except Exception as e:
        container.graph.add("router", "error", {"err": str(e)})
        return None
