from typing import Protocol


class RentSearchPort(Protocol):
    """
    Delivery port for rent search.

    Bot layer depends only on this contract.
    """

    async def search(
        self,
        payload: dict
    ) -> dict:
        ...
