import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import Base, get_db
from app.models import Tenant, User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def test_tenant(client):
    """Create a test tenant"""
    db = TestingSessionLocal()
    tenant = Tenant(name="Test Tenant", slug="test-tenant", is_active=True)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    db.close()
    return tenant


def test_register_user(client, test_tenant):
    """Test user registration"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "tenant_id": test_tenant.id,
            "preferred_language": "en"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"


def test_request_magic_link(client, test_tenant):
    """Test magic link request"""
    # First create a user
    db = TestingSessionLocal()
    user = User(
        email="test@example.com",
        full_name="Test User",
        tenant_id=test_tenant.id,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.close()
    
    response = client.post(
        "/api/v1/auth/request-magic-link",
        json={"email": "test@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
