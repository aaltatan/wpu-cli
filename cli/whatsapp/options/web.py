# ruff: noqa: RUF009

from dataclasses import dataclass
from typing import Annotated

import typer
from typer_di import Depends

from cli.whatsapp.readers import read_messages_from_xlsx
from cli.whatsapp.schemas import Message

from ._options import FilepathArg

MinMessagesTimeoutOpt = Annotated[
    float,
    typer.Option(
        "--min-timeout-between-messages",
        help="Min Timeout between messages in seconds",
        envvar="WHATSAPP_DEFAULT_MIN_TIMEOUT_BETWEEN_MESSAGES",
        rich_help_panel="Timeout",
    ),
]

MaxMessagesTimeoutOpt = Annotated[
    float,
    typer.Option(
        "--max-timeout-between-messages",
        help="Max Timeout between messages in seconds",
        envvar="WHATSAPP_DEFAULT_MAX_TIMEOUT_BETWEEN_MESSAGES",
        rich_help_panel="Timeout",
    ),
]

MinSendSelectorTimeoutOpt = Annotated[
    float,
    typer.Option(
        "--min-send-selector-timeout",
        help="Min Timeout for send selector in milliseconds",
        envvar="WHATSAPP_DEFAULT_MIN_SEND_SELECTOR_TIMEOUT",
        rich_help_panel="Timeout",
    ),
]

MaxSendSelectorTimeoutOpt = Annotated[
    float,
    typer.Option(
        "--max-send-selector-timeout",
        help="Max Timeout for send selector in milliseconds",
        envvar="WHATSAPP_DEFAULT_MAX_SEND_SELECTOR_TIMEOUT",
        rich_help_panel="Timeout",
    ),
]

PageloadTimeoutOpt = Annotated[
    float,
    typer.Option(
        "--pageload-timeout",
        help="Timeout for pageload in milliseconds",
        envvar="WHATSAPP_DEFAULT_PAGELOAD_TIMEOUT",
        rich_help_panel="Timeout",
    ),
]


@dataclass
class Timeout:
    min_between_messages: MinMessagesTimeoutOpt
    max_between_messages: MaxMessagesTimeoutOpt
    min_send_selector: MinSendSelectorTimeoutOpt
    max_send_selector: MaxSendSelectorTimeoutOpt
    pageload: PageloadTimeoutOpt


UrlOpt = Annotated[
    str,
    typer.Option(
        "--url",
        help="Base url for whatsapp app",
        envvar="WHATSAPP_DEFAULT_BASE_URL",
    ),
]


def _read_messages_from_xlsx_wrapper(filepath: FilepathArg) -> list[Message]:
    return read_messages_from_xlsx(filepath)


@dataclass
class WebOptions:
    url: UrlOpt
    messages: list[Message] = Depends(_read_messages_from_xlsx_wrapper)
    timeout: Timeout = Depends(Timeout)
