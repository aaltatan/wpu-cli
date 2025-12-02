from pathlib import Path
from typing import Protocol

from .types import Data


class Loader(Protocol):
    def load(self) -> Data: ...


class TemplateGenerator(Protocol):
    def generate(self, data: Data) -> None: ...


def make_output_dir(dir_name: str, output_dir: Path | None = None) -> Path:
    if output_dir is None:
        output_dir = Path().home() / "Desktop" / dir_name

    if not output_dir.exists():
        output_dir.absolute().mkdir(parents=True)

    return output_dir


def generate_templates(loader: Loader, generator: TemplateGenerator) -> None:
    data = loader.load()
    generator.generate(data=data)
