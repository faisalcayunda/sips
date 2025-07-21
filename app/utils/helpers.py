from typing import Any

import orjson


def orm_to_dict(orm_instance):
    """Convert SQLAlchemy ORM instance to dictionary."""
    if orm_instance is None:
        return None

    result = {}
    for key in orm_instance.__mapper__.c.keys():
        result[key] = getattr(orm_instance, key)

    # Handle relationships if needed
    for relationship in orm_instance.__mapper__.relationships:
        rel_name = relationship.key
        rel_value = getattr(orm_instance, rel_name)
        if rel_value is not None:
            # Check if it's a collection
            if hasattr(rel_value, "__iter__") and not isinstance(rel_value, str):
                result[rel_name] = [orm_to_dict(item) for item in rel_value]
            else:
                result[rel_name] = orm_to_dict(rel_value)

    return result


def orjson_dumps(__obj: Any, *, default=None) -> str:
    """Custom JSON serializer using orjson."""
    return orjson.dumps(
        __obj,
        default=default,
        option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SERIALIZE_UUID | orjson.OPT_UTC_Z,
    ).decode("utf-8")
