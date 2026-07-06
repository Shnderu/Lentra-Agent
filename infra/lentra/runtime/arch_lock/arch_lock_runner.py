from lentra.runtime.arch_lock.governor import ArchGovernor


def run_arch_lock():
    print("[ARCH LOCK v1.6] scanning...")
    gov = ArchGovernor()
    gov.hard_gate()
    print("[ARCH LOCK v1.6] OK")


if __name__ == "__main__":
    run_arch_lock()
