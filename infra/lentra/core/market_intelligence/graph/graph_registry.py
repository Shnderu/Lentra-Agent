class GraphRegistry:

    """
    Central immutable registry of ALL engines.
    No engine should be imported directly outside registry.
    """

    def __init__(self):
        self._engines = {}

    def register(self, name: str, engine: object):
        if name in self._engines:
            raise Exception(f"Engine already registered: {name}")

        self._engines[name] = engine

    def get(self, name: str):
        return self._engines[name]

    def all(self):
        return self._engines
