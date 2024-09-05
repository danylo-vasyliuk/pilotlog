from enum import StrEnum
from typing import Any, Iterable

from pydantic import BaseModel


class HeaderFieldType(StrEnum):
    TEXT = "Text"
    NUMBER = "Number"
    YEAR = "YYYY"
    BOOLEAN = "Boolean"
    DATE = "Date"
    TIME = "hhmm"
    DECIMAL = "Decimal"
    PACKED_DETAIL = "Packed Detail"
    DATE_TIME = "DateTime"


class Header(BaseModel):
    name: str
    field_type: HeaderFieldType
    comment: str | None = None


class Table(BaseModel):
    name: str
    headers: list[Header]
    rows: list[dict[str, Any]]


class Template(BaseModel):
    name: str
    tables: list[Table]
