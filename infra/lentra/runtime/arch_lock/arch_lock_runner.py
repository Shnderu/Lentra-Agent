import os
import sys
from lentra.runtime.arch_lock.firewall import ImportFirewall
from lentra.runtime.dag_check import main as dag_main


def log(msg: str):
    print(msg, flush=True)


def run_arch_lock():
    log("[ARCH LOCK v1] scanning...")

    fw = ImportFirewall()

    base_path = "/opt/lentra/infra/lentra"

    for root, _, files in os.walk(base_path):
        for f in files:
            if f.endswith(".py"):
                fw.scan_file(os.path.join(root, f))

    log("[ARCH LOCK v1] DAG check...")
    dag_main()

    log("[ARCH LOCK v1] OK - system locked")


if __name__ == "__main__":
    run_arch_lock()
