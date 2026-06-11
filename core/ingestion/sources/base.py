from abc import ABC, abstractmethod


class BaseSource(ABC):

    name: str

    @abstractmethod
    def search(self, payload: dict) -> list[dict]:
        pass
