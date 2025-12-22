# ruff: noqa: B008, E501

from typer_di import Depends, TyperDI

from .loaders import ExcelGroupedDataLoader, ExcelSingleRowDataLoader
from .options import (
    MultipleDocxOptions,
    MultipleRowsXlsxOptions,
    Options,
    SingleDocxOptions,
    get_multiple_docx_options,
    get_multiple_rows_xlsx_options,
    get_options,
    get_single_docx_options,
)
from .services import write_templates
from .writers import MultipleDocxTemplateWriter, SingleDocxTemplateWriter

app = TyperDI()


@app.callback()
def main() -> None:
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


@app.command(
    name="xlsx2mdocx",
    help=(
        "Generate multiple docx files from xlsx file (single row)\n"
        "Usage:\n"
        "\n"
        "Table (xlsx for example):\n"
        "\n"
        f"| {'name':<10} | {'age':<4}\n"
        f"| {'Abdullah':<10} | {'32':<4}\n"
        f"| {'Rawaa':<10} | {'33':<4}\n"
        f"| {'Rawaa':<10} | {'33':<4}\n"
        "\n"
        "Template (docx for example):\n"
        "\n"
        "Hello my name is {{ name }}, my age is {{ age }}\n"
        "\n"
        "Command:\n"
        "\n"
        "python manage.py templates xlsx2mdocx \\ \n"
        "-d <your_path_to_xlsx_file> \\ \n"
        "-t <your_path_to_template_file> \\ \n"
        "-o <your_path_to_output_directory> \\ \n"
        "-k name # (the `name` column from xlsx file above) \\ \n"
        "\n"
        "it will generate a multiple docx files like this:\n"
        "\n"
        "1 - Abdullah.docx\n"
        "2 - Rawaa.docx\n"
    ),
)
def generate_multiple_docx_files_from_xlsx_single_row(
    options: Options = Depends(get_options),
    multiple_docx_options: MultipleDocxOptions = Depends(get_multiple_docx_options),
):
    loader = ExcelSingleRowDataLoader(options.data_filepath)
    writer = MultipleDocxTemplateWriter(
        options.template_filepath,
        multiple_docx_options.output_dir,
        multiple_docx_options.filename_key,
        pdf=multiple_docx_options.pdf,
        include_index_in_filename=multiple_docx_options.include_idx_in_filename,
    )

    write_templates(loader, writer)


@app.command(
    name="xlsx2docx",
    help=(
        "Generate docx files from xlsx file (single row)\n"
        "Usage:\n"
        "\n"
        "Table (xlsx for example):\n"
        "\n"
        f"| {'name':<10} | {'age':<4}\n"
        f"| {'Abdullah':<10} | {'32':<4}\n"
        f"| {'Rawaa':<10} | {'33':<4}\n"
        f"| {'Rawaa':<10} | {'33':<4}\n"
        "\n"
        "Template (docx for example):\n"
        "\n"
        "{%p for person in data %}\n"
        "    Hello my name is {{ person['name'] }}, my age is {{ person['age'] }}\n"
        "    {{ page_break }}\n"
        "{%p endfor %}\n"
        "\n"
        "Command:\n"
        "\n"
        "python manage.py templates xlsx2docx \\ \n"
        "-d <your_path_to_xlsx_file> \\ \n"
        "-t <your_path_to_template_file> \\ \n"
        "-o <your_path_to_output_directory> \\ \n"
        "-v name # (the `name` column from xlsx file above) \\ \n"
    ),
)
def generate_single_docx_file_from_xlsx_single_row(
    options: Options = Depends(get_options),
    single_docx_options: SingleDocxOptions = Depends(get_single_docx_options),
):
    loader = ExcelSingleRowDataLoader(options.data_filepath)
    writer = SingleDocxTemplateWriter(
        options.template_filepath,
        single_docx_options.filepath,
        single_docx_options.template_data_variable,
        pdf=single_docx_options.pdf,
    )

    write_templates(loader, writer)


