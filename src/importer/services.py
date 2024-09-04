import json
from typing import Any, Iterator

from importer.interfaces import FileReader, JsonValidator
from importer.types import PydanticModel_T


class JsonFileReader(FileReader):
    def read(self, data: str | bytes) -> Any:
        if isinstance(data, bytes):
            data = data.decode()
        return json.loads(data.replace('\\"', '"'))


def validate_items(
    items: list[dict[str, Any]], json_validator: JsonValidator[PydanticModel_T]
) -> Iterator[PydanticModel_T]:
    for item in items:
        yield json_validator.validate(item)
