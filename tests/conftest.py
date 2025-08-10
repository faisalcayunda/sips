"""
Test configuration and common fixtures for the SIPS project.
"""

from unittest.mock import AsyncMock, MagicMock, Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import DeclarativeMeta

from app.models import BusinessesModel
from app.repositories import BusinessesRepository
from app.schemas.businesses_schema import BusinessesCreateSchema, BusinessesUpdateSchema
from app.services import BusinessesService


@pytest.fixture
def sample_business_data():
    """Sample business data for testing."""
    return {
        "name": "Test Business",
        "forestry_area_id": "area_123",
        "address": "Test Address",
        "phone": "08123456789",
        "email": "test@business.com",
        "pic_name": "Test PIC",
        "pic_phone": "08123456789",
        "pic_email": "pic@business.com",
        "sk_number": "SK-001/2024",
        "establishment_year": 2020,
        "member_count": 50,
        "chairman_name": "Test Chairman",
        "chairman_contact": "08123456789",
        "account_id": "acc_123",
        "latitude": -6.2088,
        "longitude": 106.8456,
        "capital_id": "cap_123",
        "operational_status_id": "status_123",
        "operational_period_id": "period_123",
        "class_id": "class_123",
    }


@pytest.fixture
def sample_business_response():
    """Sample business response data."""
    return {
        "id": "test_id_123",
        "status": "Y",
        "name": "Test Business",
        "forestry_area_id": "area_123",
        "address": "Test Address",
        "phone": "08123456789",
        "email": "test@business.com",
        "pic_name": "Test PIC",
        "pic_phone": "08123456789",
        "pic_email": "pic@business.com",
        "is_validated": "N",
        "created_by": "user_123",
        "updated_by": None,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": None,
        "sk_number": "SK-001/2024",
        "establishment_year": 2020,
        "member_count": 50,
        "chairman_name": "Test Chairman",
        "chairman_contact": "08123456789",
        "account_id": "acc_123",
        "latitude": -6.2088,
        "longitude": 106.8456,
        "capital_id": "cap_123",
        "operational_status_id": "status_123",
        "operational_period_id": "period_123",
        "class_id": "class_123",
    }


@pytest.fixture
def mock_business_model():
    """Mock BusinessesModel dengan SQLAlchemy inspection support."""
    mock_model = MagicMock(spec=BusinessesModel)

    # Mock SQLAlchemy inspection
    mock_model.__class__ = DeclarativeMeta
    mock_model.__name__ = "BusinessesModel"

    # Mock table columns
    mock_model.__table__ = MagicMock()
    mock_model.__table__.columns = {
        "id": MagicMock(),
        "name": MagicMock(),
        "status": MagicMock(),
        "forestry_area_id": MagicMock(),
        "address": MagicMock(),
        "phone": MagicMock(),
        "email": MagicMock(),
        "pic_name": MagicMock(),
        "pic_phone": MagicMock(),
        "pic_email": MagicMock(),
        "is_validated": MagicMock(),
        "created_by": MagicMock(),
        "updated_by": MagicMock(),
        "created_at": MagicMock(),
        "updated_at": MagicMock(),
        "sk_number": MagicMock(),
        "establishment_year": MagicMock(),
        "member_count": MagicMock(),
        "chairman_name": MagicMock(),
        "chairman_contact": MagicMock(),
        "account_id": MagicMock(),
        "latitude": MagicMock(),
        "longitude": MagicMock(),
        "capital_id": MagicMock(),
        "operational_status_id": MagicMock(),
        "operational_period_id": MagicMock(),
        "class_id": MagicMock(),
    }

    return mock_model


@pytest.fixture
def mock_business_repository(mock_business_model):
    """Mock BusinessesRepository."""
    repository = Mock(spec=BusinessesRepository)
    repository.model = mock_business_model

    # Mock methods
    repository.find_all = AsyncMock(return_value=([], 0))
    repository.find_by_id = AsyncMock(return_value={"id": "test_id"})
    repository.create = AsyncMock(return_value={"id": "new_id"})
    repository.update = AsyncMock(return_value={"id": "test_id", "name": "Updated"})
    repository.delete = AsyncMock()

    return repository


@pytest.fixture
def mock_business_service(mock_business_repository):
    """Mock BusinessesService."""
    service = Mock(spec=BusinessesService)
    service.repository = mock_business_repository

    # Mock methods
    service.find_all = AsyncMock(return_value=([], 0))
    service.find_by_id = AsyncMock(return_value={"id": "test_id"})
    service.create = AsyncMock(return_value={"id": "new_id"})
    service.update = AsyncMock(return_value={"id": "test_id", "name": "Updated"})
    service.delete = AsyncMock()

    return service


@pytest.fixture
def test_app():
    """Create FastAPI app for testing."""
    app = FastAPI()
    return app


@pytest.fixture
def test_client(test_app):
    """Create test client."""
    return TestClient(test_app)


@pytest.fixture
def valid_business_create_schema(sample_business_data):
    """Valid business create schema."""
    return BusinessesCreateSchema(**sample_business_data)


@pytest.fixture
def valid_business_update_schema():
    """Valid business update schema."""
    return BusinessesUpdateSchema(name="Updated Business", status="N")


@pytest.fixture
def mock_db_session():
    """Mock database session."""
    session = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    return session


@pytest.fixture
def mock_db():
    """Mock database connection."""
    db = MagicMock()
    db.session = mock_db_session()
    return db
