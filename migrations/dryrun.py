import glob

def run():
    files = sorted(glob.glob("/app/migrations/*.up.sql"))

    print("[DRY RUN] migrations to apply:")

    for f in files:
        print(" -", f)

    print("[DRY RUN END]")


if __name__ == "__main__":
    run()
