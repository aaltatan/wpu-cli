from typing import Annotated

import typer

from cli.utils import get_salaries_filepath

from .services import (
    get_authenticated_whatsapp_page,
    get_messages_from_excel,
    send_whatsapp_messages,
)

app = typer.Typer()


@app.command()
def send_salaries(
    password: Annotated[
        str,
        typer.Option(
            "--password",
            help="Password for Salaries.xlsb file",
            hide_input=True,
            prompt=True,
            envvar="EXCEL_FILE_PASSWORD",
        ),
    ],
    first_cell: Annotated[
        tuple[int, int],
        typer.Option(
            default_factory=lambda: (1, 2),
            help="Start cell in Salaries.xlsb file",
        ),
    ],
    sheet_name: Annotated[
        str,
        typer.Option("--sheet", help="Sheet name in Salaries.xlsb file"),
    ] = "whatsapp",
    last_column: Annotated[
        int,
        typer.Option("--last-column", help="Last column in Salaries.xlsb file"),
    ] = 3,
    timeout: Annotated[
        float,
        typer.Option("--timeout", "-t", help="Timeout between messages"),
    ] = 2,
):
    """Send whatsapp messages from `whatsapp` sheet in [Salaries|Partials]_[Wages|Overtime]_20****.xlsb file."""  # noqa: E501
    filepath = get_salaries_filepath()
    page = get_authenticated_whatsapp_page()
    messages = get_messages_from_excel(
        filepath,
        password=password,
        sheet_name=sheet_name,
        first_cell=first_cell,
        last_column=last_column,
    )
    send_whatsapp_messages(page, messages, timeout)
