import logging

logger = logging.getLogger(__name__)


def safe_event_bus_error(e: Exception):
    logger.error("[EVENT BUS ERROR] %s", str(e))
