from pathlib import Path
from typing import Annotated

import typer

from cli.fuzz.enums import AdditionalProcessor, DefaultProcessor, Scorer
from cli.fuzz.readers import get_readers
from cli.fuzz.writers import Writer
from cli.utils import extract_extension


def reader_path_callback(value: Path) -> Path:
    extension = extract_extension(value)

    if extension not in get_readers():
        message = f"No implementation found for '{extension}' extension"
        raise typer.BadParameter(message)

    return value


ChoicesPathOpt = Annotated[
    Path,
    typer.Option(
        "-c",
        "--choices-input",
        file_okay=True,
        dir_okay=False,
        exists=True,
        resolve_path=True,
        help="path to a file containing the choices",
        callback=reader_path_callback,
    ),
]

ProcessorOpt = Annotated[
    list[AdditionalProcessor],
    typer.Option(
        "-p",
        "--processor",
        default_factory=list,
    ),
]

DefaultProcessorOpt = Annotated[
    list[DefaultProcessor],
    typer.Option(
        "--default-processor",
        default_factory=lambda: [
            DefaultProcessor["GENERAL"],
            DefaultProcessor["ARABIC"],
        ],
    ),
]

ScorerOpt = Annotated[
    Scorer,
    typer.Option(
        "-s",
        "--scorer",
        envvar="FUZZ_DEFAULT_SCORER",
        help="q for Quick Ratio, w for Weighted Ratio, u for unicode",
    ),
]

AccuracyOpt = Annotated[
    int,
    typer.Option(
        "-a",
        "--accuracy",
        envvar="FUZZ_DEFAULT_ACCURACY",
        help="Accuracy for fuzzy matching 1 to 100",
    ),
]

LimitOpt = Annotated[
    int,
    typer.Option(
        "-l",
        "--limit",
        envvar="FUZZ_DEFAULT_LIMIT",
        help="Limit for matching results",
    ),
]

RemoveDuplicatedOpt = Annotated[
    bool,
    typer.Option(
        "--remove-duplicated",
        envvar="FUZZ_DEFAULT_REMOVE_DUPLICATED",
        help="Remove duplicated results",
    ),
]


QueriesPathOpt = Annotated[
    Path,
    typer.Option(
        "-q",
        "--queries-input",
        file_okay=True,
        dir_okay=False,
        exists=True,
        resolve_path=True,
        help="path to a file containing the queries",
        callback=reader_path_callback,
    ),
]


def export_path_callback(path: Path) -> Path:
    if path.exists():
        message = f"The file {path} already exists."
        raise typer.BadParameter(message)

    return path


ExportPathOpt = Annotated[
    Path,
    typer.Option(
        "-e",
        "--export-path",
        help="Path to the output file",
        exists=False,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        callback=export_path_callback,
    ),
]

WriterOpt = Annotated[
    Writer,
    typer.Option(
        "-w",
        "--writer",
        envvar="FUZZ_DEFAULT_WRITER",
        help="writer type",
    ),
]
