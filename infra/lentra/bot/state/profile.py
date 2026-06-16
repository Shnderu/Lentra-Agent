from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class UserProfile:
    user_id: int

    preferred_cities: List[str] = field(default_factory=list)

    viewed_items: List[str] = field(default_factory=list)
    clicked_items: List[str] = field(default_factory=list)
    saved_items: List[str] = field(default_factory=list)

    # FEATURE WEIGHTS (learned signals)
    feature_weights: Dict[str, float] = field(default_factory=lambda: {
        "price": 0.4,
        "score": 0.4,
        "distance": 0.2
    })

    # implicit preferences
    preference_bias: Dict[str, float] = field(default_factory=dict)
