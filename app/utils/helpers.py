from typing import Any, AsyncGenerator, BinaryIO, Dict, Optional

import orjson
from fastapi import Request

from app.core.security import decode_token


def orm_to_dict(orm_instance: Any) -> Optional[Dict[str, Any]]:
    """Convert SQLAlchemy ORM instance to dictionary."""
    if orm_instance is None:
        return None

    result: Dict[str, Any] = {}

    # Handle basic attributes
    for key in orm_instance.__mapper__.c.keys():
        result[key] = getattr(orm_instance, key)

    # Handle relationships if needed
    for relationship in orm_instance.__mapper__.relationships:
        rel_name = relationship.key
        rel_value = getattr(orm_instance, rel_name)
        if rel_value is not None:
            # Check if it's a collection
            if hasattr(rel_value, "__iter__") and not isinstance(rel_value, (str, bytes)):
                result[rel_name] = [orm_to_dict(item) for item in rel_value]
            else:
                result[rel_name] = orm_to_dict(rel_value)

    return result


def orjson_dumps(__obj: Any, *, default: Optional[Any] = None) -> str:
    """Custom JSON serializer using orjson."""
    return orjson.dumps(
        __obj,
        default=default,
        option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SERIALIZE_UUID | orjson.OPT_UTC_Z,
    ).decode("utf-8")


async def iterfile(file_content: BinaryIO) -> AsyncGenerator[bytes, None]:
    """Iterate over file content in chunks."""
    try:
        chunk = await file_content.content.read(8192)
        while chunk:
            yield chunk
            chunk = await file_content.content.read(8192)
    finally:
        await file_content.release()


def safe_get_attr(obj: Any, attr: str, default: Any = None) -> Any:
    """Safely get attribute from object with fallback."""
    try:
        return getattr(obj, attr, default)
    except (AttributeError, TypeError):
        return default


def validate_required_fields(data: Dict[str, Any], required_fields: list) -> None:
    """Validate that required fields are present in data."""
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")


def generate_incremental_id(existing_ids: list[str]) -> str:
    """
    Generate a new incremental numeric ID based on the largest existing numeric ID in the list.
    Assumes IDs are numeric strings. Returns the next ID as a string.
    """
    if not existing_ids:
        return "1"
    numeric_ids = [int(i) for i in existing_ids if i.isdigit()]
    if not numeric_ids:
        return "1"
    max_id = max(numeric_ids)
    return str(max_id + 1)


async def auth_from_jwt(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return  # guest
    token = auth.split(" ", 1)[1]
    try:
        payload = decode_token(token)
        request.state.user_id = str(payload.get("sub"))
    except:
        # Token jelek → tetap dianggap guest (biar rate limit jatuh ke IP)
        return
