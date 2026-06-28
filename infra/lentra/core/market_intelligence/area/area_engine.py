

class AreaEngine:

    def score(self, location: str):

        # базовые эвристики (позже заменим на geo+data layer)

        if not location:
            return {
                "area_score": 5.0,
                "internet": 5.0,
                "noise": 5.0,
                "expat_density": 5.0
            }

        if "My Khe" in location or "beach" in location.lower():
            return {
                "area_score": 8.5,
                "internet": 9.0,
                "noise": 6.0,
                "expat_density": 8.0
            }

        if "center" in location.lower():
            return {
                "area_score": 7.0,
                "internet": 8.0,
                "noise": 4.5,
                "expat_density": 7.5
            }

        return {
            "area_score": 6.0,
            "internet": 6.0,
            "noise": 6.0,
            "expat_density": 6.0
        }
