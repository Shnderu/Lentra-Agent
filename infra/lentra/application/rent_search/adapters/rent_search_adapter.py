from lentra.application.rent_search.service import (
    RentSearchApplicationService
)


class RentSearchAdapter:
    """
    Application boundary adapter.

    Implements bot delivery port.
    """

    def __init__(self, connector=None):

        self.service = RentSearchApplicationService(
            connector
        )


    async def search(
        self,
        payload: dict
    ):

        return await self.service.search(
            payload
        )
