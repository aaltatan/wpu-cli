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
        callback=loader_path_callback,
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
        callback=loader_path_callback,
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
        envvar="FUZZ_DEFAULT_SCORER",
        help="q for Quick Ratio, w for Weighted Ratio, u for unicode",
    ),
]

AccuracyOption = Annotated[
    int,
    typer.Option(
        "-a",
        "--accuracy",
        envvar="FUZZ_DEFAULT_ACCURACY",
        help="Accuracy for fuzzy matching 1 to 100",
    ),
]

LimitOption = Annotated[
    int,
    typer.Option(
        "-l",
        "--limit",
        envvar="FUZZ_DEFAULT_LIMIT",
        help="Limit for matching results",
    ),
]

RemoveDuplicatedOption = Annotated[
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
        callback=export_path_callback,
    ),
]

WriterOption = Annotated[
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
    choices_path: InitVar[ChoicesPathOption]
    processors: InitVar[ProcessorOption]
    default_processors: InitVar[DefaultProcessorOption]
    scorer: InitVar[ScorerOption]

    accuracy: AccuracyOption
    limit: LimitOption
    remove_duplicated: RemoveDuplicatedOption

    choices: list[str] = field(init=False)
    processor_fn: ProcessFn = field(init=False)
    scorer_fn: ScorerFn = field(init=False)

    def __post_init__(
        self,
        choices_path: ChoicesPathOption,
        processors: ProcessorOption,
        default_processors: DefaultProcessorOption,
        scorer: ScorerOption,
    ) -> None:
        self.choices = get_loader_data(choices_path)
        self.processor_fn = get_processor_fn(processors + default_processors)
        self.scorer_fn = get_scorer_fn(scorer)


def get_options(  # noqa: PLR0913
    choices_path: ChoicesPathOption,
    processors: ProcessorOption,
    default_processors: DefaultProcessorOption,
    scorer: ScorerOption,
    accuracy: AccuracyOption,
    limit: LimitOption,
    remove_duplicated: RemoveDuplicatedOption,
) -> Options:
    return Options(
        choices_path, processors, default_processors, scorer, accuracy, limit, remove_duplicated
    )
