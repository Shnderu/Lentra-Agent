from lentra.telegram.ux.screens.base import UXScreen


def error_screen(message: str = "Error"):
    return UXScreen(
        screen="error",
        text=message,
        cards=[],
        buttons=[]
    )


def property_list_screen(cards: list):
    return UXScreen(
        screen="property_list",
        text="Available properties",
        cards=cards,
        buttons=[]
    )


SCREEN_MAP = {
    "error": error_screen,
    "property_list": property_list_screen
}
