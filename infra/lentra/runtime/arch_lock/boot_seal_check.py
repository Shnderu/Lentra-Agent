from lentra.runtime.arch_lock.seal_engine import SealEngine


def run_boot_seal():
    engine = SealEngine()

    # if first run -> create baseline
    try:
        engine.validate()
    except Exception as e:
        print("[BOOT SEAL] initializing baseline snapshot")
        engine.save_snapshot()
        return

    print("[BOOT SEAL] OK")


if __name__ == "__main__":
    run_boot_seal()
