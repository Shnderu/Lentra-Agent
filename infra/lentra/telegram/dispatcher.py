from lentra.core.market_intelligence.build import build_intelligence_gateway


def get_gateway():
    return build_intelligence_gateway()


class Dispatcher:
    def __init__(self):
        self.gateway = get_gateway()
