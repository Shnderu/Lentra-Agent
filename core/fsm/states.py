
from enum import Enum


class FSMState(str, Enum):

    IDLE = "idle"

    # route flow
    ROUTE_FROM = "route_from"
    ROUTE_TO = "route_to"
    ROUTE_DATE = "route_date"

    # watch flow
    WATCH_FROM = "watch_from"
    WATCH_TO = "watch_to"
    WATCH_PRICE = "watch_price"

    # planner
    PLANNER_INPUT = "planner_input"
