from typing import Any, Dict


class ListingAdapter:
    """
    Унифицирует входные данные:
    - dict
    - dataclass Listing
    - raw string (fallback)
    """

    @staticmethod
    def normalize(item: Any) -> Dict[str, Any]:
        # CASE 1: already dict
        if isinstance(item, dict):
            return item

        # CASE 2: dataclass / object with attributes
        if hasattr(item, "__dict__"):
            return vars(item)

        # CASE 3: string fallback
        if isinstance(item, str):
            return {
                "raw": item,
                "title": item,
                "location": "",
                "price": 0
            }

        # CASE 4: unknown type hard fallback
        return {
            "raw": str(item),
            "title": str(item),
            "location": "",
            "price": 0
        }
