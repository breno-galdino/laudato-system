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
            session.add_all([
                Scope(name="me", description="Acesso ao próprio usuário"),
                Scope(name="admin", description="Administrador do sistema")
            ])
            session.commit()
    yield
    SQLModel.metadata.drop_all(engine)  # DROP TABLES AFTER TESTS

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def admin_token(client):
    # Cria o usuário
    client.post(
        "/auth/register",
        json={
            "email": "admin@example.com",
            "password": "adminpass",
            "username": "adminuser",
            "full_name": "Admin User",
        },
    )

    # Opcional: promover manualmente para admin
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == "admin@example.com")).first()
        admin_scope = session.exec(select(Scope).where(Scope.name == "admin")).first()
        
        user_admin = session.exec(select(UserScope).where(UserScope.user_id == user.id, UserScope.scope_id == admin_scope.id)).first()
        
        if not user_admin:
            session.add(UserScope(user_id=user.id, scope_id=admin_scope.id))
            session.commit()

    # Faz login
    response = client.post(
        "/auth/token",
        data={"username": "admin@example.com", "password": "adminpass"},
    )

    token = response.json()["access_token"]
    return f"Bearer {token}"

