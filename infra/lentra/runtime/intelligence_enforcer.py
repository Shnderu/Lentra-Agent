from lentra.core.market_intelligence.output.facade import MarketIntelligenceOutputFacade

_facade = MarketIntelligenceOutputFacade()


def interpret(payload: dict):
    return _facade.analyze(payload)
