from lentra.telegram.ui.renderer import renderer


async def search_handler(ctx: dict):
    """
    Заглушка feature: search
    """

    message = ctx.get("message")

    data = {
        "screen": "property_list",
        "cards": [
            {
                "title": "Demo Property",
                "price": "$1000",
                "city": "Hanoi",
                "meta": {"score": 0.91}
            }
        ]
    }

    return renderer.render_message(data)
