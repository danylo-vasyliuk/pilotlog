import pytest

from exporter.services import CSVWriter, CSVTemplateRenderer
from exporter.types import Template, Table, Header, HeaderFieldType


class TestCSVWriter:
    @pytest.fixture
    def service(self) -> CSVWriter:
        return CSVWriter()

    def test_write(self, service: CSVWriter) -> None:
        data = [["a", "b"], [1, 2], [3, 4]]
        assert list(service.write(data)) == ["a,b\r\n", "1,2\r\n", "3,4\r\n"]


class TestCSVTemplateRenderer:
    @pytest.fixture
    def service(self) -> CSVTemplateRenderer:
        return CSVTemplateRenderer()

    @pytest.fixture
    def template(self) -> Template:
        return Template(
            name="Test Template",
            tables=[
                Table(
                    name="Test Table",
                    headers=[
                        Header(name="a", field_type=HeaderFieldType.NUMBER),
                        Header(
                            name="b",
                            field_type=HeaderFieldType.TEXT,
                            comment="b_test_comment",
                        ),
                    ],
                    rows=[
                        {
                            "a": 1,
                            "b": 2,
                        }
                    ],
                )
            ],
        )

    def test_render(self, service: CSVTemplateRenderer, template: Template) -> None:
        expected = [
            ["Test Template", ""],
            ["", ""],
            ["Test Table", "b_test_comment"],
            ["Number", "Text"],
            ["a", "b"],
            [1, 2],
            ["", ""],
        ]
        actual = list(service.render(template=template))
        assert expected == actual

    def test_big_number_of_headers(
        self, service: CSVTemplateRenderer, template: Template
    ) -> None:
        number_of_columns = 1000
        template = template.model_copy(deep=True)
        template.tables[0].headers = [
            Header(name=f"name_{i}", field_type=HeaderFieldType.TEXT)
            for i in range(number_of_columns)
        ]

        assert len(list(service.render(template=template))[0]) == number_of_columns