@app.command(
    name="mxlsx2mdocx",
    help=(
        "Generate multiple docx files from xlsx file (multiple rows)\n"
        "Usage:\n"
        "\n"
        "Table (xlsx for example):\n"
        "\n"
        f"| {'name':<10} | {'age':<4} | {'watch_date':<10} | {'watch_time':<10} |\n"
        f"| {'Abdullah':<10} | {'32':<4} | {'12-12-2012':<10} | {'10:45':<10} |\n"
        f"| {'Abdullah':<10} | {'32':<4} | {'13-12-2012':<10} | {'10:45':<10} |\n"
        f"| {'Rawaa':<10} | {'33':<4} | {'14-12-2012':<10} | {'11:45':<10} |\n"
        f"| {'Rawaa':<10} | {'33':<4} | {'15-12-2012':<10} | {'11:45':<10} |\n"
        "\n"
        "Template (docx for example):\n"
        "\n"
        "Hello my name is {{ name }}, my age is {{ age }}\n"
        "My watches is:\n"
        "{%p for watch in watches %}\n"
        "- {{ watch['date'] }} {{ watch['time'] }}\n"
        "{%p endfor %}\n"
        "\n"
        "Command:\n"
        "\n"
        "python manage.py templates mxlsx2mdocx \\ \n"
        "-d <your_path_to_xlsx_file> \\ \n"
        "-t <your_path_to_template_file> \\ \n"
        "-o <your_path_to_output_directory> \\ \n"
        "-k name # (the `name` column from xlsx file above) \\ \n"
        "-c watch_date \\ \n"
        "-c watch_time \\ \n"
        "-g watches \\ \n"
        "-k name \n"
        "\n"
        "it will generate a single docx file like this:\n"
        "\n"
        "1 - Abdullah.docx\n"
        "2 - Rawaa.docx\n"
    ),
)
def generate_docx_multiple_files_from_xlsx_multiple_rows(
    options: Options = Depends(get_options),
    multiple_docx_options: MultipleDocxOptions = Depends(get_multiple_docx_options),
    multiple_rows_xlsx_options: MultipleRowsXlsxOptions = Depends(get_multiple_rows_xlsx_options),
):
    loader = ExcelGroupedDataLoader(
        options.data_filepath,
        multiple_rows_xlsx_options.group_variable,
        *multiple_rows_xlsx_options.grouped_columns,
    )
    write = MultipleDocxTemplateWriter(
        options.template_filepath,
        multiple_docx_options.output_dir,
        multiple_docx_options.filename_key,
        pdf=multiple_docx_options.pdf,
        include_index_in_filename=multiple_docx_options.include_idx_in_filename,
    )

    write_templates(loader, write)


@app.command(
    name="mxlsx2docx",
    help=(
        "Generate multiple docx files from xlsx file (multiple rows)\n"
        "Usage:\n"
        "\n"
        "Table (xlsx for example):\n"
        "\n"
        f"| {'name':<10} | {'age':<4} | {'watch_date':<10} | {'watch_time':<10} |\n"
        f"| {'Abdullah':<10} | {'32':<4} | {'12-12-2012':<10} | {'10:45':<10} |\n"
        f"| {'Abdullah':<10} | {'32':<4} | {'13-12-2012':<10} | {'10:45':<10} |\n"
        f"| {'Rawaa':<10} | {'33':<4} | {'14-12-2012':<10} | {'11:45':<10} |\n"
        f"| {'Rawaa':<10} | {'33':<4} | {'15-12-2012':<10} | {'11:45':<10} |\n"
        "\n"
        "Template (docx for example):\n"
        "\n"
        "{%p for person in data %}\n"
        "Hello my name is {{ person['name'] }}, my age is {{ person['age'] }}\n"
        "My watches is:\n"
        "{%p for watch in person['watches'] %}\n"
        "- {{ watch['date'] }} {{ watch['time'] }}\n"
        "{%p endfor %}\n"
        "{{ page_break }}\n"
        "\n"
        "Command:\n"
        "\n"
        "python manage.py templates mxlsx2mdocx \\ \n"
        "-d <your_path_to_xlsx_file> \\ \n"
        "-t <your_path_to_template_file> \\ \n"
        "-o <your_path_to_output_directory> \\ \n"
        "-k name # (the `name` column from xlsx file above) \\ \n"
        "-c watch_date \\ \n"
        "-c watch_time \\ \n"
        "-g watches "
    ),
)
def generate_single_docx_file_from_xlsx_multiple_rows(
    options: Options = Depends(get_options),
    single_docx_options: SingleDocxOptions = Depends(get_single_docx_options),
    multiple_rows_xlsx_options: MultipleRowsXlsxOptions = Depends(get_multiple_rows_xlsx_options),
):
    loader = ExcelGroupedDataLoader(
        options.data_filepath,
        multiple_rows_xlsx_options.group_variable,
        *multiple_rows_xlsx_options.grouped_columns,
    )
    writer = SingleDocxTemplateWriter(
        options.template_filepath,
        single_docx_options.filepath,
        single_docx_options.template_data_variable,
        pdf=single_docx_options.pdf,
    )

    write_templates(loader, writer)
