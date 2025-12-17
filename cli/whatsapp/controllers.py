from pathlib import Path
from typing import Annotated

import typer

from .services import (
    WhatsappSender,
    get_authenticated_whatsapp_page,
    get_messages_from_xlsx,
)

app = typer.Typer()


@app.callback()
def main():
    """Send whatsapp bulk messages using playwright."""


@app.command("send")
def send_messages(
    filepath: Annotated[
        Path,
        typer.Option(
            "-p",
            "--filepath",
            help="Path to xlsx file",
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
) -> None:
    """Send whatsapp messages from xlsx file (You should have a file with two columns: phone number and message)."""  # noqa: E501
    playwright, browser, context, page = get_authenticated_whatsapp_page()

    with WhatsappSender(
        playwright,
        browser,
        context,
        page,
        timeout_between_messages,
        pageload_timeout,
    ) as sender:
        sender.send(messages=get_messages_from_xlsx(filepath))
