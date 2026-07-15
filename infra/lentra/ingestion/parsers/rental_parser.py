import re
from typing import Dict, Any


class RentalParser:
    """
    Rental parser V3

    Extracts normalized rental property data.
    """

    CITY_KEYWORDS = {
        "da nang": "da_nang",
        "danang": "da_nang",
        "bangkok": "bangkok",
        "bali": "bali",
        "chiang mai": "chiang_mai",
    }

    DISTRICT_KEYWORDS = {
        "my an": "my_an",
        "son tra": "son_tra",
        "sơn trà": "son_tra",
        "hoi hai": "hoi_hai",
        "ngu hanh son": "ngu_hanh_son",
    }

    TYPE_KEYWORDS = {
        "studio": "studio",
        "apartment": "apartment",
        "condo": "condo",
        "room": "room",
        "1 bedroom": "apartment",
        "2 bedroom": "apartment",
    }


    def parse(self, text: str) -> Dict[str, Any]:

        lower = text.lower()


        price_vnd_mln = None
        price_usd = None


        usd = re.search(
            r'(\d{2,5})\s*\$',
            lower
        )

        if usd:
            price_usd = int(usd.group(1))


        vnd = re.search(
            r'(\d+(?:\.\d+)?)\s*(?:млн|million|triệu|trieu|m)',
            lower
        )

        if vnd:
            price_vnd_mln = float(vnd.group(1))


        city = None

        for k, v in self.CITY_KEYWORDS.items():
            if k in lower:
                city = v
                break


        district = None

        for k, v in self.DISTRICT_KEYWORDS.items():
            if k in lower:
                district = v
                break


        property_type = None

        for k, v in self.TYPE_KEYWORDS.items():
            if k in lower:
                property_type = v
                break


        bedrooms = None

        bed = re.search(
            r'(\d+)\s*[- ]*bed',
            lower
        )

        if bed:
            bedrooms = int(bed.group(1))

        elif "studio" in lower:
            bedrooms = 0


        bathrooms = None

        bath = re.search(
            r'(\d+)\s*bath',
            lower
        )

        if bath:
            bathrooms = int(bath.group(1))


        area_m2 = None

        area = re.search(
            r'(\d+(?:\.\d+)?)\s*(?:m2|m²|sqm)',
            lower
        )

        if area:
            area_m2 = float(area.group(1))


        floor = None

        floor_match = re.search(
            r'(\d+)\s*floor',
            lower
        )

        if floor_match:
            floor = int(floor_match.group(1))


        total_floors = None

        total_floor_match = re.search(
            r'(\d+)\s*(?:floors|storey)',
            lower
        )

        if total_floor_match:
            total_floors = int(total_floor_match.group(1))


        pool = any(
            x in lower
            for x in [
                "pool",
                "swimming",
                "бассейн"
            ]
        )


        sea_view = any(
            x in lower
            for x in [
                "sea view",
                "ocean view",
                "вид на море"
            ]
        )


        pet_friendly = any(
            x in lower
            for x in [
                "pet",
                "pets",
                "кош",
                "собак",
                "животн"
            ]
        )


        balcony = "balcony" in lower or "балкон" in lower

        parking = any(
            x in lower
            for x in [
                "parking",
                "парковка",
                "garage"
            ]
        )

        furnished = any(
            x in lower
            for x in [
                "furnished",
                "мебель",
                "меблирован"
            ]
        )

        washing_machine = any(
            x in lower
            for x in [
                "washing machine",
                "washer",
                "стирал"
            ]
        )

        air_conditioner = any(
            x in lower
            for x in [
                "air conditioner",
                "aircon",
                "кондиционер"
            ]
        )

        kitchen = any(
            x in lower
            for x in [
                "kitchen",
                "кухн"
            ]
        )

        refrigerator = any(
            x in lower
            for x in [
                "refrigerator",
                "fridge",
                "холодиль"
            ]
        )

        wifi = any(
            x in lower
            for x in [
                "wifi",
                "wi-fi",
                "internet",
                "интернет"
            ]
        )


        deposit = None

        if "100%" in lower:
            deposit = 1.0
        elif "50%" in lower:
            deposit = 0.5


        electricity_price = None

        electricity = re.search(
            r'(\d+(?:\.\d+)?)\s*(?:квт|kw|kwh)',
            lower
        )

        if electricity:
            electricity_price = float(
                electricity.group(1)
            )


        water_price = None

        water = re.search(
            r'вода\s*(\d+(?:\.\d+)?)',
            lower
        )

        if water:
            water_price = float(
                water.group(1)
            )


        features = {
            "pool": pool,
            "sea_view": sea_view,
            "pet_friendly": pet_friendly,
            "balcony": balcony,
            "parking": parking,
            "furnished": furnished,
            "washing_machine": washing_machine,
            "air_conditioner": air_conditioner,
            "kitchen": kitchen,
            "refrigerator": refrigerator,
            "wifi": wifi,
        }


        return {
            "raw": text,
            "price_vnd_mln": price_vnd_mln,
            "price_usd": price_usd,
            "city": city,
            "district": district,
            "type": property_type,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,

            "area_m2": area_m2,
            "floor": floor,
            "total_floors": total_floors,

            "pool": pool,
            "sea_view": sea_view,
            "pet_friendly": pet_friendly,

            "balcony": balcony,
            "parking": parking,
            "furnished": furnished,
            "washing_machine": washing_machine,
            "air_conditioner": air_conditioner,
            "kitchen": kitchen,
            "refrigerator": refrigerator,
            "wifi": wifi,
            "internet": wifi,

            "deposit": deposit,
            "electricity_price": electricity_price,
            "water_price": water_price,

            "features": features,
        }
