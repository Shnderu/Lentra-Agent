from lentra.runtime.bootstrap_guard import enforce_bootstrap


def main():
    enforce_bootstrap()

    print("[RUNTIME] execution kernel started")

    # runtime MUST NOT import API
    # API is external ingress layer only

    import time
    while True:
        time.sleep(5)


if __name__ == "__main__":
    main()
