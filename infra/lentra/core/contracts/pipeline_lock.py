from lentra.core.seal.system_seal import SystemSeal


class PipelineLock:
    _locked = False

    @classmethod
    def lock(cls):
        cls._locked = True
        SystemSeal.seal()

    @classmethod
    def assert_locked(cls):
        if not cls._locked:
            raise RuntimeError("[PIPELINE NOT LOCKED] unsafe state")

    @classmethod
    def is_locked(cls):
        return cls._locked
