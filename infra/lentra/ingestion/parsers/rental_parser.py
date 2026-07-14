import re
from typing import Dict, Any


class RentalParser:
    """
    MVP parser для аренды жилья.

    Извлекает:
    - цену
    - район
    - город
    - тип жилья

    Normalization Layer v1
    """

    CITY_KEYWORDS = {
        "da nang": "da_nang",
        "da nang": "da_nang",
        "danang": "da_nang",
        "bangkok": "bangkok",
        "bali": "bali",
        "chiang mai": "chiang_mai",
    }

    DISTRICT_KEYWORDS = {
        "my an": "my_an",
        "son tra": "son_tra",
        "hoi hai": "hoi_hai",
        "ngu hanh son": "ngu_hanh_son",
        "an thuong": "an_thuong",
    }

    TYPE_KEYWORDS = {
        "studio": "studio",
        "apartment": "apartment",
        "condo": "condo",
        "room": "room",
    }


    def parse(self, text: str) -> Dict[str, Any]:

        lower_text = text.lower()


        # -------------------------
        # PRICE
        # -------------------------

        price_vnd_mln = None


        # 7 млн
        mln_match = re.search(
            r'(\d+(?:[.,]\d+)?)\s*(?:млн|million|m)',
            lower_text
        )

        if mln_match:
            price_vnd_mln = float(
                mln_match.group(1).replace(",", ".")
            )


        # fallback USD
        usd_match = re.search(
            r'(\d{2,5})\s*\$',
            lower_text
        )

        price_usd = None

        if usd_match:
            price_usd = int(
                usd_match.group(1)
            )


        # -------------------------
        # CITY
        # -------------------------

        city = None

        for key, value in self.CITY_KEYWORDS.items():

            if key in lower_text:
                city = value
                break


        # Telegram Da Nang канал
        if city is None:
            city = "da_nang"


        # -------------------------
        # DISTRICT
        # -------------------------

        district = None

        for key, value in self.DISTRICT_KEYWORDS.items():

            if key in lower_text:
                district = value
                break


        # -------------------------
        # TYPE
        # -------------------------

        property_type = None

        for key, value in self.TYPE_KEYWORDS.items():

            if key in lower_text:
                property_type = value
                break


        return {

            "raw": text,

            "price_vnd_mln": price_vnd_mln,

            "price_usd": price_usd,

            "city": city,

            "district": district,

            "type": property_type,
        }
