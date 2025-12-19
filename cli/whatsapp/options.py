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

BaseUrlOption = Annotated[
    str,
    typer.Option(
        "--url",
        "--base-url",
        help="Base url for whatsapp app",
        envvar="WHATSAPP_DEFAULT_BASE_URL",
    ),
]

MessagesTimeoutOption = Annotated[
    float,
    typer.Option(
        "--timeout-between-messages",
        help="Timeout between messages",
        envvar="WHATSAPP_DEFAULT_TIMEOUT_BETWEEN_MESSAGES",
    ),
]

PageloadTimeoutOption = Annotated[
    float,
    typer.Option(
        "--pageload-timeout",
        help="Timeout for pageload",
        envvar="WHATSAPP_DEFAULT_PAGELOAD_TIMEOUT",
    ),
]
