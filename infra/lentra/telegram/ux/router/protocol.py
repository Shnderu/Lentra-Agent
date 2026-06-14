"""
Callback Data Protocol v1

FORMAT:
    action:entity:payload

EXAMPLES:
    list:open:123
    list:back:
    property:view:5139
"""

def encode(action: str, entity: str = "", payload: str = ""):
    return f"{action}:{entity}:{payload}".rstrip(":")


def decode(callback_data: str):
    parts = callback_data.split(":")

    return {
        "action": parts[0] if len(parts) > 0 else None,
        "entity": parts[1] if len(parts) > 1 else None,
        "payload": parts[2] if len(parts) > 2 else None
    }
