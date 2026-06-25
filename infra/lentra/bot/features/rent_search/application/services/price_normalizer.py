import re

from lentra.bot.features.rent_search.contracts import RentSearchItem


class PriceNormalizer:

    FX = {
        "USD": 1.0,
        "THB": 0.027,
        "VND": 0.000039,
    }

    def normalize(self, item: RentSearchItem) -> RentSearchItem:

        if not item.price:
            return item

        text = item.price.upper()

        currency = "USD"

        if "THB" in text:
            currency = "THB"

        elif "VND" in text:
            currency = "VND"

        match = re.search(r"([\d\.]+)", text)

        if not match:
            return item

        value = float(match.group(1))

        usd_value = value * self.FX.get(currency, 1.0)

        item.currency = currency
        item.price_value = usd_value

        return item
