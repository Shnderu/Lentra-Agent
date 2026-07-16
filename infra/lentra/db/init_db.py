from lentra.db.session import engine
from lentra.db.session import Base

# важно: импорт модели обязателен
from lentra.models.apartment import Apartment  # noqa

def init():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init()
