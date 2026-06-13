from lentra.storage.db import SessionLocal, engine, Base
from lentra.storage.models import PropertyDB


class PropertyRepository:

    def __init__(self):
        Base.metadata.create_all(bind=engine)

    def save(self, prop: PropertyDB):
        db = SessionLocal()
        try:
            db.add(prop)
            db.commit()
            db.refresh(prop)
            return prop
        finally:
            db.close()

    def list(self, limit: int = 50):
        db = SessionLocal()
        try:
            return db.query(PropertyDB).order_by(PropertyDB.id.desc()).limit(limit).all()
        finally:
            db.close()
