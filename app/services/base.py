from functools import lru_cache
from typing import Any, Dict, Generic, List, Tuple, Type, TypeVar, Union

from sqlalchemy import or_

from app.core.database import Base
from app.core.exceptions import NotFoundException, UnprocessableEntity
from app.repositories import BaseRepository

ModelType = TypeVar("ModelType", bound=Base)
RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)


class BaseService(Generic[ModelType, RepositoryType]):
    """Optimized base service dengan caching dan performance improvements."""

    def __init__(self, model: Type[ModelType], repository: Type[RepositoryType]):
        self.model_class = model
        self.repository = repository
        self._valid_columns = set(self.repository.inspector.c.keys())
        self._has_soft_delete = hasattr(self.model_class, "is_deleted")

    @lru_cache(maxsize=256)
    def _parse_filter_item(self, filter_item: str) -> Tuple[str, str]:
        """Cache parsing filter."""
        try:
            col, value = filter_item.split("=", 1)
            return col.strip(), value.strip()
        except ValueError:
            raise UnprocessableEntity(f"Invalid filter {filter_item} must be 'name=value'")

    @lru_cache(maxsize=256)
    def _parse_sort_item(self, sort_item: str) -> Tuple[str, str]:
        """Cache parsing sort."""
        try:
            col, order = sort_item.split(":", 1)
            return col.strip(), order.strip().lower()
        except ValueError:
            raise UnprocessableEntity(f"Invalid sort {sort_item}. Must be 'name:asc' or 'name:desc'")

    def _validate_column(self, col: str) -> None:
        """Validate column dengan cache."""
        if col not in self._valid_columns:
            raise UnprocessableEntity(f"Invalid column: {col}")

    def _convert_value(self, col: str, value: str) -> Any:
        """Convert value ke tipe yang sesuai."""
        if col == "id":
            try:
                return str(value)
            except ValueError:
                raise UnprocessableEntity(f"Invalid id value: {value}")

        if isinstance(value, str) and value.lower() in {"true", "false", "t", "f"}:
            return value.lower() in {"true", "t"}

        if value.isdigit():
            return int(value)

        try:
            return float(value)
        except ValueError:
            return value

    def _build_filters(self, filters: Union[str, list[str]]) -> List:
        """Build filters dengan optimization."""
        list_model_filters = []

        if isinstance(filters, str):
            filters = [filters]

        if self._has_soft_delete:
            filters.append("is_deleted=false")

        for filter_item in filters:
            if isinstance(filter_item, list):
                or_conditions = []
                for values in filter_item:
                    col, value = self._parse_filter_item(values)
                    self._validate_column(col)
                    converted_value = self._convert_value(col, value)

                    if isinstance(converted_value, bool):
                        or_conditions.append(getattr(self.model_class, col).is_(converted_value))
                    else:
                        or_conditions.append(getattr(self.model_class, col) == converted_value)

                if or_conditions:
                    list_model_filters.append(or_(*or_conditions))
            else:
                col, value = self._parse_filter_item(filter_item)
                self._validate_column(col)
                converted_value = self._convert_value(col, value)

                if isinstance(converted_value, bool):
                    list_model_filters.append(getattr(self.model_class, col).is_(converted_value))
                else:
                    list_model_filters.append(getattr(self.model_class, col) == converted_value)

        return list_model_filters

    def _build_sort(self, sort: Union[str, list[str]]) -> List:
        """Build sort dengan optimization."""
        if not sort:
            return []

        list_sort = []

        if isinstance(sort, str):
            sort = [sort]

        for sort_item in sort:
            col, order = self._parse_sort_item(sort_item)
            self._validate_column(col)

            if order == "asc":
                list_sort.append(getattr(self.model_class, col).asc())
            elif order == "desc":
                list_sort.append(getattr(self.model_class, col).desc())
            else:
                raise UnprocessableEntity(f"Invalid sort order '{order}' for {col}")

        return list_sort

    async def find_by_id(self, id: str, relationships: List[str] = None) -> ModelType:
        """Find record by ID dengan optional eager loading."""
        record = await self.repository.find_by_id(id, relationships=relationships)
        if not record:
            raise NotFoundException(f"{self.model_class.__name__} with id {id} not found.")
        return record

    async def find_all(
        self,
        filters: Union[str, list[str]] = None,
        sort: Union[str, list[str]] = None,
        search: str = "",
        group_by: str = None,
        limit: int = 100,
        offset: int = 0,
        relationships: List[str] = None,
        searchable_columns: List[str] = None,
    ) -> Tuple[List[ModelType], int]:
        """Optimized find_all."""

        if group_by:
            self._validate_column(group_by)

        list_model_filters = self._build_filters(filters or [])
        list_sort = self._build_sort(sort or [])

        return await self.repository.find_all(
            filters=list_model_filters,
            sort=list_sort,
            search=search,
            group_by=group_by,
            limit=limit,
            offset=offset,
            relationships=relationships,
            searchable_columns=searchable_columns,
        )

    async def create(self, data: Dict[str, Any]) -> ModelType:
        """Create new record."""
        return await self.repository.create(data)

    async def update(self, id: str, data: Dict[str, Any], refresh: bool = True) -> ModelType:
        """Update existing record."""
        # Check existence first
        if not await self.repository.exists(id):
            raise NotFoundException(f"{self.model_class.__name__} with id {id} not found.")

        updated = await self.repository.update(id, data, refresh=refresh)
        if not updated:
            raise NotFoundException(f"{self.model_class.__name__} with id {id} not found.")

        return updated

    async def delete(self, id: str, permanent: bool = False) -> None:
        """Delete record dengan soft delete support."""
        if not await self.repository.exists(id):
            raise NotFoundException(f"{self.model_class.__name__} with id {id} not found.")

        if self._has_soft_delete and not permanent:
            delete_data = {"is_deleted": True}
            if hasattr(self.model_class, "is_active"):
                delete_data["is_active"] = False
            await self.repository.update(id, delete_data, refresh=False)
        else:
            await self.repository.delete(id)

    # Bulk operations
    async def bulk_create(self, data_list: List[Dict[str, Any]], batch_size: int = 1000) -> List[ModelType]:
        """Bulk create dengan validation."""
        return await self.repository.bulk_create(data_list, batch_size=batch_size, return_records=True)

    async def exists_by_id(self, id: str) -> bool:
        """Check existence tanpa fetch object."""
        return await self.repository.exists(id)

    async def count_by_filters(self, filters: Union[str, list[str]] = None) -> int:
        """Count records dengan filters."""
        list_model_filters = self._build_filters(filters or [])
        return await self.repository.count(list_model_filters)
