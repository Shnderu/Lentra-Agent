from typing import Dict, Optional


class GeoClassifier:
    """
    VIETNAM GEO CLASSIFIER V2

    Output:
    - country
    - region
    - city
    - district

    Deterministic rule-based classifier.
    """


    REGION_MAP = {
        "North": {
            "hanoi",
            "ha noi",
            "hai phong",
            "bac ninh",
            "ninh binh"
        },

        "Central": {
            "da nang",
            "hue",
            "hoi an",
            "nha trang"
        },

        "South": {
            "ho chi minh",
            "ho chi minh city",
            "hcm",
            "saigon",
            "can tho",
            "vung tau"
        }
    }


    DISTRICT_MAP = {

        "da nang": {
            "son tra",
            "my khe",
            "my an",
            "hai chau",
            "ngu hanh son",
            "cam le"
        },

        "ho chi minh": {
            "district 1",
            "district 2",
            "district 3",
            "binh thanh",
            "thao dien"
        },

        "hanoi": {
            "tay ho",
            "ba dinh",
            "cau giay",
            "dong da"
        }
    }


    def classify(
        self,
        raw_location: str
    ) -> Dict[str, Optional[str]]:

        if not raw_location:
            return self._empty()


        text = raw_location.lower()


        return {

            "country": "Vietnam",

            "region":
                self._detect_region(text),

            "city":
                self._detect_city(text),

            "district":
                self._detect_district(text)
        }



    def _detect_region(
        self,
        text: str
    ) -> Optional[str]:

        for region, keywords in self.REGION_MAP.items():

            for keyword in keywords:

                if keyword in text:
                    return region

        return None



    def _detect_city(
        self,
        text: str
    ) -> Optional[str]:

        for keywords in self.REGION_MAP.values():

            for city in keywords:

                if city in text:
                    return city.title()

        return None



    def _detect_district(
        self,
        text: str
    ) -> Optional[str]:

        for city, districts in self.DISTRICT_MAP.items():

            for district in districts:

                if district in text:
                    return district.title()

        return None



    def _empty(self):

        return {

            "country": "Vietnam",

            "region": None,

            "city": None,

            "district": None
        }
