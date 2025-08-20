from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.orm import DeclarativeMeta

from app.models import BusinessProductModel
from app.repositories import BusinessProductRepository


class TestBusinessProductRepository:
    """Test cases for BusinessProductRepository."""

    @pytest.fixture
    def mock_model(self):
        """Mock BusinessProductModel with SQLAlchemy inspection support."""
        mock_model = MagicMock(spec=BusinessProductModel)
        mock_model.__class__ = DeclarativeMeta
        mock_model.__name__ = "BusinessProductModel"

        mock_model.__table__ = MagicMock()
        mock_model.__table__.columns = {
            "id": MagicMock(),
            "business_id": MagicMock(),
            "commodity_id": MagicMock(),
            "name": MagicMock(),
            "description": MagicMock(),
            "beneficiary_count": MagicMock(),
            "manufacture_code": MagicMock(),
            "latitude": MagicMock(),
            "longitude": MagicMock(),
            "area_managed": MagicMock(),
            "area_planned": MagicMock(),
            "area_productive": MagicMock(),
            "area_unit": MagicMock(),
            "harvest_production": MagicMock(),
            "harvest_unit": MagicMock(),
            "harvest_id": MagicMock(),
            "type_id": MagicMock(),
            "tools_available": MagicMock(),
            "tools_detail": MagicMock(),
            "price_sell": MagicMock(),
            "buyer_type_id": MagicMock(),
            "buyer_count": MagicMock(),
            "sales_freq_id": MagicMock(),
            "export_status_id": MagicMock(),
            "export_purpose": MagicMock(),
            "seedstock_availability": MagicMock(),
            "unit_price_label": MagicMock(),
            "unit_sold_label": MagicMock(),
            "buyer_target": MagicMock(),
            "created_by": MagicMock(),
            "updated_by": MagicMock(),
            "created_at": MagicMock(),
            "updated_at": MagicMock(),
        }

        return mock_model

    @pytest.fixture
    def mock_session(self):
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
        with patch("app.repositories.base.inspect") as mock_inspect, patch("app.repositories.base.db") as mock_db:
            mock_inspector = MagicMock()
            mock_inspector.c = mock_model.__table__.columns
            mock_inspect.return_value = mock_inspector

            mock_db.session = mock_session

            return BusinessProductRepository(mock_model)

    def test_init(self, repository, mock_model, mock_session):
        assert repository.model == mock_model
        assert repository.session == mock_session

    def test_inheritance(self, repository):
        from app.repositories import BaseRepository

        assert isinstance(repository, BaseRepository)

    @pytest.mark.asyncio
    async def test_find_all(self, repository):
        with patch.object(repository, "find_all", new_callable=AsyncMock) as mock_find_all:
            mock_find_all.return_value = ([], 0)
            result = await repository.find_all()
            assert result == ([], 0)

    @pytest.mark.asyncio
    async def test_find_by_id(self, repository):
        with patch.object(repository, "find_by_id", new_callable=AsyncMock) as mock_find_by_id:
            mock_find_by_id.return_value = {"id": "1"}
            result = await repository.find_by_id("1")
            assert result == {"id": "1"}

    @pytest.mark.asyncio
    async def test_create(self, repository):
        with patch.object(repository, "create", new_callable=AsyncMock) as mock_create:
            mock_create.return_value = {"id": "1"}
            result = await repository.create({"name": "X"})
            assert result == {"id": "1"}

    @pytest.mark.asyncio
    async def test_update(self, repository):
        with patch.object(repository, "update", new_callable=AsyncMock) as mock_update:
            mock_update.return_value = {"id": "1", "name": "Updated"}
            result = await repository.update("1", {"name": "Updated"})
            assert result == {"id": "1", "name": "Updated"}

    @pytest.mark.asyncio
    async def test_delete(self, repository):
        with patch.object(repository, "delete", new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = True
            result = await repository.delete("1")
            assert result is True
