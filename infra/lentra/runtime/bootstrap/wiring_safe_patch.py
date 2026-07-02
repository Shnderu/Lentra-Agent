

    builder = GraphV2Builder()
    hook = GraphV2EnrichmentHook(builder)

    original_handle = gateway.handle

    def wrapped(payload):
        result = original_handle(payload)
        return hook.apply(result, payload)

    gateway.handle = wrapped
    return gateway
