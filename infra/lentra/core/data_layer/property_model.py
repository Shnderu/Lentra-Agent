from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Property:
    raw_query: str
    property_type: Optional[str] = None
    location: Optional[str] = None
    budget_max: Optional[int] = None


class PropertyExtractor:
    def extract(self, intent: Dict[str, Any], raw_query: str) -> Property:
        return Property(
            raw_query=raw_query,
            property_type=intent.get("type"),
            location=intent.get("location"),
            budget_max=intent.get("budget_max"),
        )


property_extractor = PropertyExtractor()
