from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from models.application import Application
    from models.candidate import Candidate
    from models.review import Review
    from models.score import Score
    from models.user import User

    _ = (Application, Candidate, Review, Score, User)
    Base.metadata.create_all(bind=engine)
