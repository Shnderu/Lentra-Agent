from lentra.telegram.ui.renderer import renderer


async def search_feature(ctx: dict) -> str:
    """
    Production feature: search
    """

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
