import inspect


class ConnectorInspector:
    """
    Проверяет connector на runtime ДО вызова
    """

    REQUIRED_METHOD = "call"

    def validate(self, connector: object):
        if not hasattr(connector, self.REQUIRED_METHOD):
            return {
                "ok": False,
                "error": f"Missing method: {self.REQUIRED_METHOD}",
                "type": type(connector).__name__
            }

        method = getattr(connector, self.REQUIRED_METHOD)

        if not inspect.iscoroutinefunction(method):
            return {
                "ok": False,
                "error": "call() must be async",
                "type": type(connector).__name__
            }

        return {"ok": True}
