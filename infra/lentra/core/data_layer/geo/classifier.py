from typing import Dict, Optional


class GeoClassifier:
    """
    VIETNAM GEO CLASSIFIER V3

    Canonical output:

    country
    region
    city
    district

    All values are normalized:
    lowercase
    underscore separated

    Example:

    Da Nang
    da_nang

    My Khe
    my_khe
    """


    REGION_MAP = {

        "north": {
            "hanoi",
            "ha noi",
            "hai phong",
            "bac ninh",
            "ninh binh",
        },

        "central": {
            "da nang",
            "danang",
            "hue",
            "hoi an",
            "nha trang",
        },

        "south": {
            "ho chi minh",
            "hcm",
            "saigon",
            "can tho",
            "vung tau",
        }
    }


    DISTRICT_MAP = {

        "da_nang": {
            "son tra",
            "my khe",
            "my khe beach",
            "my an",
            "an thuong",
            "hai chau",
            "ngu hanh son",
            "cam le",
            "center",
            "da nang center",
            "han river"
        },

        "ho_chi_minh": {
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


        text = (
            raw_location
            .lower()
            .replace("-", " ")
        )


        city = self._detect_city(
            text
        )


        district = self._detect_district(
            text,
            city
        )


        if city is None and district:

            city = self._detect_city_by_district(
                district
            )


        return {

            "country": "vietnam",

            "region": self._detect_region(
                text
            ),

            "city": city,

            "district": district

        }



    def _normalize(
        self,
        value: str
    ) -> str:

        return (
            value
            .lower()
            .strip()
            .replace(" ", "_")
        )



    def _detect_region(
        self,
        text: str
    ) -> Optional[str]:

        for region, cities in self.REGION_MAP.items():

            for city in cities:

                if city in text:

                    return region

        return None



    def _detect_city(
        self,
        text: str
    ) -> Optional[str]:

        for cities in self.REGION_MAP.values():

            for city in cities:

                if city in text:

                    return self._normalize(
                        city
                    )

        return None



    def _detect_district(
        self,
        text: str,
        city: Optional[str]
    ) -> Optional[str]:


        if city:

            districts = self.DISTRICT_MAP.get(
                city,
                set()
            )

            for district in districts:

                if district in text:

                    return self._normalize(
                        district
                    )


        for districts in self.DISTRICT_MAP.values():

            for district in districts:

                if district in text:

                    return self._normalize(
                        district
                    )


        return None





    def _detect_city_by_district(
        self,
        district: str
    ) -> Optional[str]:

        for city, districts in self.DISTRICT_MAP.items():

            if district in [
                self._normalize(x)
                for x in districts
            ]:

                return city

        return None


    def _empty(self):

        return {

            "country": "vietnam",

            "region": None,

            "city": None,

            "district": None

        }
