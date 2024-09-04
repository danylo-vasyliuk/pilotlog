from pathlib import Path

from django.core.files import File
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from importer.services import JsonFileReader, validate_items
from pilotlog.importer.services import PilotlogDBSaver, PilotlogJsonValidator


class ImportSerializer(serializers.Serializer):
    file = serializers.FileField(write_only=True)

    def validate_file(self, file: File) -> File:
        if Path(file.name).suffix != ".json":
            raise ValidationError("Invalid file type")
        return file

    def save(self) -> None:
        file_content = self.validated_data["file"].read()

        reader = JsonFileReader()
        json_validator = PilotlogJsonValidator()
        db_saver = PilotlogDBSaver()

        json_log_records = reader.read(file_content)
        pydantic_log_records = validate_items(
            items=json_log_records, json_validator=json_validator
        )
        db_saver.save(items=pydantic_log_records)
