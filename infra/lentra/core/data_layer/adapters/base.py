from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseAdapter(ABC):
    """
    CONTRACT FOR ALL DATA SOURCES
    """

    @abstractmethod
    def fetch(self) -> List[Dict[str, Any]]:
        """
        Returns RAW listings (unprocessed)
        """
        pass
