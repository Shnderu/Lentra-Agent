from typing import Any


class TraceValidationError(Exception):
    pass


class TraceValidator:
    """
    TRACE GRAPH V2 IMMUTABLE VALIDATION LAYER
    """

    def validate(self, router, listener, trace):
        self._validate_router(router)
        self._validate_listener(listener)
        self._validate_trace(trace)

        self._validate_async_boundary(router, listener)

        return True

    def _validate_router(self, router):
        if not hasattr(router, "route"):
            raise TraceValidationError("Router missing 'route' method")

        if callable(router.route) is False:
            raise TraceValidationError("Router.route must be callable")

        # ❗ must be sync
        if hasattr(router.route, "__await__"):
            raise TraceValidationError("Router.route must NOT be async")

    def _validate_listener(self, listener):
        if not hasattr(listener, "handle_event"):
            raise TraceValidationError("Listener missing 'handle_event'")

        if not callable(listener.handle_event):
            raise TraceValidationError("Listener.handle_event must be callable")

        if not hasattr(listener, "next_event"):
            raise TraceValidationError("Listener missing 'next_event'")

    def _validate_trace(self, trace):
        if trace is None:
            return

        if not hasattr(trace, "record"):
            raise TraceValidationError("Trace missing 'record' method")

    def _validate_async_boundary(self, router, listener):
        # STRICT RULE:
        # router = SYNC ONLY
        # listener = ASYNC OK
        # trace = ASYNC OK

        if hasattr(router.route, "__await__"):
            raise TraceValidationError("Router must be sync (graph layer violation)")
