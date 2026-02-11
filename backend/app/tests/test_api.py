import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, Base
from app.models.models import Tenant, User

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_tenant(client):
    db = TestingSessionLocal()
    tenant = Tenant(
        name="Test Business",
        slug="test-business",
        email="test@business.com",
        phone="+15141234567"
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    db.close()
    return tenant

@pytest.fixture
def test_user(client, test_tenant):
    db = TestingSessionLocal()
    user = User(
        tenant_id=test_tenant.id,
        email="user@test.com",
        full_name="Test User",
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_readiness_check(client):
    """Test readiness check endpoint"""
    response = client.get("/api/health/ready")
    assert response.status_code == 200
    assert "database" in response.json()

def test_liveness_check(client):
    """Test liveness check endpoint"""
    response = client.get("/api/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"

def test_create_tenant(client):
    """Test creating a new tenant"""
    response = client.post(
        "/api/tenants/",
        json={
            "name": "New Business",
            "slug": "new-business",
            "email": "new@business.com",
            "phone": "+15149876543",
            "settings": {}
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Business"
    assert data["slug"] == "new-business"
    assert data["email"] == "new@business.com"

def test_create_booking(client, test_tenant):
    """Test creating a new booking"""
    from datetime import datetime, timedelta
    
    response = client.post(
        "/api/bookings/",
        json={
            "tenant_id": test_tenant.id,
            "customer_name": "John Doe",
            "customer_phone": "+15145551234",
            "service_type": "Consultation",
            "appointment_date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "source": "web"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert data["status"] == "pending"

def test_list_faq_items(client, test_tenant):
    """Test listing FAQ items"""
    response = client.get(f"/api/faq/?tenant_id={test_tenant.id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Biz-Bot API"
