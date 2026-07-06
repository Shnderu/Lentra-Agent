from lentra.runtime.arch_lock.arch_state_engine import ArchStateEngine
from lentra.runtime.arch_lock.seal_engine import SealEngine


class GovernorEvolutionBridge:
    """
    Connects runtime enforcement with evolution tracking.
    """

    def __init__(self):
        self.state = ArchStateEngine()
        self.seal = SealEngine()

    def capture_and_version(self, snapshot):
        version = self.state.create_version(snapshot)
        print("[EVOLUTION] new version:", version)

        return version

    def full_cycle(self):
        snapshot = self.seal.build_snapshot()
        return self.capture_and_version(snapshot)
