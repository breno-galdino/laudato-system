from sqlmodel import SQLModel, Session, create_engine
from .core.config import settings

DATABASE_URL = settings.DATABASE_CONNECTION
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
