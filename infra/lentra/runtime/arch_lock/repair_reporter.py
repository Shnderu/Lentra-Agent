from lentra.runtime.arch_lock.governor_repair_bridge import GovernorRepairBridge


def main():
    bridge = GovernorRepairBridge()

    result = bridge.run_diagnostics()

    print("[REPAIR REPORT] status:", result["status"])

    if result["status"] != "ok":
        print("[REPAIR REPORT] system has violations")
    else:
        print("[REPAIR REPORT] system clean - no repair needed")


if __name__ == "__main__":
    main()
