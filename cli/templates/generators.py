from pathlib import Path
from uuid import uuid4

from docxtpl import DocxTemplate
from rich.progress import track

from .types import Data


def _generate_filepath(filename: str, output_dir: Path, extension: str) -> Path:
    filepath = output_dir / f"{filename}.{extension}"

    if filepath.exists():
        new_filename = f"{filename}-{uuid4().hex}"
        filepath = _generate_filepath(new_filename, output_dir, extension)

        if not isinstance(filepath, Path):
            message = "Unexpected filepath type"
            raise ValueError(message)

        return filepath

    return filepath


class DocxTemplateGenerator:
    def __init__(
        self,
        template_path: Path,
        output_dir: Path,
        *,
        include_index_in_filename: bool = False,
    ) -> None:
        self.template = DocxTemplate(template_path)
        self.output_dir = output_dir
        self.include_index_in_filename = include_index_in_filename

    def generate(self, data: Data, filename_key: str | None = None) -> None:
        for idx, item in track(
            enumerate(data, start=1),
            description="📝 Generating",
            total=len(data),
        ):
            filename = f"template-{idx}"

            if filename_key and filename_key in item:
                filename = item[filename_key]

                if self.include_index_in_filename:
                    filename = f"{idx}-{item[filename_key]}"

            filepath = _generate_filepath(filename, self.output_dir, "docx")

            self.template.render(item)
            self.template.save(filepath)
