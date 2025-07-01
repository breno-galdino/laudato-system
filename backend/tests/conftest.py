import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session, select
from app.main import app
from app.database import get_session

from app.models.users import User, UserScope, Scope

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        if not session.exec(select(Scope).where(Scope.name == "me")).first():
            scope = Scope(name="me", description="Acesso ao próprio usuário")
            session.add(scope)
            session.commit()
            session.refresh(scope)
    yield
    SQLModel.metadata.drop_all(engine)  # DROP TABLES AFTER TESTS

@pytest.fixture
def client():
    return TestClient(app)
