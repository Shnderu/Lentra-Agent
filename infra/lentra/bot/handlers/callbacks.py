from __future__ import annotations

from aiogram import Router
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lentra.bot.core.container import Container


def build_callback_router(container: "Container") -> Router:
    router = Router()

    # SAFE ACCESS: prevent crash on partial init / wrong container state
    renderer = getattr(container, "renderer", None)

    if renderer is None:
        # fallback to no-op renderer instead of crash
        from lentra.bot.core.container import NullRenderer
        renderer = NullRenderer()

    # дальше весь код работает через renderer безопасно
    router["renderer"] = renderer  # если используется DI через router state

    return router
