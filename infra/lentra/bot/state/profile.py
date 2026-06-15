from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class UserProfile:
    user_id: int

    # интересы
    preferred_cities: List[str] = field(default_factory=list)

    # поведенческий сигнал
    viewed_items: List[str] = field(default_factory=list)
    clicked_items: List[str] = field(default_factory=list)

    # скоринг предпочтений
    feature_weights: Dict[str, float] = field(default_factory=lambda: {
        "pool": 0.2,
        "sea_view": 0.3,
        "price": 0.5
    })
