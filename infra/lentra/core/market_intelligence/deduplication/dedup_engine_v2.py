from typing import List, Dict


class DedupEngineV2:

    def process(self, listings: List[Dict]) -> List[Dict]:

        seen = set()
        result = []

        for l in listings:

            key = (
                l.get("price"),
                str(l.get("location")),
                l.get("market_price")
            )

            if key in seen:
                continue

            seen.add(key)
            result.append(l)

        return result
