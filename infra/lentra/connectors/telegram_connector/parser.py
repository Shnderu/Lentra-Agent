import re


class TelegramPropertyParser:

    @staticmethod
    def parse(text: str):

        result = {
            "price": None,
            "deposit": None,
            "area_m2": None,
            "bedrooms": None,
            "bathrooms": None,
            "pet_friendly": False,
            "pool": False,
            "sea_view": False,
        }

        price_match = re.search(
            r'(\d+(?:\.\d+)?)\s*млн\s*VND/месяц',
            text,
            re.IGNORECASE
        )

        if price_match:
            result["price"] = float(price_match.group(1))

        deposit_match = re.search(
            r'Депозит:\s*(\d+(?:\.\d+)?)',
            text,
            re.IGNORECASE
        )

        if deposit_match:
            result["deposit"] = float(deposit_match.group(1))

        area_match = re.search(
            r'(\d+(?:\.\d+)?)\s*кв/м',
            text,
            re.IGNORECASE
        )

        if area_match:
            result["area_m2"] = float(area_match.group(1))

        room_match = re.search(
            r'(\d+)\+1',
            text
        )

        if room_match:
            result["bedrooms"] = int(room_match.group(1))

        if "2 санузла" in text:
            result["bathrooms"] = 2

        if "питомц" in text.lower():
            result["pet_friendly"] = True

        if "бассейн" in text.lower():
            result["pool"] = True

        if "вид на море" in text.lower():
            result["sea_view"] = True

        return result
