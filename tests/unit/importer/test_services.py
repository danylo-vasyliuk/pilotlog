import json

import pytest

from importer.services import JsonFileReader


class TestJsonFileReader:
    @pytest.fixture
    def service(self) -> JsonFileReader:
        return JsonFileReader()

    def test_read_str(self, service: JsonFileReader) -> None:
        data = '{"a": 1, "b": 2}'
        assert service.read(data) == {"a": 1, "b": 2}

    def test_read_bytes(self, service: JsonFileReader) -> None:
        data = b'{"a": 1, "b": 2}'
        assert service.read(data) == {"a": 1, "b": 2}

    def test_read_invalid(self, service: JsonFileReader) -> None:
        with pytest.raises(json.JSONDecodeError):
            service.read("invalid")
