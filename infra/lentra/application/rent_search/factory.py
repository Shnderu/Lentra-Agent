from lentra.application.rent_search.adapters.rent_search_adapter import (
    RentSearchAdapter
)


def build_rent_search_adapter(connector=None):

    return RentSearchAdapter(
        connector
    )
