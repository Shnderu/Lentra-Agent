# ============================================================
# LENTRA BOT MAIN (SAFE DI FIX)
# ============================================================

import asyncio

from lentra.core.safety.ast_guard import install_import_guard
from lentra.bot.handlers.router_builder import build_main_router
from lentra.bot.core.container import build_container


def main():
    # SAFE MODE INIT
    install_import_guard()

    # DI CONTAINER
    container = build_container()

    # ROUTER BUILD (FIXED CONTRACT)
    router = build_main_router(container)

    # BOOT LOG
    print("[BOOT] ENTER MAIN")
    print("[BOOT] BOT + DP CREATED")
    print("[BOOT] ROUTER BUILT")
    print("[BOOT] ROUTER INCLUDED")

    # START BOT
    asyncio.run(container.bot.run(router))


if __name__ == "__main__":
    main()
