from lentra.db.session import engine
from lentra.db.session import Base

# canonical property model registration
from lentra.models.storage import PropertyDB  # noqa


def init():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init()
