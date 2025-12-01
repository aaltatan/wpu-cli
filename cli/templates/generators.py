from pathlib import Path
from typing import Any
from uuid import uuid4

from docx2pdf import convert
from docxtpl import DocxTemplate
from rich.progress import track

from .types import Data

ADDITIONAL_CONTEXT = {
    "new_line": "\n",
    "tab": "\t",
    "page_break": "\f",
}


def _generate_filepath(filename: str, output_dir: Path, extension: str) -> Path:
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    filepath = output_dir / f"{filename}.{extension}"

    if filepath.exists():
        new_filename = f"{filename}-{uuid4().hex}"
        filepath = _generate_filepath(new_filename, output_dir, extension)

        if not isinstance(filepath, Path):
            message = "Unexpected filepath type"
            raise ValueError(message)

        return filepath

    return filepath


class MultipleDocxTemplateGenerator:
    def __init__(
        self,
        template_path: Path,
        output_dir: Path,
        filename_key: str | None = None,
        *,
        pdf: bool = False,
        include_index_in_filename: bool = False,
    ) -> None:
        self.template = DocxTemplate(template_path)
        self.output_dir = output_dir
        self.filename_key = filename_key
        self.pdf = pdf
        self.include_index_in_filename = include_index_in_filename

    def _get_filename(
        self,
        item: dict[Any, Any],
        idx: int,
        filename_key: str | None = None,
    ) -> str:
        filename = f"template-{idx}"

        if filename_key and filename_key in item:
            filename = item[filename_key]

            if self.include_index_in_filename:
                filename = f"{idx}-{item[filename_key]}"

        return filename

    def generate(self, data: Data) -> None:
        for idx, item in track(
            enumerate(data, start=1),
            description="📝 Generating",
            total=len(data),
        ):
            filename = self._get_filename(item, idx, self.filename_key)
            filepath = _generate_filepath(
                filename,
                self.output_dir if not self.pdf else self.output_dir / "docx",
                "docx",
            )

            self.template.render({**item, **ADDITIONAL_CONTEXT})
            self.template.save(filepath)

            if self.pdf:
                output_dir = self.output_dir / "pdf"
                if not output_dir.exists():
                    output_dir.mkdir(parents=True)

                convert(filepath, output_dir)


class SingleDocxTemplateGenerator:
    def __init__(
        self,
        template_path: Path,
        output_dir: Path,
        filename: str,
        data_key: str,
        *,
        pdf: bool = False,
    ) -> None:
        self.template = DocxTemplate(template_path)
        self.output_dir = output_dir
        self.filename = filename
        self.data_key = data_key
        self.pdf = pdf

    def generate(self, data: Data) -> None:
        filepath = _generate_filepath(self.filename, self.output_dir, "docx")

        self.template.render({self.data_key: data, **ADDITIONAL_CONTEXT})
        self.template.save(filepath)

        if self.pdf:
            convert(filepath, self.output_dir)
