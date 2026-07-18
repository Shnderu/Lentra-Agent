from typing import List, Dict


TELEGRAM_SOURCES: List[Dict] = [

    {
        "name": "domiko_vietnam",
        "channel": "domikovietnam",
        "city": "da_nang",
        "active": True,
    },

    {
        "name": "da_nang_rentals",
        "channel": "danangrentals",
        "city": "da_nang",
        "active": True,
    },

    {
        "name": "da_nang_expats",
        "channel": "danangexpats",
        "city": "da_nang",
        "active": True,
    },

]


def get_active_sources():

    return [
        source
        for source in TELEGRAM_SOURCES
        if source.get("active")
    ]
