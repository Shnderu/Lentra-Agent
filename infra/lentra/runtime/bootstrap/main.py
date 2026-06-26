"""
Runtime bootstrap Lentra
"""

# 1. СНАЧАЛА включаем архитектурный замок
from lentra.core.system_boundary import install_import_guard

install_import_guard()


# 2. дальше только чистый runtime
from lentra.worker.run import main as worker_main


def main():
    worker_main()


if __name__ == "__main__":
    main()
