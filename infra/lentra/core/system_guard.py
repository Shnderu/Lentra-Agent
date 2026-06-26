class SystemGuard:
    """
    DISABLED CONTROL MODE

    Guards НЕ участвуют в execution decisioning
    """

    def validate(self, *args, **kwargs):
        return True
