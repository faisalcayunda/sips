from unittest.mock import AsyncMock, Mock

import pytest

from app.repositories import BusinessProductRepository
from app.schemas.user_schema import UserSchema
from app.services import BaseService, BusinessProductService


class TestBusinessProductService:
    """Test cases for BusinessProductService."""

    @pytest.fixture
    def mock_repository(self):
        """Mock BusinessProductRepository with inspector columns."""
        mock_repo = Mock(spec=BusinessProductRepository)

        mock_inspector = Mock()
        mock_inspector.c = {
            "id": Mock(),
            "business_id": Mock(),
            "commodity_id": Mock(),
            "name": Mock(),
            "description": Mock(),
            "beneficiary_count": Mock(),
            "manufacture_code": Mock(),
            "latitude": Mock(),
            "longitude": Mock(),
            "area_managed": Mock(),
            "area_planned": Mock(),
            "area_productive": Mock(),
            "area_unit": Mock(),
            "harvest_production": Mock(),
            "harvest_unit": Mock(),
            "harvest_id": Mock(),
            "type_id": Mock(),
            "tools_available": Mock(),
            "tools_detail": Mock(),
            "price_sell": Mock(),
            "buyer_type_id": Mock(),
            "buyer_count": Mock(),
            "sales_freq_id": Mock(),
            "export_status_id": Mock(),
            "export_purpose": Mock(),
            "seedstock_availability": Mock(),
            "unit_price_label": Mock(),
            "unit_sold_label": Mock(),
            "buyer_target": Mock(),
            "created_by": Mock(),
            "updated_by": Mock(),
            "created_at": Mock(),
            "updated_at": Mock(),
        }
        mock_repo.inspector = mock_inspector
        return mock_repo

    @pytest.fixture
    def mock_current_user(self):
        """Mock current user."""
        return UserSchema(id="test_user_id", name="Test User", email="test@example.com", enable="Y")

    @pytest.fixture
    def service(self, mock_repository):
        """Create BusinessProductService with mocked repository."""
        return BusinessProductService(mock_repository)

    def test_init(self, service, mock_repository):
        assert service.repository == mock_repository

    def test_inheritance(self, service):
        assert isinstance(service, BaseService)

    @pytest.mark.asyncio
    async def test_find_all(self, service, mock_repository):
        mock_repository.find_all = AsyncMock(return_value=([], 0))
        result = await service.find_all()
        assert result == ([], 0)
        mock_repository.find_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_find_by_id(self, service, mock_repository):
        mock_repository.find_by_id = AsyncMock(return_value={"id": "test_id"})
        result = await service.find_by_id("test_id")
        assert result == {"id": "test_id"}
        mock_repository.find_by_id.assert_called_once()
        call_args = mock_repository.find_by_id.call_args
        assert call_args[0][0] == "test_id"

    @pytest.mark.asyncio
    async def test_create(self, service, mock_repository, mock_current_user):
        mock_repository.create = AsyncMock(return_value={"id": "new_id"})

        data = {
            "name": "Test Product",
            "business_id": "BIZ00000000001",
            "commodity_id": 1,
        }
        result = await service.create(data, mock_current_user)
        assert result == {"id": "new_id"}
        expected_data = data.copy()
        expected_data["created_by"] = mock_current_user.id
        mock_repository.create.assert_called_once_with(expected_data)

    @pytest.mark.asyncio
    async def test_update(self, service, mock_repository, mock_current_user):
        mock_repository.exists = AsyncMock(return_value=True)
        mock_repository.update = AsyncMock(return_value={"id": "1", "name": "Updated"})

        data = {"name": "Updated"}
        result = await service.update("1", data, mock_current_user)
        assert result == {"id": "1", "name": "Updated"}
        mock_repository.update.assert_called_once()
        call_args = mock_repository.update.call_args
        assert call_args[0][0] == "1"
        expected_data = data.copy()
        expected_data["updated_by"] = mock_current_user.id
        assert call_args[0][1] == expected_data

    @pytest.mark.asyncio
    async def test_delete(self, service, mock_repository):
        mock_repository.exists = AsyncMock(return_value=True)
        mock_repository.delete = AsyncMock()

        await service.delete("1")
        mock_repository.delete.assert_called_once_with("1")

    @pytest.mark.asyncio
    async def test_find_all_with_filters(self, service, mock_repository):
        mock_repository.find_all = AsyncMock(return_value=([], 0))

        filters = ["name=test"]
        sort = "name:asc"
        search = "test"
        group_by = "name"
        limit = 10
        offset = 0

        result = await service.find_all(
            filters=filters, sort=sort, search=search, group_by=group_by, limit=limit, offset=offset
        )

        assert result == ([], 0)
        mock_repository.find_all.assert_called_once()
        call_args = mock_repository.find_all.call_args
        assert call_args[1]["filters"] is not None
        assert call_args[1]["sort"] is not None
        assert call_args[1]["search"] == search
        assert call_args[1]["group_by"] == group_by
        assert call_args[1]["limit"] == limit
        assert call_args[1]["offset"] == offset
        assert call_args[1]["relationships"] == []
        assert call_args[1]["searchable_columns"] == []
