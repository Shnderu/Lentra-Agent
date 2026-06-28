
from lentra.core.market_intelligence.models.market_object import MarketObject


class ViewModelMapper:

    def build_card(self, obj: MarketObject) -> dict:

        risk = obj.risk if obj.risk is not None else 0.5

        return {
            "id": obj.id,
            "price": obj.market_price,
            "range": self._range(obj.market_price),
            "badges": self._badges(risk),
            "ui_state": self._ui_state(risk),
            "title": self._title(obj),
            "subtitle": self._subtitle(obj),
            "explanation": f"risk {risk:.2f}",
            "negotiation": obj.negotiation or None,
            "target_discount": self._discount(obj)
        }

    def _range(self, price):

        if not price:
            return None

        return {
            "min": price * 0.9,
            "max": price * 1.1
        }

    def _badges(self, risk):

        if risk < 0.3:
            return ["low_risk"]
        if risk < 0.7:
            return ["medium_risk"]
        return ["high_risk"]

    def _ui_state(self, risk):

        if risk < 0.3:
            return "green"
        if risk < 0.7:
            return "yellow"
        return "red"

    def _title(self, obj):

        if obj.listings:
            return obj.listings[0].title

        return "Property"

    def _subtitle(self, obj):

        sources = {l.source for l in obj.listings}

        return "sources: " + ",".join(list(sources))

    def _discount(self, obj):

        if obj.market_price is None:
            return 0.03

        deviation = obj.price_deviation or 0

        return max(0.01, min(0.1, 0.03 + abs(deviation)))
