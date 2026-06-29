class ScenarioRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._scenarios = {}
        return cls._instance

    @classmethod
    def instance(cls):
        return cls()

    def register(self, name, handler):
        self._scenarios[name] = handler

    def get(self, name):
        return self._scenarios.get(name)

    def has(self, name):
        return name in self._scenarios

    def exists(self, name):
        return self.has(name)

    def all(self):
        return dict(self._scenarios)
