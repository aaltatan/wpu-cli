from dataclasses import dataclass
from typing import Annotated

import typer

RICH_HELP_PANEL = "Multiple Rows xlsx Options"

GroupedColumnsOption = Annotated[
    list[str],
    typer.Option(
        "-c",
        "--column",
        help="Column to be grouped by",
        rich_help_panel=RICH_HELP_PANEL,
    ),
]

GroupKeyVariable = Annotated[
    str,
    typer.Option(
        "-g",
        "--group-variable",
        help="Group (Iterable) variable to use it in template e.g.: {%p for item in data %}",
        envvar="TEMPLATES_DEFAULT_XLSX_MULTIPLE_ROWS_TEMPLATE_GROUP_VARIABLE",
        rich_help_panel=RICH_HELP_PANEL,
    ),
]


@dataclass
class MultipleRowsXlsxOptions:
    grouped_columns: GroupedColumnsOption
    group_variable: GroupKeyVariable


def get_multiple_rows_xlsx_options(
    grouped_columns: GroupedColumnsOption,
    group_variable: GroupKeyVariable,
) -> MultipleRowsXlsxOptions:
    return MultipleRowsXlsxOptions(grouped_columns, group_variable)
