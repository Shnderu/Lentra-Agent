from lentra.services.intelligence_gateway import IntelligenceGateway

gateway = IntelligenceGateway()


class TelegramRuntime:

    def process(self, listings, text=None):
        return gateway.execute(
            listings=listings,
            query_text=text,
            source="telegram"
        )
