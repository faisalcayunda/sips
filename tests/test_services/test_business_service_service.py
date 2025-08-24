from unittest.mock import AsyncMock, Mock

import pytest

from app.repositories import BusinessServiceRepository
from app.schemas import UserSchema
from app.services import BusinessServiceService


class TestBusinessServiceService:
    """Test cases for BusinessServiceService."""

    @pytest.fixture
    def mock_repository(self):
        """Mock BusinessServiceRepository."""
        mock_repo = Mock(spec=BusinessServiceRepository)
        # Mock inspector to provide valid columns for validation
        mock_inspector = Mock()
        mock_inspector.c = {
            "id": Mock(),
            "business_id": Mock(),
            "commodity_id": Mock(),
            "name": Mock(),
            "latitude": Mock(),
            "longitude": Mock(),
            "visitor_type_id": Mock(),
            "origin_visitor_id": Mock(),
            "ticket_price": Mock(),
            "parking_fee": Mock(),
            "other_item_price_id": Mock(),
            "additional_info": Mock(),
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
        """Create BusinessServiceService instance with mocked repository."""
        return BusinessServiceService(mock_repository)

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

        data = {"name": "Test Service"}
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
        assert call_args[1]["refresh"] == True  # Keyword argument (refresh=True)

    @pytest.mark.asyncio
    async def test_update_with_refresh_false(self, service, mock_repository, mock_current_user):
        """Test update method with refresh=False."""
        mock_repository.update = AsyncMock(return_value={"id": "test_id", "name": "Updated"})

        data = {"name": "Updated"}
        result = await service.update("test_id", data, mock_current_user, refresh=False)
        assert result == {"id": "test_id", "name": "Updated"}
        # Check that update was called with correct arguments
        mock_repository.update.assert_called_once()
        call_args = mock_repository.update.call_args
        assert call_args[0][0] == "test_id"  # First positional argument
        expected_data = data.copy()
        expected_data["updated_by"] = mock_current_user.id
        assert call_args[0][1] == expected_data  # Second positional argument
        assert call_args[1]["refresh"] == False  # Keyword argument (refresh=False)

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

    @pytest.mark.asyncio
    async def test_find_all_with_relationships(self, service, mock_repository):
        """Test find_all method with relationships."""
        mock_repository.find_all = AsyncMock(return_value=([], 0))

        relationships = ["business", "commodity"]
        searchable_columns = ["name", "business_id"]

        result = await service.find_all(relationships=relationships, searchable_columns=searchable_columns)

        assert result == ([], 0)
        mock_repository.find_all.assert_called_once()
        call_args = mock_repository.find_all.call_args
        assert call_args[1]["relationships"] == relationships
        assert call_args[1]["searchable_columns"] == searchable_columns

    @pytest.mark.asyncio
    async def test_find_by_id_with_relationships(self, service, mock_repository):
        """Test find_by_id method with relationships."""
        mock_repository.find_by_id = AsyncMock(return_value={"id": "test_id"})

        relationships = ["business", "commodity"]
        result = await service.find_by_id("test_id", relationships=relationships)

        assert result == {"id": "test_id"}
        mock_repository.find_by_id.assert_called_once_with("test_id", relationships=relationships)

    @pytest.mark.asyncio
    async def test_create_with_complex_data(self, service, mock_repository, mock_current_user):
        """Test create method with complex data structure."""
        mock_repository.create = AsyncMock(return_value={"id": "new_id"})

        data = {
            "business_id": "BUS123",
            "commodity_id": 1,
            "name": "Forest Tourism Service",
            "latitude": "-6.2088",
            "longitude": "106.8456",
            "visitor_type_id": "VT01",
            "origin_visitor_id": "OV01",
            "ticket_price": 50000,
            "parking_fee": 10000,
            "other_item_price_id": "OIP01",
            "additional_info": "Additional services available",
        }

        result = await service.create(data, mock_current_user)
        assert result == {"id": "new_id"}

        # Verify that created_by is added to data
        expected_data = data.copy()
        expected_data["created_by"] = mock_current_user.id
        mock_repository.create.assert_called_once_with(expected_data)

    @pytest.mark.asyncio
    async def test_update_with_complex_data(self, service, mock_repository, mock_current_user):
        """Test update method with complex data structure."""
        mock_repository.update = AsyncMock(return_value={"id": "test_id", "name": "Updated Service"})

        data = {
            "name": "Updated Service",
            "ticket_price": 75000,
            "parking_fee": 15000,
            "additional_info": "Updated additional services",
        }

        result = await service.update("test_id", data, mock_current_user)
        assert result == {"id": "test_id", "name": "Updated Service"}

        # Verify that updated_by is added to data
        expected_data = data.copy()
        expected_data["updated_by"] = mock_current_user.id
        mock_repository.update.assert_called_once_with("test_id", expected_data, refresh=True)

    @pytest.mark.asyncio
    async def test_find_all_pagination(self, service, mock_repository):
        """Test find_all method with pagination parameters."""
        mock_repository.find_all = AsyncMock(return_value=([], 100))

        limit = 25
        offset = 50

        result = await service.find_all(limit=limit, offset=offset)
        assert result == ([], 100)

        mock_repository.find_all.assert_called_once()
        call_args = mock_repository.find_all.call_args
        assert call_args[1]["limit"] == limit
        assert call_args[1]["offset"] == offset

    @pytest.mark.asyncio
    async def test_find_all_default_values(self, service, mock_repository):
        """Test find_all method with default values."""
        mock_repository.find_all = AsyncMock(return_value=([], 0))

        result = await service.find_all()

        assert result == ([], 0)
        mock_repository.find_all.assert_called_once()
        call_args = mock_repository.find_all.call_args

        # Check default values
        assert call_args[1]["filters"] == []
        assert call_args[1]["sort"] == []
        assert call_args[1]["search"] == ""
        assert call_args[1]["group_by"] is None
        assert call_args[1]["limit"] == 100
        assert call_args[1]["offset"] == 0
        assert call_args[1]["relationships"] == []
        assert call_args[1]["searchable_columns"] == []
