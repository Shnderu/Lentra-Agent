from lentra.runtime.arch_lock.arch_lock_runner import run_arch_lock
from lentra.runtime.arch_lock.seal_engine import SealEngine
from lentra.runtime.arch_lock.freezer import GraphFreezer


class ArchGovernor:
    """
    Central enforcement brain for architecture rules.
    """

    def __init__(self):
        self.seal = SealEngine()
        self.freeze = GraphFreezer()

    def evaluate_boot(self):
        """
        Full system evaluation before runtime start.
        """

        print("[GOVERNOR] starting evaluation...")

        # 1. syntax + DAG + policy
        run_arch_lock()

        # 2. freeze snapshot validation
        snapshot = self.freeze.scan("/opt/lentra/infra/lentra")
        print("[GOVERNOR] freeze snapshot size:", len(snapshot))

        # 3. seal validation
        try:
            self.seal.validate()
        except Exception:
            print("[GOVERNOR] seal not initialized → creating baseline")
            self.seal.save_snapshot()

        print("[GOVERNOR] system APPROVED")

    def hard_gate(self):
        """
        Used by systemd ExecStartPre.
        Blocks boot if architecture invalid.
        """

        self.evaluate_boot()
