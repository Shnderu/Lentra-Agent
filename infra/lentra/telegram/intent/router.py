from lentra.telegram.state.machine import next_state
from lentra.telegram.ui.router import render


def route(event: dict) -> dict:
    chat_id = event.get("chat_id")
    text = event.get("text", "")

    print("[ROUTER IN]", chat_id, text)

    # 🔥 state transition
    state = next_state(chat_id, event)

    if not state:
        print("[ROUTER ERROR] empty state")
        return render("main")

    screen = state.get("screen")

    if not screen:
        print("[ROUTER WARN] missing screen → fallback main")
        screen = "main"

    result = render(screen)

    # 🔥 HARD GUARANTEE: UI must exist
    if not isinstance(result, dict):
        print("[ROUTER ERROR] invalid render output")
        return render("main")

    if "reply_markup" not in result:
        print("[ROUTER WARN] missing reply_markup → injecting fallback menu")
        fallback = render("main")
        result["reply_markup"] = fallback.get("reply_markup", {})

    print("[ROUTER OUT]", screen)

    return result
