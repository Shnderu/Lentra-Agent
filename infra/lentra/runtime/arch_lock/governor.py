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

        # Phase 3 (ADR_ARCH_LOCK_RULE_MIGRATION_V1): declarative rules from
        # rules_v1.json + v2_rules are evaluated in DRY-RUN, log-only mode.
        # The gate verdict above is final; dry_run() never raises and never
        # changes the exit code until Phase 4 approval.
        try:
            from lentra.runtime.arch_lock.rule_loader import dry_run
            dry_run(project_root)
        except Exception as e:
            print("[GOVERNOR] rule dry-run unavailable (non-blocking):", repr(e))

        return result
