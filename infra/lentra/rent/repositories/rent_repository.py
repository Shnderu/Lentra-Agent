# ============================================================
# RENT REPOSITORY ADAPTER LAYER
# ============================================================

from lentra.rent.repository import RentRepository as _BaseRentRepository


class RentRepository(_BaseRentRepository):
    """
    Canonical rent repository adapter.

    Repository layer must not depend on delivery layers.

    Dependency direction:

        bot
          |
          v
        application
          |
          v
        rent.repository
    """

    pass
