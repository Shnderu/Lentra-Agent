from typing import List, Dict, Any
from lentra.core.data_layer.adapters.base import BaseAdapter


class TelegramAdapter(BaseAdapter):
    """
    Simulated Telegram channels ingestion
    """

    def fetch(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "tg_001",
                "source": "telegram",
                "source_url": "https://t.me/vietnam_rentals/123",

                "title": "HCMC apartment district 1",
                "description": "Modern flat, expat friendly",

                "price": "15000000",
                "currency": "VND",

                "property_type": "apartment",
                "size": "50",

                "location": "Ho Chi Minh City, District 1",

                "images": [],
                "contact": "@agent123",
                "timestamp": "2026-06-26"
            }
        ]
