from collections import defaultdict
from typing import Any, Iterator, Type
from uuid import UUID

from django.db import transaction
from django.db.models import Model
from pydantic import BaseModel

from importer.interfaces import JsonValidator, Saver
from importer.types import Entity
from pilotlog.importer.entities import (
    AirCraftEntity,
    AirFieldEntity,
    FlightEntity,
    ImagePicEntity,
    LimitRulesEntity,
    LogRecordEntity,
    MyQueryBuildEntity,
    MyQueryEntity,
    PilotEntity,
    QualificationEntity,
    SettingConfigEntity,
    TableType,
)
from pilotlog.models import (
    Aircraft,
    AirField,
    Flight,
    ImagePic,
    LimitRules,
    LogRecord,
    MyQuery,
    MyQueryBuild,
    Pilot,
    Qualification,
    SettingConfig,
)


class PilotlogJsonValidator(JsonValidator[LogRecordEntity]):
    pydantic_model = LogRecordEntity
    TABLE_TYPE_TO_ENTITY: dict[TableType, Type[Entity]] = {
        TableType.AIRFIELD: AirFieldEntity,
        TableType.AIRCRAFT: AirCraftEntity,
        TableType.PILOT: PilotEntity,
        TableType.FLIGHT: FlightEntity,
        TableType.IMAGE_PIC: ImagePicEntity,
        TableType.LIMIT_RULES: LimitRulesEntity,
        TableType.MY_QUERY: MyQueryEntity,
        TableType.MY_QUERY_BUILD: MyQueryBuildEntity,
        TableType.QUALIFICATION: QualificationEntity,
        TableType.SETTING_CONFIG: SettingConfigEntity,
    }

    def get_data_for_model(self, item: dict[str, Any]) -> dict[str, Any]:
        table = item["table"].lower()
        return {
            **item,
            "table": table,
            "meta": self.TABLE_TYPE_TO_ENTITY[table](**item["meta"]),
        }


class ModelWithSaveParams(BaseModel):
    db_model: Type[Model]
    fk_fields: dict[str, str] = {}  # model_field: entity_field
    m2m_fields: dict[str, tuple[str, ...]] = {}  # model_field: (entity_field, ...)


class PilotlogDBSaver(Saver[LogRecordEntity]):
    """
    Saver class responsible for saving pilotlog model instances to the database.

    It uses the `TABLE_TYPE_TO_MODEL` mapping to map each table type to the
    corresponding Django model.
    """

    TABLE_TYPE_TO_MODEL = {
        TableType.AIRFIELD: ModelWithSaveParams(db_model=AirField),
        TableType.AIRCRAFT: ModelWithSaveParams(db_model=Aircraft),
        TableType.PILOT: ModelWithSaveParams(db_model=Pilot),
        TableType.FLIGHT: ModelWithSaveParams(
            db_model=Flight,
            fk_fields={
                "aircraft_id": "aircraft_code",
                "arr_id": "arr_code",
                "dep_id": "dep_code",
                "p1_id": "p1_code",
                "p2_id": "p2_code",
                "p3_id": "p3_code",
                "p4_id": "p4_code",
            },
        ),
        TableType.IMAGE_PIC: ModelWithSaveParams(db_model=ImagePic),
        TableType.LIMIT_RULES: ModelWithSaveParams(db_model=LimitRules),
        TableType.MY_QUERY: ModelWithSaveParams(db_model=MyQuery),
        TableType.MY_QUERY_BUILD: ModelWithSaveParams(
            db_model=MyQueryBuild, fk_fields={"my_query_id": "my_query_code"}
        ),
        TableType.QUALIFICATION: ModelWithSaveParams(
            db_model=Qualification, fk_fields={"ref_airfield_id": "ref_airfield_code"}
        ),
        TableType.SETTING_CONFIG: ModelWithSaveParams(db_model=SettingConfig),
    }

    @transaction.atomic
    def save(self, items: Iterator[LogRecordEntity]) -> None:
        log_records_to_create: list[LogRecord] = []
        # {table_name: {code: {fk_field_name: value} } }
        meta_items_to_adjust_fk = {
            table: {}
            for table, model_with_save_params in self.TABLE_TYPE_TO_MODEL.items()
            if model_with_save_params.fk_fields
        }
        db_model_to_db_entities_to_create: dict[Type[Model], list[Model]] = defaultdict(
            list
        )

        for item in items:
            meta = item.meta

            # create LogRecord instance
            log_records_to_create.append(
                LogRecord(
                    **self.prepare_entity_for_save(
                        item,
                        keys_mapping={"record_modified": "modified"},
                        exclude_fields={"meta"},
                    )
                )
            )

            # Exclude pydantic fields for db model
            # Store meta item code with related fk codes to adjust foreign keys
            model_with_save_params = self.TABLE_TYPE_TO_MODEL[item.table]
            exclude_fields_for_db_model = set(model_with_save_params.fk_fields.values())
            if exclude_fields_for_db_model:
                meta_items_to_adjust_fk[item.table][meta.code] = meta.model_dump(
                    include=exclude_fields_for_db_model
                )

            # Create meta db model instance
            db_model_to_db_entities_to_create[model_with_save_params.db_model].append(
                model_with_save_params.db_model(
                    **self.prepare_entity_for_save(
                        meta,
                        exclude_fields=exclude_fields_for_db_model,
                    )
                )
            )

        # save instances to db
        LogRecord.objects.bulk_create(
            log_records_to_create,
            batch_size=2_000,
            unique_fields=["guid", "table"],
            ignore_conflicts=True,
        )
        for (
            db_model,
            db_entities_to_create,
        ) in db_model_to_db_entities_to_create.items():
            db_model.objects.bulk_create(db_entities_to_create, batch_size=2_000)

        self.adjust_relations(meta_items_to_adjust_fk)

    @staticmethod
    def prepare_entity_for_save(
        item: Entity,
        keys_mapping: dict[str, str] | None = None,
        exclude_fields: set[str] | None = None,
    ) -> dict[str, Any]:
        data = item.model_dump(exclude=exclude_fields)
        for old_key, new_key in (keys_mapping or {}).items():
            data[new_key] = data.pop(old_key)
        return data

    def adjust_relations(
        self,
        meta_items_to_adjust_fk: dict[TableType, dict[str, dict[str, UUID | str]]],
    ) -> None:
        for table, meta_items in meta_items_to_adjust_fk.items():
            model_with_save_params = self.TABLE_TYPE_TO_MODEL[table]
            db_model = model_with_save_params.db_model
            entity_field_to_fk_field = {
                v: k for k, v in model_with_save_params.fk_fields.items()
            }

            # Fetch all entities that will be updated in a single query
            db_entities = db_model.objects.in_bulk(meta_items.keys())

            # Fetch all related objects
            related_model_ids = defaultdict(tuple)
            for fk_field in entity_field_to_fk_field.values():
                related_model_ids[fk_field] = tuple(
                    db_model._meta.get_field(fk_field)
                    .remote_field.model.objects.in_bulk()
                    .keys()
                )

            # set all FK fields
            for code, fk_values in meta_items.items():
                for entity_field, fk_value in fk_values.items():
                    if entity_field in entity_field_to_fk_field:
                        fk_field = entity_field_to_fk_field[entity_field]
                        if fk_value in related_model_ids[fk_field]:
                            setattr(db_entities[code], fk_field, fk_value)

            # Save all entities
            db_model.objects.bulk_update(
                db_entities.values(), fields=list(entity_field_to_fk_field.values())
            )
