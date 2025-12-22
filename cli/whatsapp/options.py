from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

FilepathArgument = Annotated[
    Path,
    typer.Argument(
        help="Path to xlsx file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    ),
]

WhatsappUrlOption = Annotated[
    str,
    typer.Option(
        "--url",
        "--base-url",
        help="Base url for whatsapp app",
        envvar="WHATSAPP_DEFAULT_BASE_URL",
    ),
]

MinMessagesTimeoutOption = Annotated[
    float,
    typer.Option(
        "--min-timeout-between-messages",
        help="Min Timeout between messages in seconds",
        envvar="WHATSAPP_DEFAULT_MIN_TIMEOUT_BETWEEN_MESSAGES",
        rich_help_panel="Timeout",
    ),
]

MaxMessagesTimeoutOption = Annotated[
    float,
    typer.Option(
        "--max-timeout-between-messages",
        help="Max Timeout between messages in seconds",
        envvar="WHATSAPP_DEFAULT_MAX_TIMEOUT_BETWEEN_MESSAGES",
        rich_help_panel="Timeout",
    ),
]

MinSendSelectorTimeoutOption = Annotated[
    float,
    typer.Option(
        "--min-send-selector-timeout",
        help="Min Timeout for send selector in milliseconds",
        envvar="WHATSAPP_DEFAULT_MIN_SEND_SELECTOR_TIMEOUT",
        rich_help_panel="Timeout",
    ),
]

MaxSendSelectorTimeoutOption = Annotated[
    float,
    typer.Option(
        "--max-send-selector-timeout",
        help="Max Timeout for send selector in milliseconds",
        envvar="WHATSAPP_DEFAULT_MAX_SEND_SELECTOR_TIMEOUT",
        rich_help_panel="Timeout",
    ),
]

PageloadTimeoutOption = Annotated[
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
    min_between_messages: MinMessagesTimeoutOption
    max_between_messages: MaxMessagesTimeoutOption
    min_send_selector: MinSendSelectorTimeoutOption
    max_send_selector: MaxSendSelectorTimeoutOption
    pageload: PageloadTimeoutOption


def get_timeout(
    min_between_messages: MinMessagesTimeoutOption,
    max_between_messages: MaxMessagesTimeoutOption,
    min_send_selector: MinSendSelectorTimeoutOption,
    max_send_selector: MaxSendSelectorTimeoutOption,
    pageload: PageloadTimeoutOption,
) -> Timeout:
    return Timeout(
        min_between_messages, max_between_messages, min_send_selector, max_send_selector, pageload
    )
