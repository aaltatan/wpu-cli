from dataclasses import dataclass
from typing import Annotated

import typer

from cli.whatsapp.options import FilepathArg
from cli.whatsapp.readers import read_messages_from_xlsx

from .readers import get_desktop_whatsapp_hyperlinks

CheckingLoopOpt = Annotated[
    int,
    typer.Option(
        "-t",
        "--timeout",
        help="Timeout for checking send status in milliseconds",
        envvar="WHATSAPP_DESKTOP_DEFAULT_CHECKING_LOOP",
        rich_help_panel="Timeout",
    ),
]

AfterOpeningOpt = Annotated[
    float,
    typer.Option(
        "--after-opening-timeout",
        help="Timeout for opening hyperlink in milliseconds",
        envvar="WHATSAPP_DESKTOP_DEFAULT_AFTER_OPENING",
        rich_help_panel="Timeout",
    ),
]

BetweenMessagesOpt = Annotated[
    float,
    typer.Option(
        "--between-messages-timeout",
        help="Timeout between messages in milliseconds",
        envvar="WHATSAPP_DESKTOP_DEFAULT_BETWEEN_MESSAGES",
        rich_help_panel="Timeout",
    ),
]


@dataclass
class Timeout:
    checking_loop: int = 15
    after_opening: float = 2
    between_messages: float = 1


def get_desktop_whatsapp_hyperlinks_wrapper(filepath: FilepathArg) -> list[str]:
    messages = read_messages_from_xlsx(filepath)
    return get_desktop_whatsapp_hyperlinks(messages)


BlockAfterErrorOpt = Annotated[
    bool,
    typer.Option(
        "--block-after-error",
        help="Block after error",
        rich_help_panel="Block After Error",
    ),
]


@dataclass
class Config:
    block_after_error: BlockAfterErrorOpt
