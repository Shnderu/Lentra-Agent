from lentra.telegram.ux.screens.registry import property_list_screen


def open_property_list(payload, context):
    """
    Navigate back to list
    """
    cards = context.get("cards", [])
    return property_list_screen(cards).to_dict()


def noop(payload, context):
    return {"screen": "error", "text": "Unknown action"}
