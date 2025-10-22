import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base
from app.contracts import get_db
from app.auth import create_access_token
from app import models
import json

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency override for get_db
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Apply the override to the FastAPI app
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    """
    Yields a clean, in-memory database session for each test.
    Creates all tables before the test and drops them after.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Yields a TestClient that uses the clean, in-memory database.
    Depends on db_session to ensure tables are created and dropped.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def authenticated_client(client):
    """
    Yields a TestClient that is pre-authenticated as the 'admin' user.
    """
    token = create_access_token(data={"sub": "admin"})
    client.headers = {"Authorization": f"Bearer {token}"}
    yield client


@pytest.fixture(scope="session")
def mock_ai_service_response():
    """
    Provides a consistent, fake response from the AI service.
    This avoids making real API calls during tests.
    """
    return {
        "contratante": json.dumps(["Empresa Teste LTDA"]),
        "contratado": json.dumps(["Fornecedor de Testes SA"]),
        "valor_bens": "R$ 50.000,00",
        "obrigacoes_contratante": json.dumps(["Pagar o valor", "Fornecer acesso"]),
        "obrigacoes_contratada": json.dumps(["Entregar o produto", "Prestar suporte"]),
        "objeto": json.dumps(["Licença de software de teste"]),
        "vigencia": "24 meses",
        "clausula_rescisao": "Multa de 20% em caso de rescisão antecipada.",
    }