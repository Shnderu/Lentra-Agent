from enum import Enum


class LayerType(str, Enum):
    API = "api"
    BOT = "bot"
    SERVICE = "service"
    DOMAIN = "domain"
    DATA = "data"
    INFRASTRUCTURE = "infrastructure"
