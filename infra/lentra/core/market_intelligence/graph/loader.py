import logging

logger = logging.getLogger(__name__)


def warn_graph_disabled(e: Exception):
    logger.warning("[GRAPH][WARN] disabled due to: %s", str(e))
