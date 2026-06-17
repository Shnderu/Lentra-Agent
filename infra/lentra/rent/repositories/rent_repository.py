# ============================================================
# RENT REPOSITORY ADAPTER LAYER
# ============================================================

from lentra.bot.features.rent_search.repository import RentRepository as _RealRentRepository


class RentRepository(_RealRentRepository):
    """
    Adapter layer to preserve legacy DI contracts.

    Keeps old architecture imports working while real logic
    lives in bot.features.rent_search.
    """

    pass
