from lentra.runtime.arch_lock.v2_policy_engine import PolicyEngine
from lentra.runtime.arch_lock.v2_remediation.engine import RemediationEngine

def main():
    policy = PolicyEngine()
    engine = RemediationEngine()

    violations = policy.scan()

    print(f"[ARCH LOCK v2] violations: {len(violations)}")

    if not violations:
        print("[ARCH LOCK v2] OK")
        return

    for v in violations:
        print(engine.explain(v))

        patch = engine.propose_patch(v)
        print(f"[PATCH PROPOSED] {patch}")

    # IMPORTANT: no auto apply in v2 baseline
    print("[ARCH LOCK v2] remediation mode: PROPOSE ONLY")

if __name__ == "__main__":
    main()
