from typing import Protocol

from .schemas import Data


class Reader(Protocol):
    def read(self) -> Data: ...


class TemplateWriter(Protocol):
    def write(self, data: Data) -> None: ...


def write_templates(reader: Reader, writer: TemplateWriter) -> None:
    data = reader.read()
    writer.write(data=data)
