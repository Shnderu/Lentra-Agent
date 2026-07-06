from lentra.runtime.arch_lock.firewall import Firewall
from lentra.runtime.arch_lock.policy_engine import PolicyEngine


class ArchGovernor:
    """
    ARCH LOCK v1.6 Governor
    single decision point
    """

    def __init__(self):
        self.rules = [
            ("lentra.core", "lentra.runtime.intelligence_gateway"),
            ("lentra.core.market_intelligence", "lentra.runtime"),
            ("lentra.runtime", "lentra.core.bootstrap"),
        ]

        self.firewall = Firewall(self.rules)
        self.policy = PolicyEngine([])

    def hard_gate(self, project_root="/opt/lentra/infra"):
        violations = self.firewall.scan(project_root)
        result = self.policy.evaluate(violations)

        print("[GOVERNOR] result:", result)

        if result["status"] != "OK":
            raise RuntimeError("[ARCH LOCK v1.6] BLOCKED")

        return result
