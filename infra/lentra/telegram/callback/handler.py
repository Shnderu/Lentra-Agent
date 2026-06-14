from lentra.telegram.callback.router import handle_callback


def process_update(update: dict):

    callback = update.get("callback_query", {})

    data = callback.get("data")

    return handle_callback(data)
