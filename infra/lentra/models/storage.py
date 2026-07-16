from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    JSON,
    Boolean,
)

from lentra.db.session import Base


class RawMessageDB(Base):
    __tablename__ = "raw_messages"

    id = Column(Integer, primary_key=True)

    message_id = Column(Integer, index=True)
    chat_id = Column(Integer, index=True)

    chat_title = Column(String)

    text = Column(Text)

    raw_json = Column(JSON)

    ingested_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    status = Column(
        String,
        default="new"
    )


class ProcessingQueueDB(Base):
    __tablename__ = "processing_queue"

    id = Column(Integer, primary_key=True)

    raw_message_id = Column(
        Integer,
        index=True
    )

    task_type = Column(String)

    payload = Column(JSON)

    status = Column(
        String,
        default="new"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class PropertyDB(Base):
    """
    Canonical normalized property entity.

    Source:
        Telegram
        Facebook
        Local sites

    Used by:
        Deduplication
        Market Intelligence
        AI ranking
    """

    __tablename__ = "properties"


    id = Column(
        Integer,
        primary_key=True
    )


    title = Column(
        String,
        nullable=True
    )

    description = Column(
        Text
    )


    # normalized pricing

    price = Column(
        Float,
        nullable=True
    )

    price_vnd_mln = Column(
        Float,
        nullable=True,
        index=True
    )

    currency = Column(
        String,
        nullable=True
    )


    # location

    location = Column(
        String,
        nullable=True
    )

    city = Column(
        String,
        nullable=True,
        index=True
    )

    district = Column(
        String,
        nullable=True,
        index=True
    )


    property_type = Column(
        String,
        nullable=True
    )


    # property characteristics

    area_m2 = Column(
        Float,
        nullable=True
    )

    bedrooms = Column(
        Integer,
        nullable=True
    )

    bathrooms = Column(
        Integer,
        nullable=True
    )


    pool = Column(
        Boolean,
        default=False
    )

    sea_view = Column(
        Boolean,
        default=False
    )

    pet_friendly = Column(
        Boolean,
        default=False
    )


    # intelligence fields

    score = Column(
        Float,
        default=0.0
    )

    confidence = Column(
        Float,
        default=0.0
    )


    features = Column(
        JSON
    )


    raw_text = Column(
        Text
    )


    raw_data = Column(
        JSON
    )


    # source tracking

    source_chat_id = Column(
        Integer,
        index=True
    )

    source_message_id = Column(
        Integer,
        index=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
