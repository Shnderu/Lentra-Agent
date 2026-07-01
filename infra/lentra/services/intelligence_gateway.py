from lentra.runtime.intelligence_gateway import interpret


class IntelligenceGateway:
    """
    CANONICAL GATEWAY

    Больше НЕТ orchestrator / analyze / routing logic.
    Только один путь → AI OS.
    """

    def analyze(self, payload: dict, trace=None):
        return interpret(payload)
