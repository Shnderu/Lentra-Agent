from lentra.runtime.intelligence_gateway import interpret

class IntelligenceGateway:
    def __init__(self):
        pass

    def analyze(self, payload: dict, trace=None):
        return interpret(payload)
