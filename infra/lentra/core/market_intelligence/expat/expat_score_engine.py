import json
from pathlib import Path
from typing import Dict, Any


class ExpatScoreEngine:
    """
    Market Intelligence Area Context Engine v3.

    Responsibility:
    - area intelligence
    - expat suitability
    - district context

    Profiles loaded from Data Layer.
    """


    def __init__(self):

        self.area_profiles = self._load_profiles()



    def _load_profiles(self):

        path = Path(
            "lentra/data/geo/vietnam_area_profiles.json"
        )

        if not path.exists():

            return {}

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def _normalize_location(
        self,
        location: Any
    ) -> Dict[str, Any]:

        if isinstance(location, dict):

            return location


        if isinstance(location, str):

            return {
                "segment": location.lower(),
                "micro_market": location.lower()
            }


        return {}



    def _find_profile(
        self,
        location: Dict[str, Any]
    ) -> Dict[str, float]:

        city = str(
            location.get(
                "city",
                ""
            )
        ).lower()


        district = str(
            location.get(
                "district",
                ""
            )
        ).lower()


        city_profiles = self.area_profiles.get(
            city,
            {}
        )


        profile = city_profiles.get(
            district
        )


        if profile:

            return profile


        return {

            "internet_score": 5.0,
            "expat_score": 5.0,
            "noise_score": 5.0,
            "safety_score": 5.0,
            "infrastructure_score": 5.0,

        }



    def score(
        self,
        listing: dict
    ):

        location = self._normalize_location(
            listing.get(
                "location",
                {}
            )
        )


        profile = self._find_profile(
            location
        )


        area_score = round(
            (
                profile["internet_score"]
                +
                profile["expat_score"]
                +
                profile["safety_score"]
                +
                profile["infrastructure_score"]
                -
                profile["noise_score"]
            )
            /
            4.0,

            2
        )


        return {

            **profile,

            "area_score": min(
                area_score / 10,
                1.0
            ),

            "location": location

        }



    def evaluate(
        self,
        payload: dict
    ):

        return self.score(
            payload
        )
