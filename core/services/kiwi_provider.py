import requests
import logging
import os

class KiwiProvider:
    """TEQUILA Kiwi API (flight search)"""

    BASE_URL = "https://api.tequila.kiwi.com/v2/search"

    def __init__(self):
        self.api_key = os.getenv("KIWI_API_KEY")

    def search(self, from_code: str, to_code: str, date: str):
        if not self.api_key:
            logging.warning("KIWI API KEY NOT SET - fallback mode")
            return []

        headers = {"apikey": self.api_key}

        params = {
            "fly_from": from_code,
            "fly_to": to_code,
            "date_from": date,
            "date_to": date,
            "curr": "USD",
            "limit": 5
        }

        try:
            r = requests.get(self.BASE_URL, headers=headers, params=params, timeout=10)
            data = r.json()

            results = []

            for f in data.get("data", []):
                results.append({
                    "airline": f.get("airlines", ["unknown"])[0],
                    "price": f.get("price"),
                    "from": from_code,
                    "to": to_code,
                    "duration": f.get("duration", {}).get("total", 0) // 3600
                })

            return results

        except Exception as e:
            logging.error(f"KIWI ERROR: {e}")
            return []
