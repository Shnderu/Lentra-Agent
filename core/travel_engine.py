class TravelEngine:
    def analyze_route(self, text: str):
        text = text.lower()

        if "moscow" in text and "paris" in text:
            return {
                "route": "MOW → PAR",
                "score": 0.82,
                "recommendation": "Possible fare drop window in 7–14 days"
            }

        if "dubai" in text:
            return {
                "route": "ANY → DXB",
                "score": 0.74,
                "recommendation": "High volatility route"
            }

        return {
            "route": "UNKNOWN",
            "score": 0.3,
            "recommendation": "Not enough data"
        }
