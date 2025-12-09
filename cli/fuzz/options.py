from pathlib import Path
from typing import Annotated

import typer

from .processors import AdditionalProcessor, DefaultProcessor
from .scorers import Scorer
from .writers import Writer

QueriesPathOption = Annotated[
    Path,
    typer.Option(
        "-q",
        "--queries-input",
        file_okay=True,
        dir_okay=False,
        exists=True,
        resolve_path=True,
        help="path to a file containing the queries",
    ),
]

ChoicesPathOption = Annotated[
    Path,
    typer.Option(
        "-c",
        "--choices-input",
        file_okay=True,
        dir_okay=False,
        exists=True,
        resolve_path=True,
        help="path to a file containing the choices",
    ),
]

ProcessorOption = Annotated[
    list[AdditionalProcessor],
    typer.Option("-p", "--processor", default_factory=list),
]

DefaultProcessorOption = Annotated[
    list[DefaultProcessor],
    typer.Option(
        "--default-processor",
        default_factory=lambda: [
            DefaultProcessor["GENERAL"],
            DefaultProcessor["ARABIC"],
        ],
    ),
]

ScorerOption = Annotated[
    Scorer,
    typer.Option(
        "-s",
        "--scorer",
        envvar="DEFAULT_SCORER",
        help="q for Quick Ratio, w for Weighted Ratio, u for unicode",
    ),
]

AccuracyOption = Annotated[
    int,
    typer.Option(
        "-a",
        "--accuracy",
        envvar="DEFAULT_ACCURACY",
        help="Accuracy for fuzzy matching 1 to 100",
    ),
]

LimitOption = Annotated[
    int,
    typer.Option(
        "-l",
        "--limit",
        envvar="DEFAULT_LIMIT",
        help="Limit for matching results",
    ),
]

RemoveDuplicatedOption = Annotated[
    bool,
    typer.Option(
        "--remove-duplicated",
        envvar="DEFAULT_REMOVE_DUPLICATED",
        help="Remove duplicated results",
    ),
]

ExportPathOption = Annotated[
    Path,
    typer.Option(
        "-e",
        "--export-path",
        help="Path to the output file",
        exists=False,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        default_factory=lambda: Path().home() / "Desktop" / "output.xlsx",
    ),
]

WriterOption = Annotated[
    Writer,
    typer.Option(
        "-w",
        "--writer",
        envvar="DEFAULT_WRITER",
        help="writer type",
    ),
]
