from enum import Enum


class TaskType(str, Enum):
    RENT_SEARCH = "rent.search"
    RENT_DETAILS = "rent.details"
    RENT_COMPARE = "rent.compare"
