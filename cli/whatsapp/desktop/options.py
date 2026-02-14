from typing import Annotated

import typer

CheckingLoopTimeoutOpt = Annotated[
    int,
    typer.Option(
        "-t",
        "--timeout",
        help="Timeout for checking send status in milliseconds",
        envvar="WHATSAPP_DESKTOP_DEFAULT_CHECKING_LOOP",
        rich_help_panel="Timeout",
    ),
]

AfterOpeningTimeoutOpt = Annotated[
    float,
    typer.Option(
        "--after-opening-timeout",
        help="Timeout for opening hyperlink in milliseconds",
        envvar="WHATSAPP_DESKTOP_DEFAULT_AFTER_OPENING",
        rich_help_panel="Timeout",
    ),
]

BetweenMessagesTimeoutOpt = Annotated[
    float,
    typer.Option(
        "--between-messages-timeout",
        help="Timeout between messages in milliseconds",
        envvar="WHATSAPP_DESKTOP_DEFAULT_BETWEEN_MESSAGES",
        rich_help_panel="Timeout",
    ),
]


BlockAfterErrorOpt = Annotated[
    bool,
    typer.Option(
        "--block-after-error",
        help="Block after error",
        rich_help_panel="Block After Error",
    ),
]
