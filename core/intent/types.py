from dataclasses import dataclass


@dataclass
class Intent:
    name: str
    confidence: float = 1.0
