# ruff: noqa: FBT002, E501
from pathlib import Path

import typer

from .options import (
    DataPathOption,
    OutputDirOption,
    PDFOption,
    TemplatePathOption,
)

DEFAULT_OUTPUT_DESKTOP_DIRNAME = "output"


def make_output_dir(dir_name: str, output_dir: Path | None = None) -> Path:
    if output_dir is None:
        output_dir = Path().home() / "Desktop" / dir_name

    if not output_dir.exists():
        output_dir.absolute().mkdir(parents=True)

    return output_dir


def app_callback(
    ctx: typer.Context,
    data_filepath: DataPathOption,
    template: TemplatePathOption,
    output_dir: OutputDirOption = None,
    pdf: PDFOption = False,
):
    """Generate docx files from xlsx files.

    Tags:
    In order to manage paragraphs, table rows, table columns, runs, special syntax has to be used:\n\n
      {%p jinja2_tag %} for paragraphs\n
      {%tr jinja2_tag %} for table rows\n
      {%tc jinja2_tag %} for table columns\n
      {%r jinja2_tag %} for runs\n
    \n
    By using these tags, python-docx-template will take care to put the real jinja2 tags (without the p, tr, tc or r) at the right place into the document's xml source code. In addition, these tags also tell python-docx-template to remove the paragraph, table row, table column or run where the tags are located.\n
    \n
    For example, if you have this kind of template:\n
      {%p if display_paragraph %}\n
      One or many paragraphs\n
      {%p endif %}\n
    \n

    Split and merge text:\n\n

    You can merge a jinja2 tag with previous line by using {%-\n\n

    You can merge a jinja2 tag with next line by using -%}\n\n

    A text containing Jinja2 tags may be unreadable if too long:\n\n

    My house is located {% if living_in_town %} in urban area {% else %} in countryside {% endif %} and I love it.\n\n
    One can use ENTER or SHIFT+ENTER to split a text like below, then use {%- and -%} to tell docxtpl to merge the whole thing:\n\n

    My house is located\n
    {%- if living_in_town -%}\n
     in urban area\n
    {%- else -%}\n
     in countryside\n
    {%- endif -%}\n
     and I love it.\n\n

    IMPORTANT : Use an unbreakable space (CTRL+SHIFT+SPACE) when a space is wanted at line beginning or ending.\n\n

    IMPORTANT 2 : {%- xxx -%} tags must be alone in a line : do not add some text before or after on the same line.\n\n

    Additional context:\n
      {{ new_line }} for new line\n
      {{ tab }} for tab\n
      {{ page_break }} for page break\n
    """  # noqa: D301
    ctx.obj = {
        "data_filepath": data_filepath,
        "template": template,
        "output_dir": make_output_dir(
            DEFAULT_OUTPUT_DESKTOP_DIRNAME, output_dir
        ),
        "pdf": pdf,
    }
