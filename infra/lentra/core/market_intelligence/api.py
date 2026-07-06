"""
CORE MARKET INTELLIGENCE API

RULE:
- pure logic only
- no runtime imports
- no enforcement calls
"""

class MarketIntelligenceAPI:

    def calculate_price(self, data: dict):
        return {"price": data.get("price", 0)}

    def calculate_risk(self, data: dict):
        return {"risk": 0.5}

    def rank(self, items: list):
        return sorted(items, key=lambda x: x.get("score", 0), reverse=True)
