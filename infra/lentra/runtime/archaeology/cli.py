from .engine import ArchaeologyEngine
from .runtime_trace import RuntimeTrace



if __name__ == "__main__":


    report = ArchaeologyEngine(
        "."
    ).run()


    print()

    print(
        "=== Archaeology Report ==="
    )


    print(
        "Total:",
        report["total_files"]
    )


    print(
        "Reachable:",
        report["reachable"]
    )


    print(
        "Dead candidates:",
        report["dead_candidates"]
    )


    print()

    print(
        "=== Domain Map ==="
    )


    for key,value in report["domains"].items():

        print(
            key.upper(),
            ":",
            len(value)
        )


    print()

    print(
        "=== Runtime Trace ==="
    )


    trace = RuntimeTrace(".").run()


    targets = [
        "search_pipeline",
        "gateway_v3",
        "decision",
        "ranking",
        "risk_engine",
        "dedup_engine"
    ]


    for item in trace:

        text = (
            item["file"]
            +
            " "
            +
            " ".join(
                item["imports"]
            )
        ).lower()


        if any(
            t in text
            for t in targets
        ):

            print(
                item["file"]
            )

            for imp in item["imports"]:

                if any(
                    t in imp.lower()
                    for t in targets
                ):

                    print(
                        "  ->",
                        imp
                    )
