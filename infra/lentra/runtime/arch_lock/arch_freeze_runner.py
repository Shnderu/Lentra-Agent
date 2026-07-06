from lentra.runtime.arch_lock.freezer import GraphFreezer


def run_freeze():
    freezer = GraphFreezer()

    snapshot = freezer.scan("/opt/lentra/infra/lentra")

    print("[ARCH FREEZE v1] snapshot size:", len(snapshot))

    # future: store hash in git or sqlite
    for k, v in list(snapshot.items())[:5]:
        print(k, "=>", v)


if __name__ == "__main__":
    run_freeze()
