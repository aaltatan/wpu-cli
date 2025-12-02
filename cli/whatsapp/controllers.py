from typing import Annotated

import typer

from cli.utils import get_salaries_filepath

from .services import (
    close_whatsapp_page,
    get_authenticated_whatsapp_page,
    get_messages_from_salaries_file,
    send_whatsapp_messages,
)

app = typer.Typer()


@app.command("send-salaries")
def send_salaries_whatsapp_messages(  # noqa: PLR0913
    password: Annotated[
        str,
        typer.Option(
            "--password",
            help="Password for Salaries.xlsb file",
            hide_input=True,
            prompt="Password for Salaries.xlsb file",
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
    timeout_between_messages: Annotated[
        float,
        typer.Option(
            "--timeout-between-messages", help="Timeout between messages"
        ),
    ] = 2,
    pageload_timeout: Annotated[
        float,
        typer.Option(
            "--pageload-timeout",
            help="Timeout for pageload",
        ),
    ] = 10_000,
) -> None:
    """Send whatsapp messages from `whatsapp` sheet in [Salaries|Partials]_[Wages|Overtime]_20****.xlsb file."""  # noqa: E501
    filepath = get_salaries_filepath()

    playwright, browser, context, page = get_authenticated_whatsapp_page()

    messages = get_messages_from_salaries_file(
        filepath,
        password=password,
        sheet_name=sheet_name,
        first_cell=first_cell,
        last_column=last_column,
    )
    send_whatsapp_messages(
        page, messages, timeout_between_messages, pageload_timeout
    )

    close_whatsapp_page(playwright, browser, context, page)
