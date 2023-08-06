
from typing import Any, List, Optional, TypeVar, TypedDict

from wcd_geo_db.const import DivisionLevel, DivisionType


__all__ = 'DivisionSource',


class DivisionSource(TypedDict):
    code: Any
    path: List[Any]
    name: Optional[str]
    types: List[DivisionType]
    level: DivisionLevel
