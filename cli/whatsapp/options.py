# ruff: noqa: RUF009

from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import pandas as pd
import typer
from typer_di import Depends

from .schemas import Message

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


def _get_messages_from_xlsx(filepath: Path) -> list[Message]:
    messages_dict: dict[str, list[str]] = {}
    data = pd.read_excel(filepath).to_dict(orient="records")

    for row in data:
        phone, text = row.values()

        phone = str(phone)
        text = str(text).replace("_x000D_", "")

        if phone in messages_dict:
            messages_dict[phone].append(text)
        else:
            messages_dict[phone] = [text]

    return [Message(phone, texts) for phone, texts in messages_dict.items()]


FilepathArg = Annotated[
    Path,
    typer.Argument(
        help="Path to xlsx file contains the messages",
    ),
]

UrlOpt = Annotated[
    str,
    typer.Option(
        "--url",
        help="Base url for whatsapp app",
        envvar="WHATSAPP_DEFAULT_BASE_URL",
    ),
]


@dataclass
class Options:
    url: UrlOpt
    messages: list[Message] = Depends(_get_messages_from_xlsx)
    timeout: Timeout = Depends(Timeout)
