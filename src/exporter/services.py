import csv
from typing import Any, Iterable, Iterator

from exporter.interfaces import TemplateRenderer, Writer
from exporter.types import Template


class Echo:
    def write(self, value: Any) -> Any:
        return value


class CSVWriter(Writer):
    def __init__(self):
        self.pseudo_buffer = Echo()

    def write(self, data: Iterable[Any]) -> Iterator[Any]:
        writer = csv.writer(self.pseudo_buffer)
        for row in data:
            yield writer.writerow(row)


class CSVTemplateRenderer(TemplateRenderer):
    def render(self, template: Template) -> Iterator[list[Any]]:
        columns_num = max(len(table.headers) for table in template.tables) or 1

        yield [template.name] + self.get_empty_line(columns_num - 1)
        yield self.get_empty_line(columns_num)

        for table in template.tables:
            # code here
            index_to_comment = {
                i: header.comment
                for i, header in enumerate(table.headers)
                if header.comment is not None
            }
            # table name and comments
            yield [table.name] + [
                index_to_comment.get(i + 1, "") for i in range(columns_num - 1)
            ]
            # column types
            yield [header.field_type.value for header in table.headers]
            # column names
            yield [header.name for header in table.headers]

            # rows
            for row in table.rows:
                yield [row.get(header.name, "") for header in table.headers]

            yield self.get_empty_line(columns_num)

    @staticmethod
    def get_empty_line(columns_num: int) -> list[str]:
        return [""] * columns_num
