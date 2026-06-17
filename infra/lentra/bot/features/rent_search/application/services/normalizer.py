import re
from lentra.bot.features.rent_search.contracts.rent_item import RentSearchItem


class RentNormalizer:

    def normalize_price(self, price: str):

        if not price:
            return None, None

        price = price.replace(",", "").strip()

        # THB
        if "THB" in price:
            value = re.findall(r"\d+", price)
            return (float(value[0]) if value else None, "THB")

        # VND
        if "VND" in price:
            value = re.findall(r"\d+", price)
            return (float(value[0]) if value else None, "VND")

        # USD
        if "$" in price:
            value = re.findall(r"\d+", price)
            return (float(value[0]) if value else None, "USD")

        return None, None

    def normalize(self, item: RentSearchItem, country: str) -> RentSearchItem:

        value, currency = self.normalize_price(item.price)

        item.price_value = value
        item.currency = currency
        item.country = country

        return item
