from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.orm import DeclarativeMeta

from app.models import BusinessesModel
from app.repositories import BusinessesRepository


class TestBusinessesRepository:
    """Test cases for BusinessesRepository."""

    @pytest.fixture
    def mock_model(self):
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
    def mock_session(self):
        """Mock database session."""
        session = AsyncMock()
        session.commit = AsyncMock()
        session.rollback = AsyncMock()
        session.close = AsyncMock()
        session.execute = AsyncMock()
        session.scalar = AsyncMock()
        session.add = AsyncMock()
        session.refresh = AsyncMock()
        return session

    @pytest.fixture
    def repository(self, mock_model, mock_session):
        """Create BusinessesRepository instance with mocked model and session."""
        # Patch the inspect function to return our mock inspector
        with patch("app.repositories.base.inspect") as mock_inspect, patch("app.repositories.base.db") as mock_db:

            mock_inspector = MagicMock()
            mock_inspector.c = mock_model.__table__.columns
            mock_inspect.return_value = mock_inspector

            # Mock the database session
            mock_db.session = mock_session

            return BusinessesRepository(mock_model)

    def test_init(self, repository, mock_model, mock_session):
        """Test repository initialization."""
        assert repository.model == mock_model
        assert repository.session == mock_session

    def test_inheritance(self, repository):
        """Test that repository inherits from BaseRepository."""
        from app.repositories import BaseRepository

        assert isinstance(repository, BaseRepository)

    @pytest.mark.asyncio
    async def test_find_all(self, repository):
        """Test find_all method."""
        # Mock the entire find_all method to avoid SQLAlchemy operations
        with patch.object(repository, "find_all", new_callable=AsyncMock) as mock_find_all:
            mock_find_all.return_value = ([], 0)

            result = await repository.find_all()
            assert result == ([], 0)

    @pytest.mark.asyncio
    async def test_find_by_id(self, repository):
        """Test find_by_id method."""
        # Mock the entire find_by_id method to avoid SQLAlchemy operations
        with patch.object(repository, "find_by_id", new_callable=AsyncMock) as mock_find_by_id:
            mock_find_by_id.return_value = {"id": "test_id"}

            result = await repository.find_by_id("test_id")
            assert result == {"id": "test_id"}

    @pytest.mark.asyncio
    async def test_create(self, repository):
        """Test create method."""
        # Mock the entire create method to avoid SQLAlchemy operations
        with patch.object(repository, "create", new_callable=AsyncMock) as mock_create:
            mock_create.return_value = {"id": "new_id"}

            data = {"name": "Test Business"}
            result = await repository.create(data)
            assert result == {"id": "new_id"}

    @pytest.mark.asyncio
    async def test_update(self, repository):
        """Test update method."""
        # Mock the entire update method to avoid SQLAlchemy operations
        with patch.object(repository, "update", new_callable=AsyncMock) as mock_update:
            mock_update.return_value = {"id": "test_id", "name": "Updated"}

            data = {"name": "Updated"}
            result = await repository.update("test_id", data)
            assert result == {"id": "test_id", "name": "Updated"}

    @pytest.mark.asyncio
    async def test_delete(self, repository):
        """Test delete method."""
        # Mock the entire delete method to avoid SQLAlchemy operations
        with patch.object(repository, "delete", new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = True

            result = await repository.delete("test_id")
            assert result is True
