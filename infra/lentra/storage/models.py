from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# ----------------------------
# RAW MESSAGES (AUDIT LAYER)
# ----------------------------
class RawMessageDB(Base):
    __tablename__ = "raw_messages"

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, index=True)
    chat_id = Column(Integer, index=True)
    chat_title = Column(String)
    text = Column(Text)
    raw_json = Column(JSON)
    ingested_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="new")


# ----------------------------
# PROCESSING QUEUE
# ----------------------------
class ProcessingQueueDB(Base):
    __tablename__ = "processing_queue"

    id = Column(Integer, primary_key=True)
    raw_message_id = Column(Integer, index=True)
    task_type = Column(String)
    payload = Column(JSON)
    status = Column(String, default="new")
    created_at = Column(DateTime, default=datetime.utcnow)


# ----------------------------
# DOMAIN MODEL (FINAL PRODUCT)
# ----------------------------
class PropertyDB(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)

    # core info
    title = Column(String, nullable=True)
    description = Column(Text)

    # parsed structured data
    price = Column(Float, nullable=True)
    currency = Column(String, nullable=True)
    location = Column(String, nullable=True)
    property_type = Column(String, nullable=True)

    # metadata
    source_chat_id = Column(Integer, index=True)
    source_message_id = Column(Integer, index=True)

    # system fields
    confidence = Column(Float, default=0.0)
    raw_data = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)
