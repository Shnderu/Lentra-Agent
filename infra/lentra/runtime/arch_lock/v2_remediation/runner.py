from lentra.runtime.arch_lock.firewall import Firewall
from lentra.runtime.arch_lock.v2_remediation.types import load_default_rules
import os


def run():
    print("[ARCH LOCK v2.2 remediation] starting...")

    rules = load_default_rules()

    fw = Firewall(rules=rules)

    project_root = "/opt/lentra/infra"

    # FIX: scan requires project_root
    result = fw.scan(project_root)

    print("[ARCH LOCK v2.2 remediation] result:", result)

    return result


if __name__ == "__main__":
    run()
