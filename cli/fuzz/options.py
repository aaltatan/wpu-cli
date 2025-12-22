from dataclasses import InitVar, dataclass, field
from pathlib import Path
from typing import Annotated

import typer

from cli.utils import extract_extension

from .loaders import get_loader_data, get_loaders
from .processors import AdditionalProcessor, DefaultProcessor, ProcessFn, get_processor_fn
from .scorers import Scorer, ScorerFn, get_scorer_fn
from .writers import Writer


def loader_path_callback(value: Path) -> Path:
    extension = extract_extension(value)

    if extension not in get_loaders():
        message = f"No implementation found for '{extension}' extension"
        raise ValueError(message)

    return value


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
        callback=loader_path_callback,
    ),
]

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
        callback=loader_path_callback,
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


@dataclass
class Options:
    choices_path: InitVar[ChoicesPathOpt]
    processors: InitVar[ProcessorOpt]
    default_processors: InitVar[DefaultProcessorOpt]
    scorer: InitVar[ScorerOpt]

    accuracy: AccuracyOpt
    limit: LimitOpt
    remove_duplicated: RemoveDuplicatedOpt

    choices: list[str] = field(init=False)
    processor_fn: ProcessFn = field(init=False)
    scorer_fn: ScorerFn = field(init=False)

    def __post_init__(
        self,
        choices_path: ChoicesPathOpt,
        processors: ProcessorOpt,
        default_processors: DefaultProcessorOpt,
        scorer: ScorerOpt,
    ) -> None:
        self.choices = get_loader_data(choices_path)
        self.processor_fn = get_processor_fn(processors + default_processors)
        self.scorer_fn = get_scorer_fn(scorer)


def get_options(  # noqa: PLR0913
    choices_path: ChoicesPathOpt,
    processors: ProcessorOpt,
    default_processors: DefaultProcessorOpt,
    scorer: ScorerOpt,
    accuracy: AccuracyOpt,
    limit: LimitOpt,
    remove_duplicated: RemoveDuplicatedOpt,
) -> Options:
    return Options(
        choices_path, processors, default_processors, scorer, accuracy, limit, remove_duplicated
    )
