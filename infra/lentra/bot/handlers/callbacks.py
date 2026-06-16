from __future__ import annotations

from aiogram import Router
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lentra.bot.core.container import Container


def build_callback_router(container: "Container") -> Router:
    router = Router()

    renderer = getattr(container, "renderer", None)

    if renderer is None:
        from lentra.bot.core.container import NullRenderer
        renderer = NullRenderer()

    # HANDLER CONTEXT INJECTION VIA CLOSURE (COMPATIBLE MODE)

    @router.callback_query()
    async def handle_any_callback(callback, *args, **kwargs):
        # renderer доступен через closure
        await renderer.render(callback)

    return router
