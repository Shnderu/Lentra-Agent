def assert_registry_bound(app):
    gw = app.state.gateway

    if not hasattr(gw, "registry") or gw.registry is None:
        raise RuntimeError("REGISTRY NOT BOUND")

    if len(gw.registry._engines) == 0:
        raise RuntimeError("NO ENGINES REGISTERED")
