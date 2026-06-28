
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PropertyObject:

    id: str | None = None

    title: str = ""

    price: float | None = None

    location: str | None = None

    source: str | None = None

    city: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)
