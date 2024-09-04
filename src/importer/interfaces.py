import abc
from typing import Any, Generic, Iterator, Type

from importer.types import PydanticModel_T


class FileReader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read(self, data: str | bytes) -> Any: ...


class JsonValidator(Generic[PydanticModel_T], metaclass=abc.ABCMeta):
    pydantic_model = Type[PydanticModel_T]

    def validate(self, item: dict[str, Any]) -> PydanticModel_T:
        data = self.get_data_for_model(item)
        return self.pydantic_model(**data)

    @abc.abstractmethod
    def get_data_for_model(self, item: dict[str, Any]) -> dict[str, Any]: ...


class Saver(Generic[PydanticModel_T], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save(self, items: Iterator[PydanticModel_T]) -> None: ...
