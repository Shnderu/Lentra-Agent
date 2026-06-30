from lentra.services.intelligence_gateway import IntelligenceGateway


class StreamProcessor:

    def __init__(self):
        self.gateway = IntelligenceGateway()

    def process(self, listings):
        return self.gateway.execute(listings, source="stream")
