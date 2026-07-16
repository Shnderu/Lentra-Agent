from lentra.core.market_intelligence.contracts.market_object_contract import MarketObjectContract


class MarketObjectBuilder:

    def build(self, data: dict) -> MarketObjectContract:

        location = data.get("location", {})

        if isinstance(location, str):
            location = {
                "segment": location,
                "micro_market": "unknown"
            }

        return MarketObjectContract(
            price=float(data.get("price", 0)),
            location=location,
            risk=float(data.get("risk", 0.5)),
            confidence=float(data.get("confidence", 0.5)),
            market_price=float(data.get("market_price", 0)),
            deviation=float(data.get("deviation", 0)),
            features={},
            signals={}
        )
