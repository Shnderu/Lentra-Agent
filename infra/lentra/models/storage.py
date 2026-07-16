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
        nullable=False
    )

    price_vnd_mln = Column(
        Float,
        nullable=True,
        index=True
    )

    deposit_vnd_mln = Column(
        Float,
        nullable=True
    )

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

    pet_friendly = Column(
        Boolean,
        default=False
    )

    pool = Column(
        Boolean,
        default=False
    )

    sea_view = Column(
        Boolean,
        default=False
    )

    score = Column(
        Float,
        default=0.0
    )

    raw = Column(
        Text
    )

    features = Column(
        JSON
    )

    city = Column(
        String,
        index=True
    )

    district = Column(
        String,
        index=True
    )

    source = Column(
        Text
    )

    url = Column(
        Text
    )

    embedding = Column(
        JSON
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow
    )
