class SystemSeal:
    """
    Locks architecture after runtime bootstrap.
    Prevents structural mutation at runtime.
    """

    _sealed = False

    @classmethod
    def seal(cls):
        cls._sealed = True

    @classmethod
    def is_sealed(cls):
        return cls._sealed

    @classmethod
    def assert_not_sealed(cls):
        if cls._sealed:
            raise RuntimeError("[SYSTEM SEALED] mutation not allowed")
