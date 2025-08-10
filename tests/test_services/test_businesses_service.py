from unittest.mock import AsyncMock, Mock

import pytest

from app.repositories import BusinessesRepository
from app.schemas.user_schema import UserSchema
from app.services import BusinessesService


class TestBusinessesService:
    """Test cases for BusinessesService."""

    @pytest.fixture
    def mock_repository(self):
        """Mock BusinessesRepository."""
        mock_repo = Mock(spec=BusinessesRepository)
        # Mock inspector to provide valid columns for validation
        # Use the actual model attribute names, not database column names
        mock_inspector = Mock()
        mock_inspector.c = {
            "id": Mock(),
            "status": Mock(),
            "name": Mock(),
            "forestry_area_id": Mock(),
            "sk_number": Mock(),
            "establishment_year": Mock(),
            "member_count": Mock(),
            "chairman_name": Mock(),
            "chairman_contact": Mock(),
            "account_id": Mock(),
            "latitude": Mock(),
            "longitude": Mock(),
            "capital_id": Mock(),
            "operational_status_id": Mock(),
            "operational_period_id": Mock(),
            "class_id": Mock(),
            "is_validated": Mock(),
            "capital_provider_name": Mock(),
            "capital_provision_type": Mock(),
            "capital_provision_type_other": Mock(),
            "capital_repayment_period": Mock(),
            "created_by": Mock(),
            "updated_by": Mock(),
            "created_at": Mock(),
            "updated_at": Mock(),
        }
        mock_repo.inspector = mock_inspector
        return mock_repo

    @pytest.fixture
    def mock_current_user(self):
        """Mock current user for testing."""
        return UserSchema(id="test_user_id", name="Test User", email="test@example.com", enable="Y")

    @pytest.fixture
    def service(self, mock_repository):
        """Create BusinessesService instance with mocked repository."""
        return BusinessesService(mock_repository)

    def test_init(self, service, mock_repository):
        """Test service initialization."""
        assert service.repository == mock_repository

    def test_inheritance(self, service):
        """Test that service inherits from BaseService."""
        from app.services import BaseService

        assert isinstance(service, BaseService)

    @pytest.mark.asyncio
    async def test_find_all(self, service, mock_repository):
        """Test find_all method."""
        mock_repository.find_all = AsyncMock(return_value=([], 0))

        result = await service.find_all()
        assert result == ([], 0)
        mock_repository.find_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_find_by_id(self, service, mock_repository):
        """Test find_by_id method."""
        mock_repository.find_by_id = AsyncMock(return_value={"id": "test_id"})

        result = await service.find_by_id("test_id")
        assert result == {"id": "test_id"}
        # Check that find_by_id was called with correct arguments
        mock_repository.find_by_id.assert_called_once()
        call_args = mock_repository.find_by_id.call_args
        assert call_args[0][0] == "test_id"  # First positional argument

    @pytest.mark.asyncio
    async def test_create(self, service, mock_repository, mock_current_user):
        """Test create method."""
        mock_repository.create = AsyncMock(return_value={"id": "new_id"})

        data = {"name": "Test Business"}
        result = await service.create(data, mock_current_user)
        assert result == {"id": "new_id"}
        # Verify that created_by is added to data
        expected_data = data.copy()
        expected_data["created_by"] = mock_current_user.id
        mock_repository.create.assert_called_once_with(expected_data)

    @pytest.mark.asyncio
    async def test_update(self, service, mock_repository, mock_current_user):
        """Test update method."""
        mock_repository.update = AsyncMock(return_value={"id": "test_id", "name": "Updated"})

        data = {"name": "Updated"}
        result = await service.update("test_id", data, mock_current_user)
        assert result == {"id": "test_id", "name": "Updated"}
        # Check that update was called with correct arguments
        mock_repository.update.assert_called_once()
        call_args = mock_repository.update.call_args
        assert call_args[0][0] == "test_id"  # First positional argument
        expected_data = data.copy()
        expected_data["updated_by"] = mock_current_user.id
        assert call_args[0][1] == expected_data  # Second positional argument

    @pytest.mark.asyncio
    async def test_delete(self, service, mock_repository):
        """Test delete method."""
        mock_repository.delete = AsyncMock()

        await service.delete("test_id")
        mock_repository.delete.assert_called_once_with("test_id")

    @pytest.mark.asyncio
    async def test_find_all_with_filters(self, service, mock_repository):
        """Test find_all method with filters."""
        mock_repository.find_all = AsyncMock(return_value=([], 0))

        filters = ["name=test"]  # Use valid column with proper filter format
        sort = "name:asc"  # Use valid column with proper sort format
        search = "test"
        group_by = "name"  # Use valid column
        limit = 10
        offset = 0

        result = await service.find_all(
            filters=filters, sort=sort, search=search, group_by=group_by, limit=limit, offset=offset
        )

        assert result == ([], 0)
        # Verify that find_all was called with the expected parameters
        mock_repository.find_all.assert_called_once()
        call_args = mock_repository.find_all.call_args

        # Check that the required parameters are present
        assert call_args[1]["filters"] is not None  # Should contain processed filters
        assert call_args[1]["sort"] is not None  # Should contain processed sort
        assert call_args[1]["search"] == search
        assert call_args[1]["group_by"] == group_by
        assert call_args[1]["limit"] == limit
        assert call_args[1]["offset"] == offset
        assert call_args[1]["relationships"] == []  # Default empty list
        assert call_args[1]["searchable_columns"] == []  # Default empty list
