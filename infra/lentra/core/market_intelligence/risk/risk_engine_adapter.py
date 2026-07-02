class RiskEngineAdapter:
    def __init__(self, engine):
        self.engine = engine

    def evaluate(self, payload: dict) -> dict:
        # нормализуем вход под process()
        return self.engine.process(payload)
