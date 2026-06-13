# ============================================================
# LENTRA CONNECTOR BASE V16.2
# ============================================================

from typing import Dict, Any, List
from abc import ABC, abstractmethod


class BaseConnector(ABC):
    name: str

    @abstractmethod
    async def fetch(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Must return RAW listings (NOT normalized)
        """
        pass
