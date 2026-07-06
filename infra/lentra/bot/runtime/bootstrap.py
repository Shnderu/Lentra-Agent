from lentra.runtime.bootstrap_guard import enforce_bootstrap


def main():
    enforce_bootstrap()

    print("[BOT] locked bootstrap OK")

    import time
    while True:
        time.sleep(5)


if __name__ == "__main__":
    main()
