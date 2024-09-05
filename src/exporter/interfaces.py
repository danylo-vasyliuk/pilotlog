import abc
from typing import Any, Iterable, Iterator

from exporter.types import Template


class Writer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def write(self, data: Iterable[Any]) -> Iterator[Any]: ...


class TemplateRenderer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def render(self, template: Template) -> Iterator[list[Any]]: ...
