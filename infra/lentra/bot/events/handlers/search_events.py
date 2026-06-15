from lentra.bot.events.registry import bus


async def on_search_completed(event):

    if event.payload.get("results_count", 0) == 0:
        print(f"[EVENT] No results for user {event.user_id}")

    else:
        print(f"[EVENT] Search OK for user {event.user_id}")


def register_search_handlers():
    bus.subscribe("search_completed", on_search_completed)
