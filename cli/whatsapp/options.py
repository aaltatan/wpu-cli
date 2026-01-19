from pathlib import Path
from typing import Annotated

import typer

FilepathArg = Annotated[
    Path,
    typer.Argument(
        help="Path to xlsx file contains the messages",
    ),
]
