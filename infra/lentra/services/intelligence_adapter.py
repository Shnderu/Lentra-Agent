from lentra.runtime.intelligence_gateway import interpret

class IntelligenceAdapter:
    def __init__(self):
        pass

    def analyze(self, payload: dict):
        return interpret(payload)
