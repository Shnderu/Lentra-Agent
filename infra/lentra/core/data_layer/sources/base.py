class BaseSource:
    """
    Core abstraction for all data sources in Lentra Data Layer MVP
    """

    def fetch(self):
        """
        Should return list[dict] of raw listings
        """
        raise NotImplementedError("fetch() must be implemented by source")
