from typing import Protocol

from .schemas import Data


class Loader(Protocol):
    def load(self) -> Data: ...


class TemplateWriter(Protocol):
    def write(self, data: Data) -> None: ...


def write_templates(loader: Loader, writer: TemplateWriter) -> None:
    data = loader.load()
    writer.write(data=data)
