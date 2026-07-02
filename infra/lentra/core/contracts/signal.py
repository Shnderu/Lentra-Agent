from enum import Enum


class Signal(Enum):
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    HOLD = "hold"
    RISK = "risk"
    DUPLICATE = "duplicate"
    UNKNOWN = "unknown"
