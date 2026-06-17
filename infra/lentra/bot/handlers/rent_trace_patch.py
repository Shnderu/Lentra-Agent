def trace_rent_flow(container, service):
    container.graph.add("rent", "service_start")

    try:
        result = service.search({"trace": True})
        container.graph.add("rent", "service_done", result)
        return result
    except Exception as e:
        container.graph.add("rent", "service_error", {"err": str(e)})
        raise
