from lentra.runtime.intelligence_gateway import interpret

class PipelineDefinitionService:
    def __init__(self):
        pass

    def analyze(self, payload: dict):
        return interpret(payload)
