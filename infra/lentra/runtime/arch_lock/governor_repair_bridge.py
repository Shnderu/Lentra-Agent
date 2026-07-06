from lentra.runtime.arch_lock.self_repair_engine import SelfRepairEngine
from lentra.runtime.arch_lock.arch_lock_runner import run_arch_lock


class GovernorRepairBridge:
    """
    Bridges enforcement (ARCH LOCK) with repair planning.
    """

    def __init__(self):
        self.repair = SelfRepairEngine()

    def run_diagnostics(self):
        try:
            run_arch_lock()
            return {"status": "ok", "violations": []}
        except Exception as e:
            return {
                "status": "violation",
                "error": str(e)
            }

    def propose_fix(self, file_path: str, issue: str):
        return self.repair.generate_patch_plan(file_path, issue)
