from typing import TypeVar

from pydantic import BaseModel


PydanticModel_T = TypeVar("PydanticModel_T", bound=BaseModel)


class Entity(BaseModel):
    pass
