from lentra.application.rent_search.service import (
    RentSearchApplicationService
)


class RentSearchService:
    """
    Delivery layer adapter.

    Bot feature must not own business workflow.
    Delegates execution to application layer.
    """

    def __init__(self, connector):

        self.application = RentSearchApplicationService(
            connector
        )


    async def search(
        self,
        payload: dict
    ):

        return await self.application.search(
            payload
        )
