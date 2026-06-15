def format_listing(item: dict) -> str:

    return (
        f"🏡 {item.get('title')}\n"
        f"📍 {item.get('city')} / {item.get('district')}\n"
        f"💰 {item.get('price_vnd_mln')} mln VND\n"
        f"⭐ score: {item.get('score')}\n\n"
        f"{'🏊 pool' if item.get('pool') else ''} "
        f"{'🌊 sea view' if item.get('sea_view') else ''}"
    )


def format_search_result(items: list) -> str:

    text = "🔎 Search results:\n\n"

    for i, item in enumerate(items[:5], 1):
        text += f"{i}. {format_listing(item)}\n\n"

    return text
