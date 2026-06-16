from enum import Enum


class Intent(str, Enum):
    SEARCH = "search"
    DETAIL = "detail"
    NEXT_PAGE = "next_page"
    PREV_PAGE = "prev_page"
    FILTER = "filter"
    BACK = "back"
    UNKNOWN = "unknown"
