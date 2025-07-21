from typing import Any, Dict

from sqlalchemy.orm import declarative_base

from app.utils.helpers import orm_to_dict


class Base(declarative_base()):
    __abstract__ = True

    def to_dict(self) -> Dict[str, Any]:
        return orm_to_dict(self)
