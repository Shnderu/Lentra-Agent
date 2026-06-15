from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type, List, Optional

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def get_by_id(self, id: int) -> Optional[T]:
        return self.session.query(self.model).filter(self.model.id == id).first()

    def add(self, obj: T) -> T:
        self.session.add(obj)
        self.session.flush()
        return obj

    def list(self, limit: int = 100) -> List[T]:
        return self.session.query(self.model).limit(limit).all()
