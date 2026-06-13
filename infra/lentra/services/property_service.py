from sqlalchemy import create_engine, text
import os
import json


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


class PropertyService:

    def process(self, text, raw_json, chat_id, parsed=None):
        parsed = parsed or {}

        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO properties (
                    description,
                    price,
                    currency,
                    location,
                    property_type,
                    source_chat_id,
                    source_message_id,
                    confidence,
                    raw_data
                )
                VALUES (
                    :description,
                    :price,
                    :currency,
                    :location,
                    :property_type,
                    :source_chat_id,
                    :source_message_id,
                    :confidence,
                    :raw_data
                )
            """), {
                "description": text,
                "price": parsed.get("price"),
                "currency": parsed.get("currency"),
                "location": parsed.get("location"),
                "property_type": parsed.get("type"),
                "source_chat_id": chat_id,
                "source_message_id": parsed.get("message_id"),
                "confidence": parsed.get("confidence", 0.0),
                "raw_data": json.dumps(parsed, ensure_ascii=False)
            })
