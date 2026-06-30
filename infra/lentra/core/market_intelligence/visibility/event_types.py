from enum import Enum


class EventType(str, Enum):
    DEDUP = "dedup_event"
    RISK = "risk_event"
    GEO = "geo_event"
    EXPAT = "expat_event"
    RANKING = "ranking_event"
