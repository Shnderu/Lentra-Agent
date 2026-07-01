from typing import Any, Dict

from lentra.core.market_intelligence.output.facade import MarketIntelligenceOutputFacade


class MarketIntelligenceEngine:
    """
    LEGACY COMPAT LAYER

    ВАЖНО:
    - сохраняет все старые вызовы:
        engine.analyze(payload)
        engine.interpret(payload) (если где-то осталось)
    - но фактически использует новый Output Facade
    """

    def __init__(self):
        self._facade = MarketIntelligenceOutputFacade()

    def analyze(self, payload: Dict[str, Any]):
        """
        Новый единый pipeline выхода:
        returns MarketIntelligenceOutputContract
        """
        return self._facade.analyze(payload)

    def interpret(self, payload: Dict[str, Any]):
        """
        Backward compatibility слой для runtime/worker/bot
        """
        return self._facade.analyze(payload)
