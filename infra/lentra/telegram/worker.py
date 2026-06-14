from lentra.telegram.ui.router import resolve_screen, render
from lentra.domain.ui_bridge import handle_screen
from lentra.domain.handlers.registry import HANDLERS


def route(event: dict, state: dict = None) -> dict:
    text = (event.get("text") or "").strip()

    # =========================
    # UI ROUTING
    # =========================
    screen = resolve_screen(text, state)

    ui = render(screen)

    # =========================
    # BUSINESS LAYER ATTACHMENT
    # =========================
    business = handle_screen(screen, event)

    # business overrides UI text if needed
    if business and business.get("text"):
        ui["text"] = business["text"]

    return {
        "text": ui["text"],
        "reply_markup": ui.get("reply_markup"),
        "meta": {
            "screen": screen
        }
    }
