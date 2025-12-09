from pathlib import Path
from typing import Annotated

import typer

from .services import (
    close_whatsapp_page,
    get_authenticated_whatsapp_page,
    get_messages_from_salaries_file,
    send_whatsapp_messages,
)

app = typer.Typer()


@app.command("send-salaries")
def send_salaries_whatsapp_messages(  # noqa: PLR0913
    filepath: Annotated[
        Path,
        typer.Option(
            "-p",
            "--filepath",
            help="Path to Salaries.xlsb file",
            exists=True,
            file_okay=True,
            dir_okay=False,
            resolve_path=True,
        ),
    ],
    timeout_between_messages: Annotated[
        float,
        typer.Option(
            "--timeout-between-messages",
            help="Timeout between messages",
            envvar="DEFAULT_TIMEOUT_BETWEEN_MESSAGES",
        ),
    ],
    pageload_timeout: Annotated[
        float,
        typer.Option(
            "--pageload-timeout",
            help="Timeout for pageload",
            envvar="DEFAULT_PAGELOAD_TIMEOUT",
        ),
    ],
    password: Annotated[
        str,
        typer.Option(
            "--password",
            help="Password for Salaries.xlsb file",
            hide_input=True,
            prompt="Password for Salaries.xlsb file",
            envvar="SALARIES_EXCEL_FILE_PASSWORD",
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
) -> None:
    """Send whatsapp messages from `whatsapp` sheet in [Salaries|Partials]_[Wages|Overtime]_20****.xlsb file."""  # noqa: E501
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
