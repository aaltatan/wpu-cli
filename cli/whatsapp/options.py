from dataclasses import InitVar, dataclass, field
from pathlib import Path
from typing import Annotated

import typer

from .loaders import get_messages_from_xlsx
from .schemas import Message

FilepathArg = Annotated[
    Path,
    typer.Argument(
        help="Path to xlsx file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    ),
]

WhatsappUrlOpt = Annotated[
    str,
    typer.Option(
        "--url",
        "--base-url",
        help="Base url for whatsapp app",
        envvar="WHATSAPP_DEFAULT_BASE_URL",
    ),
]

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


def get_timeout(
    min_between_messages: MinMessagesTimeoutOpt,
    max_between_messages: MaxMessagesTimeoutOpt,
    min_send_selector: MinSendSelectorTimeoutOpt,
    max_send_selector: MaxSendSelectorTimeoutOpt,
    pageload: PageloadTimeoutOpt,
) -> Timeout:
    return Timeout(
        min_between_messages, max_between_messages, min_send_selector, max_send_selector, pageload
    )


@dataclass
class WhatsappOptions:
    filepath: InitVar[FilepathArg]
    url: WhatsappUrlOpt

    messages: list[Message] = field(init=False)

    def __post_init__(self, filepath: FilepathArg) -> None:
        self.messages = get_messages_from_xlsx(filepath)


def get_whatsapp_options(filepath: FilepathArg, url: WhatsappUrlOpt) -> WhatsappOptions:
    return WhatsappOptions(filepath, url)
